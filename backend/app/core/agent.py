import json
import uuid
import re
from typing import Dict, Any, List, Optional, Tuple
from sqlmodel import Session, select
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage

from app.config import settings
from app.core.database import engine
from app.models.db_models import ChatSession, ChatMessage, PendingAction, Project, ScheduleActivity, NCRRecord
from app.models.schemas import ChatMessageResponse, ActionRequiredPayload

# Import all Enterprise Tools
from app.tools.staff_tool import query_staff_directory
from app.tools.schedule_tool import get_schedule_metrics, get_daily_activities
from app.tools.material_tool import query_material_log
from app.tools.email_tool import send_notification_email
from app.tools.calendar_tool import schedule_meeting
from app.tools.meeting_summary_tool import summarize_meeting_transcript
from app.tools.project_controls_tool import get_lookahead_schedule, analyze_schedule_delays_and_recovery
from app.tools.qa_qc_tool import query_ncr_records, query_mir_inspection_requests
from app.tools.site_management_tool import get_daily_site_report, get_equipment_and_machinery_log

ENTERPRISE_PM_SYSTEM_PROMPT = """You are "Smart Assistant" (المساعد الذكي), an expert AI Project Controls & Construction Management Partner for Civil, Structural, and MEP Project Directors and Site Engineers.

You possess deep domain expertise in:
1. Earned Value Management (EVM): PV, EV, AC, SPI, CPI, SV, CV, EAC, ETC, BAC, TCPI, and S-Curves.
2. Schedule & Primavera P6 / MS Project: Critical Path Method (CPM), 3-Week/4-Week Look Ahead, Float, Delay Analysis & Recovery Plans.
3. QA/QC & Site Operations: NCRs, MIRs, Concrete Test Logs, Daily Site Reports (DSR), Material Delivery Notes (BOQ), and Heavy Equipment tracking.
4. Human-In-The-Loop (HITL) Safety: Proposing actions (emails, calendar meetings) with mandatory engineer approval before execution.

BEHAVIOR AND TONE GUIDELINES:
- **Intelligent, Natural & Engaging**: Speak like an experienced, helpful senior engineering colleague ("يا باشمهندس" / "Eng. [Name]").
- **Adaptive Language**: If the user writes in Arabic (especially Egyptian dialect, e.g., "قولي يعني ايه", "ازيك يا هندسة", "صبة الخرسانة"), respond in natural, professional, and clear Arabic. If in English, respond in English.
- **Explanations vs Data**:
  - When asked conceptual / educational questions (e.g. "يعني ايه EVM", "ما هو المسار الحرج", "What is SPI?"), provide a clear, insightful conceptual explanation with practical construction examples.
  - When asked for project metrics or status, ground your answer in verified tool data and present it clearly with insights and recommendations.
- **Deterministic Math**: NEVER hallucinate project numbers; maintain exact numbers from project records.
- **Concise & Direct Responses (إجابات مختصرة ومباشرة ومحددة)**: Always provide brief, high-impact, direct answers without unnecessary padding, filler, or long essays (مختصر ومباشر جداً). State key figures (Progress %, Budget, SPI, CPI, or specific activity status) directly in 2-4 bullet points or 1-2 short sentences.
- **Strict Active Project Context**: Always answer strictly based on the currently selected project provided in the context. Never confuse projects or default to another project when a specific project is selected.
"""

ALL_TOOLS = [
    query_staff_directory,
    get_schedule_metrics,
    get_daily_activities,
    get_lookahead_schedule,
    analyze_schedule_delays_and_recovery,
    query_material_log,
    query_ncr_records,
    query_mir_inspection_requests,
    get_daily_site_report,
    get_equipment_and_machinery_log,
    send_notification_email,
    schedule_meeting,
    summarize_meeting_transcript,
]

TOOLS_BY_NAME = {t.name: t for t in ALL_TOOLS}

FALLBACK_GEMINI_MODELS = [
    "gemini-3.7-flash",
    "gemini-3.5-flash",
    "gemini-flash-latest"
]

class PMAgentOrchestrator:
    def __init__(self):
        self.system_prompt = ENTERPRISE_PM_SYSTEM_PROMPT

    def _get_llm(self, provider_override: Optional[str] = None):
        provider = provider_override or settings.LLM_PROVIDER
        if provider == "openai" and settings.OPENAI_API_KEY:
            try:
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(
                    model=settings.OPENAI_MODEL,
                    api_key=settings.OPENAI_API_KEY,
                    temperature=0.3
                )
            except Exception:
                return None
        return None

    def _extract_action_payload(self, text: str) -> Tuple[str, Optional[ActionRequiredPayload]]:
        try:
            match = re.search(r'\{[\s\S]*"type"\s*:\s*"ACTION_REQUIRED"[\s\S]*\}', text)
            if match:
                json_str = match.group(0)
                data = json.loads(json_str)
                cleaned_text = text.replace(json_str, "").strip()
                if not cleaned_text:
                    cleaned_text = (
                        f"⚠️ **Action Required**: {data.get('preview_title', 'Action requires your confirmation.')}\n\n"
                        f"Please review the action details below and click **Approve** or **Edit**."
                    )
                action = ActionRequiredPayload(
                    type="ACTION_REQUIRED",
                    action_id=data["action_id"],
                    tool=data["tool"],
                    parameters=data["parameters"],
                    preview_title=data.get("preview_title"),
                    preview_details=data.get("preview_details")
                )
                return cleaned_text, action
        except Exception as e:
            print(f"Error parsing action payload: {e}")
        return text, None

    def _rule_based_router(self, user_msg: str, prj_ctx: Optional[Dict[str, Any]] = None) -> Tuple[str, Optional[ActionRequiredPayload], List[Dict[str, Any]]]:
        """Comprehensive intelligent router for conceptual inquiries, small talk, and deterministic tools."""
        text = user_msg.lower().strip()
        words = set(re.findall(r'[\w\u0600-\u06FF]+', text))

        # --- 0. Small Talk & Greetings ---
        small_talk_thanks = {"شكرا", "شكراً", "تسلم", "تمام", "thx", "thanks", "متشكر"}
        if words.intersection(small_talk_thanks) or any(k in text for k in ["ألف شكر", "الف شكر", "الله يخليك", "thank you", "تسلم يا هندسة"]):
            resp = "العفو يا باشمهندس! تحت أمرك في أي وقت لمتابعة أعمال الموقع والتحكم الهندسي. لو محتاج أي استفسار أو تقرير أنا جاهز."
            return resp, None, [{"title": "Smart Assistant Core", "category": "General", "type": "Conversational"}]

        small_talk_greetings = {"كيفك", "ازيك", "أخبارك", "اخبارك", "مرحبا", "أهلاً", "اهلا", "هاي", "hello", "hi", "hey"}
        if words.intersection(small_talk_greetings) or any(k in text for k in ["صباح الخير", "مساء الخير", "السلام عليكم", "عامل ايه", "ازي حضرتك", "يا هلا"]):
            resp = "الحمد لله كله تمام وبخير يا باشمهندس! 👷‍♂️\nجاهز لمساعدتك في أي حاجة تخص المشروع: مراجعة الجدول الزمني P6، حسابات الـ EVM، متابعة توريدات الحديد والخرسانة، أو فحص تقارير الجودة (NCR/MIR). تحب نبدأ بإيه؟"
            return resp, None, [{"title": "Smart Assistant Core", "category": "General", "type": "Conversational"}]

        identity_queries = ["مين انت", "من انت", "عرف نفسك", "بتعمل ايه", "وظيفتك ايه", "who are you", "what can you do"]
        if any(k in text for k in identity_queries):
            resp = (
                "أنا **Smart Assistant (المساعد الهندسي الذكي)** لمشاريع التشييد والتحكم الهندسي (Project Controls).\n\n"
                "وظيفتي أساعدك في:\n"
                "1. **متابعة الجداول الزمنية:** قراءة جداول Primavera P6 (.XER / .CSV) ومتابعة الـ Critical Path والـ Look Ahead.\n"
                "2. **حسابات القيمة المكتسبة (EVM):** حساب مؤشرات SPI و CPI والانحرافات وتوليد منحنى S-Curve.\n"
                "3. **التوريدات والجودة:** تتبع استلامات الحديد والخرسانة، ومتابعة محاضر عدم المطابقة (NCR) وطلبات الفحص (MIR).\n"
                "4. **الأتمتة الآمنة (HITL):** صياغة إيميلات وجدولة اجتماعات مع اشتراط موافقتك قبل التنفيذ."
            )
            return resp, None, [{"title": "Smart Assistant Core", "category": "General", "type": "Conversational"}]

        # --- 1. Conceptual / Educational Questions (Explain Concepts clearly) ---
        is_conceptual = any(k in text for k in [
            "يعني ايه", "ما هو", "ما هي", "ماذا تعني", "اشرح", "فهمني", "معنى", "عرف", 
            "ازاي بيتحسب", "طريقة حساب", "كيف يتم", "what is", "explain", "meaning of", "how to calculate", "what does"
        ])

        if is_conceptual:
            # Concept: EVM / Earned Value Management
            if any(k in text for k in ["evm", "earned value", "قيمة مكتسبة", "القيمة المكتسبة"]):
                resp = (
                    "**إدارة القيمة المكتسبة (EVM - Earned Value Management):**\n\n"
                    "هي منهجية هندسية معتمدة دولياً لمراقبة أداء المشروع ومقارنة **التقدم الفعلي** و**المصاريف الحقيقية** بالـ **Baseline (الخطة الأساسية)**.\n\n"
                    "تعتمد على 3 ركائز أساسية:\n"
                    "1. **PV (Planned Value - القيمة المخططة):** الميزانية المفترض صرفها للأعمال المخططة حتى تاريخ اليوم.\n"
                    "2. **EV (Earned Value - القيمة المكتسبة):** القيمة المالية للعمل الذي تم إنجازه فعلياً على أرض الواقع.\n"
                    "3. **AC (Actual Cost - التكلفة الفعلية):** ما تم صرفه فعلياً حتى الآن.\n\n"
                    "ومنها بنحسب أهم مؤشرين:\n"
                    "• **SPI (مؤشر الأداء الزمني = EV / PV):** لو أكبر من 1 يعني المشروع متقدم زمنياً، لو أقل من 1 يعني فيه تأخير.\n"
                    "• **CPI (مؤشر الأداء المالي = EV / AC):** لو أكبر من 1 يعني فيه توفير، لو أقل من 1 يعني فيه زيادة تكلفة (Over Budget)."
                )
                return resp, None, [{"title": "Project Controls Knowledge Base (EVM Standards)", "category": "Educational", "type": "EVM Theory"}]

            # Concept: SPI
            if "spi" in text or "مؤشر الأداء الزمني" in text:
                resp = (
                    "**مؤشر الأداء الزمني (SPI - Schedule Performance Index):**\n\n"
                    "• **القانون:** `SPI = EV / PV` (القيمة المكتسبة ÷ القيمة المخططة)\n"
                    "• **تفسير النتائج:**\n"
                    "  - `SPI = 1.0`: المشروع ماشي تماماً حسب الجدول الزمني المخطط (On Track).\n"
                    "  - `SPI > 1.0`: المشروع متقدم ومسبق الجدول الزمني (Ahead of Schedule).\n"
                    "  - `SPI < 1.0`: المشروع متأخر عن الخطة ويحتاج خطة تعافي (Behind Schedule / Delayed)."
                )
                return resp, None, [{"title": "Project Controls Knowledge Base (SPI)", "category": "Educational", "type": "EVM Theory"}]

            # Concept: CPI
            if "cpi" in text or "مؤشر أداء التكلفة" in text:
                resp = (
                    "**مؤشر أداء التكلفة (CPI - Cost Performance Index):**\n\n"
                    "• **القانون:** `CPI = EV / AC` (القيمة المكتسبة ÷ التكلفة الفعلية)\n"
                    "• **تفسير النتائج:**\n"
                    "  - `CPI = 1.0`: المصروفات مطابقة للميزانية المحددة بالظبط.\n"
                    "  - `CPI > 1.0`: كفاءة عالية وتوفير في الميزانية (Under Budget).\n"
                    "  - `CPI < 1.0`: تجاوز في الميزانية وصرف زيادة عن المنجز (Over Budget)."
                )
                return resp, None, [{"title": "Project Controls Knowledge Base (CPI)", "category": "Educational", "type": "EVM Theory"}]

            # Concept: Critical Path
            if any(k in text for k in ["critical path", "مسار حرج", "المسار الحرج"]):
                resp = (
                    "**المسار الحرج (Critical Path Method - CPM):**\n\n"
                    "هو أطول مسار للأنشطة المتتابعة في المشروع من تاريخ البداية حتى النهاية، وتتميز بنوده بأن **إجمالي السماحية (Total Float = 0)**.\n\n"
                    "💡 **الأهمية الهندسية:**\n"
                    "أي يوم تأخير في أي بند يقع على المسار الحرج (زي صب الأعمدة أو الخرسانة المسلحة) يؤخر تاريخ تسليم المشروع بالكامل بشكل مباشر ما لم يتم عمل Crashing أو Fast-Tracking."
                )
                return resp, None, [{"title": "Primavera P6 Scheduling Principles", "category": "Educational", "type": "CPM Theory"}]

            # Concept: Look Ahead Schedule
            if any(k in text for k in ["look ahead", "لوك اهيد", "خطة اسابيع"]):
                resp = (
                    "**الجدول التطلعي (Look Ahead Schedule):**\n\n"
                    "هو جدول تفصيلي قصير المدى (عادة 3 إلى 6 أسابيع) يتم استخراجه من الجدول الزمني العام للمشروع (Master Schedule).\n\n"
                    "🎯 **الهدف منه:**\n"
                    "مساعدة مهندسي الموقع في التجهيز المسبق للعمالة، المعدات، اعتماد الشوب دروينج، وطلب توريد المواد (Material Requisitions) قبل موعد التنفيذ الفعلي لتجنب أي توقف."
                )
                return resp, None, [{"title": "Site Operations Planning", "category": "Educational", "type": "Look Ahead Theory"}]

            # Concept: S-Curve
            if any(k in text for k in ["s-curve", "منحنى s", "منحنى التدفق"]):
                resp = (
                    "**منحنى التدفق التراكمي (Dynamic S-Curve):**\n\n"
                    "هو تمثيل بياني تراكمي للمصروفات أو نسب الإنجاز عبر الزمن. يأخذ شكل حرف (S) لأن معدل الصرف والإنجاز يبدأ بطيئاً في مرحلة الحفر والتجهيزات، ثم يتسارع في مرحلة الهيكل والتشطيبات، ثم يتباطأ مجدداً عند التسليم والـ Snag List."
                )
                return resp, None, [{"title": "Project Controls S-Curve Guide", "category": "Educational", "type": "S-Curve Theory"}]

        # --- 2. Email Dispatch (HITL - Priority Intent) ---
        if any(k in text for k in ["email", "إيميل", "ايميل", "ابعت", "أبعت", "send email", "رسالة", "ميل"]):
            recipient = "sherif.site@company.com"
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_msg)
            if email_match:
                recipient = email_match.group(0)
            subject = "Project Update: Site Milestones & Schedule Review"
            body = "Dear Eng. Sherif,\n\nPlease review the updated progress report and ongoing foundation pouring activities.\n\nBest regards,\nSmart Assistant PM"
            raw_res = send_notification_email.invoke({
                "recipient_email": recipient,
                "subject": subject,
                "message": body,
                "requires_approval": True
            })
            resp, action = self._extract_action_payload(raw_res)
            return resp, action, [{"title": "SMTP Dispatch Safety Layer", "category": "HITL Actions", "type": "Security"}]

        # --- 3. Meeting Scheduling (HITL - Priority Intent) ---
        if any(k in text for k in ["meeting", "اجتماع", "ميعاد", "schedule meeting", "احجز", "حدد اجتماع"]):
            title = "Site Coordination & Quality Review Meeting"
            start_iso = "2026-10-05T10:00:00+03:00"
            raw_res = schedule_meeting.invoke({
                "title": title,
                "start_time_iso": start_iso,
                "duration_minutes": 45,
                "attendees": ["sherif.site@company.com", "nourhan.qc@company.com", "ahmed.planning@company.com"],
                "requires_approval": True
            })
            resp, action = self._extract_action_payload(raw_res)
            return resp, action, [{"title": "Google Calendar & Outlook Coordinator", "category": "HITL Actions", "type": "Calendar"}]

        # --- 4. Look Ahead Schedule ---
        if any(k in text for k in ["look ahead", "lookahead", "3-week", "لوك اهيد", "الأسابيع القادمة", "خطة الأسبوعين", "خطة 3 أسابيع", "تلات أسابيع", "3 أسابيع"]):
            res = get_lookahead_schedule.invoke({"weeks": 3})
            return res, None, [{"title": "Primavera P6 3-Week Look Ahead", "category": "Schedule", "type": "P6 Parser"}]

        # --- 5. Delay Analysis & Recovery Plan ---
        if any(k in text for k in ["delay", "recovery", "تأخير", "خطة تعافي", "مسار حرج", "critical path", "tia", "تعويض التأخير"]):
            if prj_ctx:
                crit_acts = prj_ctx.get('crit_activities', [])
                crit_names = ", ".join([f"{a['id']}: {a['name'][:28]}" for a in crit_acts]) if crit_acts else "لا توجد أنشطة حرجة متأخرة حالياً"
                del_acts = prj_ctx.get('delayed_activities', [])
                del_names = ", ".join([f"{a['id']}: {a['name'][:28]}" for a in del_acts]) if del_acts else "لا توجد تأخيرات حالياً"
                is_ar = any(c in user_msg for c in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي")
                if is_ar:
                    resp = (
                        f"⚠️ **تحليل المسار الحرج والتأخيرات لمشروع: {prj_ctx['name']}**\n\n"
                        f"• **أنشطة المسار الحرج:** {crit_names}\n"
                        f"• **الأنشطة المتأخرة:** {del_names}\n"
                        f"• **مؤشر الأداء الزمني (SPI):** {prj_ctx['spi']:.3f} ({prj_ctx['spi_status']})\n"
                        f"• **التوصية المختصرة:** تسريع توريد المواد واعتماد ورديات إضافية (Crashing) لتعويض فارق الجدول الزمني."
                    )
                else:
                    resp = (
                        f"⚠️ **Critical Path & Delay Analysis: {prj_ctx['name']}**\n\n"
                        f"• **Critical Path Tasks:** {crit_names}\n"
                        f"• **Delayed Tasks:** {del_names}\n"
                        f"• **Schedule Performance (SPI):** {prj_ctx['spi']:.3f} ({prj_ctx['spi_status_en']})\n"
                        f"• **Key Action:** Authorize additional shift crashing and expedite material inspection requests."
                    )
                return resp, None, [{"title": f"Critical Path - {prj_ctx['code']}", "category": "Schedule", "type": "Project Controls"}]
            res = analyze_schedule_delays_and_recovery.invoke({})
            return res, None, [{"title": "Primavera P6 Critical Path Analysis", "category": "Schedule", "type": "Project Controls"}]

        # --- 6. QA/QC: NCR Reports ---
        if any(k in text for k in ["ncr", "عدم مطابقة", "ملاحظات جودة", "تقرير جودة", "عيوب"]):
            res = query_ncr_records.invoke({"status": "ALL"})
            return res, None, [{"title": "QA/QC Non-Conformance Registry", "category": "QA/QC", "type": "Site Inspections"}]

        # --- 7. QA/QC: MIR Inspection Requests ---
        if any(k in text for k in ["mir", "sir", "طلب فحص", "استلام مواد", "فحص خرسانة", "فحص صاج", "inspection"]):
            res = query_mir_inspection_requests.invoke({"material": ""})
            return res, None, [{"title": "Material Inspection Requests (MIR) Log", "category": "QA/QC", "type": "Consultant MIR"}]

        # --- 8. Equipment & Heavy Machinery ---
        if any(k in text for k in ["معدات", "معدة", "equipment", "machinery", "crane", "أوناش", "ونش", "حفار", "لودر"]):
            res = get_equipment_and_machinery_log.invoke({})
            return res, None, [{"title": "Heavy Machinery & Equipment Deployment Log", "category": "Site", "type": "Operations"}]

        # --- 9. Daily Site Report (DSR) & Manpower ---
        if any(k in text for k in ["تقرير يومي", "dsr", "daily report", "daily site report", "عمالة", "manpower", "headcount"]):
            res = get_daily_site_report.invoke({"report_date": "2026-10-04"})
            return res, None, [{"title": "Daily Site Progress Report (DSR)", "category": "Site", "type": "Field Logs"}]

        # --- 10. Staff queries ---
        if any(k in text for k in ["staff", "team", "engineer", "مهندس", "مين", "مسؤول", "رقم", "تليفون", "phone", "qc", "planning", "مدير"]):
            role = ""
            if "qc" in text or "جودة" in text:
                role = "QA/QC"
            elif "planning" in text or "تخطيط" in text or "جدول" in text:
                role = "Planning"
            elif "site" in text or "موقع" in text:
                role = "Site"
            elif "procurement" in text or "مشتريات" in text or "توريد" in text:
                role = "Procurement"
            elif "mep" in text or "كهربا" in text or "تكييف" in text:
                role = "MEP"
            elif "tech" in text or "مكتب فني" in text or "شوب دروينج" in text:
                role = "Technical Office"
            res = query_staff_directory.invoke({"role": role, "query": user_msg})
            return res, None, [{"title": "Project Organization Chart & Directory", "category": "Staff", "type": "HR Database"}]

        # --- 11. Schedule KPIs & Progress Inquiries (EVM, SPI, CPI, PV, EV, AC Project Status) ---
        if any(k in text for k in [
            "kpi", "spi", "cpi", "evm", "planned value", "earned value", "actual cost",
            "معدل الأداء", "تكلفة", "ميزانية", "موقف المشروع", "أداء المشروع", "حسابات المشروع",
            "نسبة", "إنجاز", "انجاز", "نسبة الإنجاز", "نسبة الانجاز", "نسبة إنجاز", "تقدم",
            "المشروع", "خلصنا اد ايه", "وصلنا لفين", "progress", "completion", "budget", "خالد", "النرجس", "النيل", "الواحة", "الحرمين", "اللوجستي"
        ]):
            if prj_ctx:
                is_ar = any(c in user_msg for c in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي")
                if is_ar:
                    resp = (
                        f"📌 **مشروع: {prj_ctx['name']}** ({prj_ctx['code']})\n\n"
                        f"• **نسبة الإنجاز الكلية:** {prj_ctx['prog_pct']:.1f}%\n"
                        f"• **الميزانية المعتمدة (BAC):** SAR {prj_ctx['bac']:,.2f}\n"
                        f"• **التكلفة الفعلية المنفقة (AC):** SAR {prj_ctx['ac']:,.2f} | **المتبقي:** SAR {prj_ctx['remaining']:,.2f}\n"
                        f"• **مؤشر الأداء الزمني (SPI):** {prj_ctx['spi']:.3f} ({prj_ctx['spi_status']})\n"
                        f"• **مؤشر كفاءة التكلفة (CPI):** {prj_ctx['cpi']:.3f} ({prj_ctx['cpi_status']})\n"
                        f"• **حالة الأنشطة:** {prj_ctx['activities_count']} نشاط ({prj_ctx['delayed_count']} متأخر)"
                    )
                else:
                    resp = (
                        f"📌 **Project: {prj_ctx['name']}** ({prj_ctx['code']})\n\n"
                        f"• **Total Progress:** {prj_ctx['prog_pct']:.1f}%\n"
                        f"• **Approved Budget (BAC):** SAR {prj_ctx['bac']:,.2f}\n"
                        f"• **Actual Cost Incurred (AC):** SAR {prj_ctx['ac']:,.2f} | **Remaining:** SAR {prj_ctx['remaining']:,.2f}\n"
                        f"• **Schedule Performance (SPI):** {prj_ctx['spi']:.3f} ({prj_ctx['spi_status_en']})\n"
                        f"• **Cost Performance (CPI):** {prj_ctx['cpi']:.3f} ({prj_ctx['cpi_status_en']})\n"
                        f"• **Activities Status:** {prj_ctx['activities_count']} tasks ({prj_ctx['delayed_count']} delayed)"
                    )
                return resp, None, [{"title": f"Live EVM - {prj_ctx['code']}", "category": "Schedule", "type": "Deterministic EVM"}]
            res = get_schedule_metrics.invoke({"kpi_name": "ALL", "period_or_month": "October 2026"})
            return res, None, [{"title": "Live EVM Engine (BAC, PV, EV, AC, SPI, CPI)", "category": "Schedule", "type": "Deterministic EVM"}]

        # --- 12. Daily Activities & Schedule tasks ---
        if any(k in text for k in ["activity", "activities", "schedule", "أنشطة", "نشاط", "صب", "خرسانة", "جدول", "اليوم", "today", "date", "تاريخ", "2026"]):
            target_date = "2026-10-04"
            date_match = re.search(r'\d{4}-\d{2}-\d{2}', user_msg)
            if date_match:
                target_date = date_match.group(0)
            res = get_daily_activities.invoke({"target_date": target_date})
            return res, None, [{"title": "Primavera P6 Activity Schedule", "category": "Schedule", "type": "Database"}]

        # --- 13. Material & Delivery Logs ---
        if any(k in text for k in ["material", "materials", "delivery", "مواد", "توريدات", "حديد", "صاج", "duct", "rebar", "boq", "مستخلص"]):
            mat_name = ""
            if "حديد" in text or "rebar" in text or "steel" in text:
                mat_name = "Steel Rebar"
            elif "خرسانة" in text or "concrete" in text:
                mat_name = "Concrete"
            elif "صاج" in text or "duct" in text:
                mat_name = "Ductwork"
            res = query_material_log.invoke({"material_name": mat_name})
            return res, None, [{"title": "Site Material Receiving & QC Log (BOQ)", "category": "Materials", "type": "Procurement"}]

        # --- 14. Meeting Summary ---
        if any(k in text for k in ["summarize", "summary", "تلخيص", "محضر", "اجتماع", "محاضر", "transcript"]):
            res = summarize_meeting_transcript.invoke({"raw_text": user_msg})
            return res, None, [{"title": "Meeting Transcript & Action Matrix", "category": "Meetings", "type": "Transcripts"}]

        # --- Helpful Conversational Fallback ---
        fallback = (
            "تحت أمرك يا باشمهندس! فهمت إنك بتسأل عن حاجة تخص إدارة المشروع، ممكن توضح سؤالك أكتر، أو تختار من المواضيع دي:\n\n"
            "• **شرح المفاهيم:** `قولي يعني ايه EVM` أو `اشرح لي الـ SPI والـ CPI` أو `ما هو المسار الحرج`\n"
            "• **موقف المشروع الحالي:** `اعرضلي موقف الـ SPI والـ CPI للشهر ده` أو `تحليل التأخيرات`\n"
            "• **الموقع والتوريدات:** `سجل توريد حديد التسليح` أو `تقارير الـ NCR المفتوحة`\n"
            "• **الإجراءات:** `ابعت إيميل لمهندس الموقع` أو `حدد اجتماع تنسيقي غداً`"
        )
        return fallback, None, [{"title": "Smart Assistant Knowledge Base", "category": "General", "type": "Fallback Guidance"}]

    def _extract_gemini_text(self, response) -> str:
        """Safely extracts text parts from Gemini response candidates, handling thinking/thought parts."""
        try:
            if hasattr(response, "candidates") and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                    text_parts = [p.text for p in candidate.content.parts if hasattr(p, "text") and p.text]
                    if text_parts:
                        return "\n\n".join(text_parts).strip()
            return getattr(response, "text", "")
        except Exception:
            return getattr(response, "text", "")

    def _get_project_context_summary(self, project_id: Optional[str] = None) -> Tuple[Dict[str, Any], str]:
        """Retrieves a comprehensive snapshot of the selected project, EVM metrics, and activities for LLM context grounding."""
        try:
            with Session(engine) as session:
                prj = None
                if project_id:
                    prj = session.exec(select(Project).where(Project.project_id == project_id)).first()
                    if not prj:
                        prj = session.exec(select(Project).where(Project.code == project_id.upper().strip())).first()
                if not prj:
                    prj = session.exec(select(Project).where(Project.is_active == True)).first()
                if not prj:
                    prj = session.exec(select(Project)).first()

                if not prj:
                    prj = Project(
                        project_id="PRJ-01",
                        code="KKIA-T5",
                        name="فرع مطار الملك خالد الدولي - الصالة 5 (King Khalid International Airport – Terminal 5)",
                        client_name="الهيئة العامة للطيران المدني (GACA)",
                        contractor_name="مجموعة بن لادن السعودية للمقاولات",
                        total_budget=28500000.0,
                        currency="SAR"
                    )

                activities = session.exec(
                    select(ScheduleActivity).where(ScheduleActivity.project_id == prj.project_id)
                ).all()
                if not activities and prj.project_id == "PRJ-01":
                    activities = session.exec(select(ScheduleActivity)).all()

                pv = sum(a.planned_value for a in activities)
                ev = sum(a.earned_value for a in activities)
                ac = sum(a.actual_cost for a in activities)
                bac = prj.total_budget or 15000000.0

                spi = round(ev / pv, 3) if pv > 0 else 1.0
                cpi = round(ev / ac, 3) if ac > 0 else 1.0
                sv = round(ev - pv, 2)
                cv = round(ev - ac, 2)
                prog_pct = round((ev / pv * 100), 1) if pv > 0 else 100.0
                remaining = max(0.0, bac - ac)

                delayed_acts = []
                crit_acts = []
                act_lines = []
                for a in activities:
                    a_prog = round((a.earned_value / a.planned_value * 100), 1) if a.planned_value > 0 else 100.0
                    crit_mark = " [CRITICAL PATH]" if a.is_critical_path else ""
                    if a.is_critical_path:
                        crit_acts.append({"id": a.activity_id, "name": a.name, "finish": a.finish_date})
                    if "delay" in a.status.lower() or (a.planned_value > a.earned_value and a.status != "Completed"):
                        delayed_acts.append({"id": a.activity_id, "name": a.name, "finish": a.finish_date})
                    act_lines.append(
                        f"- [{a.activity_id}] {a.name}: Progress={a_prog}% | Status={a.status}{crit_mark} | PV=SAR {a.planned_value:,.2f} | EV=SAR {a.earned_value:,.2f} | AC=SAR {a.actual_cost:,.2f} | Finish={a.finish_date}"
                    )

                act_summary = "\n".join(act_lines) if act_lines else "لا توجد أنشطة مسجلة لهذا المشروع."

                ctx_dict = {
                    "project_id": prj.project_id,
                    "code": prj.code,
                    "name": prj.name,
                    "client_name": prj.client_name,
                    "contractor_name": prj.contractor_name,
                    "consultant_name": prj.consultant_name,
                    "baseline_start": prj.baseline_start,
                    "baseline_finish": prj.baseline_finish,
                    "bac": bac,
                    "pv": pv,
                    "ev": ev,
                    "ac": ac,
                    "remaining": remaining,
                    "spi": spi,
                    "cpi": cpi,
                    "sv": sv,
                    "cv": cv,
                    "prog_pct": prog_pct,
                    "spi_status": "مطابق/متقدم عن الجدول" if spi >= 1.0 else "متأخر عن الجدول الزمني",
                    "spi_status_en": "On Track / Ahead" if spi >= 1.0 else "Delayed",
                    "cpi_status": "وفورات مالية / ضمن الميزانية" if cpi >= 1.0 else "تجاوز في الميزانية",
                    "cpi_status_en": "Under Budget / Savings" if cpi >= 1.0 else "Cost Overrun",
                    "activities_count": len(activities),
                    "delayed_count": len(delayed_acts),
                    "crit_activities": crit_acts,
                    "delayed_activities": delayed_acts
                }

                summary = (
                    f"CURRENT SELECTED PROJECT (المشروع المحدد حالياً):\n"
                    f"• Project ID: {prj.project_id}\n"
                    f"• Project Code: {prj.code}\n"
                    f"• Project Name: {prj.name}\n"
                    f"• Client: {prj.client_name}\n"
                    f"• Contractor: {prj.contractor_name}\n"
                    f"• Consultant: {prj.consultant_name}\n"
                    f"• Baseline Timeline: {prj.baseline_start} to {prj.baseline_finish}\n"
                    f"• Approved Budget (BAC): SAR {bac:,.2f}\n"
                    f"• Incurred Actual Cost (AC): SAR {ac:,.2f}\n"
                    f"• Remaining Budget: SAR {remaining:,.2f}\n"
                    f"• Overall Progress %: {prog_pct:.1f}%\n"
                    f"• Planned Value (PV): SAR {pv:,.2f}\n"
                    f"• Earned Value (EV): SAR {ev:,.2f}\n"
                    f"• Schedule Performance Index (SPI): {spi:.3f} ({ctx_dict['spi_status_en']})\n"
                    f"• Cost Performance Index (CPI): {cpi:.3f} ({ctx_dict['cpi_status_en']})\n"
                    f"• Schedule Variance (SV): SAR {sv:,.2f}\n"
                    f"• Cost Variance (CV): SAR {cv:,.2f}\n"
                    f"• Schedule Activities ({len(activities)} tasks, {len(delayed_acts)} delayed, {len(crit_acts)} critical):\n"
                    f"{act_summary}\n"
                )
                return ctx_dict, summary
        except Exception as e:
            fallback_dict = {
                "project_id": "PRJ-01",
                "code": "KKIA-T5",
                "name": "فرع مطار الملك خالد الدولي - الصالة 5 (King Khalid International Airport – Terminal 5)",
                "bac": 28500000.0,
                "ac": 22208000.0,
                "remaining": 6292000.0,
                "prog_pct": 90.2,
                "spi": 0.902,
                "cpi": 0.962,
                "spi_status": "متأخر",
                "spi_status_en": "Delayed",
                "cpi_status": "تجاوز تكلفة طفيف",
                "cpi_status_en": "Over Budget",
                "activities_count": 5,
                "delayed_count": 1,
                "crit_activities": [],
                "delayed_activities": []
            }
            return fallback_dict, "Project: King Khalid International Airport Terminal 5, Progress: 90.2%, Budget: SAR 28,500,000.00"

    async def _call_gemini_with_fallback(self, prompt: str) -> Optional[str]:
        """Calls Gemini API with automatic model fallback in case of rate limits or quotas."""
        if not settings.GEMINI_API_KEY:
            return None
        import requests

        models_to_try = [
            settings.GEMINI_MODEL,
            "gemini-flash-lite-latest",
            "gemini-3.1-flash-lite",
            "gemini-3.5-flash-lite",
            "gemini-3.8-flash",
            "gemini-3.7-flash",
            "gemini-flash-latest"
        ]
        seen = set()
        unique_models = [m for m in models_to_try if not (m in seen or seen.add(m))]

        for model_name in unique_models:
            clean_name = model_name.replace("models/", "")
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_name}:generateContent?key={settings.GEMINI_API_KEY}"
                payload = {
                    "contents": [
                        {
                            "parts": [
                                {"text": prompt}
                            ]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.2,
                        "maxOutputTokens": 350
                    }
                }
                res = requests.post(url, json=payload, timeout=20)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        text_parts = [p.get("text", "") for p in parts if p.get("text")]
                        text = "\n\n".join(text_parts).strip()
                        if text:
                            return text
            except Exception as e:
                print(f"[GEMINI_FALLBACK] Model {clean_name} error: {e}. Trying next...")
                continue
        return None

    async def process_message(
        self,
        user_message: str,
        session_id: Optional[str] = None,
        provider_override: Optional[str] = None,
        project_id: Optional[str] = None
    ) -> ChatMessageResponse:
        if not session_id:
            session_id = f"sess_{uuid.uuid4().hex[:8]}"

        with Session(engine) as session:
            sess = session.get(ChatSession, session_id)
            if not sess:
                sess = ChatSession(session_id=session_id, title=user_message[:35] + "...")
                session.add(sess)
                session.commit()

            user_record = ChatMessage(session_id=session_id, role="user", content=user_message)
            session.add(user_record)
            session.commit()

            history_records = session.exec(
                select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc())
            ).all()

        active_provider = provider_override or settings.LLM_PROVIDER
        sources: List[Dict[str, Any]] = []
        action_payload: Optional[ActionRequiredPayload] = None
        response_text = ""

        # Retrieve dynamic context for the selected project
        prj_ctx, project_context = self._get_project_context_summary(project_id)

        # 1. LangChain Tool Calling / Explicit LLM (if configured and supported)
        llm = self._get_llm(provider_override)
        if llm is not None and not isinstance(llm, str) and hasattr(llm, "bind_tools"):
            try:
                print(f"[CHAT_ROUTING] path=llm:{active_provider}")
                llm_with_tools = llm.bind_tools(ALL_TOOLS)
                
                messages = [SystemMessage(content=self.system_prompt + f"\n\nCURRENT PROJECT:\n{project_context}")]
                for r in history_records[-6:]:
                    if r.role == "user":
                        messages.append(HumanMessage(content=r.content))
                    elif r.role == "assistant":
                        messages.append(AIMessage(content=r.content))

                ai_response = await llm_with_tools.ainvoke(messages)
                
                if hasattr(ai_response, "tool_calls") and ai_response.tool_calls:
                    tool_call = ai_response.tool_calls[0]
                    tool_name = tool_call.get("name")
                    tool_args = tool_call.get("args", {})
                    
                    if tool_name in TOOLS_BY_NAME:
                        tool_func = TOOLS_BY_NAME[tool_name]
                        tool_output = tool_func.invoke(tool_args)
                        cleaned_resp, action_payload = self._extract_action_payload(str(tool_output))
                        sources.append({"title": f"Tool: {tool_name}", "category": "Live System", "type": "API Execution"})
                        
                        if not action_payload:
                            followup_messages = messages + [
                                ai_response,
                                ToolMessage(content=str(tool_output), tool_call_id=tool_call.get("id", "call_1"))
                            ]
                            final_ai = await llm.ainvoke(followup_messages)
                            response_text = str(final_ai.content)
                        else:
                            response_text = cleaned_resp
                    else:
                        response_text = str(ai_response.content)
                else:
                    raw_content = str(getattr(ai_response, "content", ai_response))
                    response_text, action_payload = self._extract_action_payload(raw_content)
                    sources.append({"title": "AI LLM Reasoning Engine", "category": "AI Inference", "type": "Configured LLM"})

            except Exception as e:
                print(f"LLM invoke error: {e}. Switching to direct Gemini/Rule pipeline.")
                llm = None

        # 2. Direct Gemini Generation with multi-model fallback & smart grounding
        if response_text == "" and action_payload is None and active_provider == "gemini" and settings.GEMINI_API_KEY:
            try:
                print(f"[CHAT_ROUTING] path=llm:gemini")
                text_low = user_message.lower().strip()

                # Check for HITL actions first (Security check)
                if any(k in text_low for k in ["email", "إيميل", "ايميل", "ab3at", "ابعت", "أبعت", "send email", "رسالة", "ميل"]):
                    rule_resp, action_payload, sources = self._rule_based_router(user_message, prj_ctx)
                    response_text = rule_resp
                elif any(k in text_low for k in ["meeting", "اجتماع", "ميعاد", "schedule meeting", "احجز", "حدد اجتماع"]):
                    rule_resp, action_payload, sources = self._rule_based_router(user_message, prj_ctx)
                    response_text = rule_resp
                else:
                    # Run router to check if we have domain tool data or conceptual insight
                    rule_resp, _, detected_sources = self._rule_based_router(user_message, prj_ctx)
                    is_domain_tool = detected_sources and detected_sources[0].get("type") in ["Deterministic EVM", "P6 Parser", "Project Controls", "Procurement", "Site Inspections", "Field Logs", "HR Database"]

                    # Build conversation context
                    conv_history = ""
                    for r in history_records[-6:]:
                        conv_history += f"{r.role.upper()}: {r.content}\n"

                    if is_domain_tool:
                        sources = detected_sources
                        grounded_prompt = (
                            f"{self.system_prompt}\n\n"
                            f"CURRENT ACTIVE PROJECT CONTEXT (Answer strictly for this project):\n{project_context}\n\n"
                            f"Conversation History:\n{conv_history}\n\n"
                            f"Verified Project Database Record:\n'''\n{rule_resp}\n'''\n\n"
                            f"User Inquiry: {user_message}\n\n"
                            f"MANDATORY INSTRUCTIONS:\n"
                            f"1. STRICT PROJECT CONTEXT: The user is currently inspecting project '{prj_ctx['name']}' (Code: {prj_ctx['code']}). Answer EXCLUSIVELY about this project. Never mention other projects.\n"
                            f"2. CONCISE & DIRECT (مختصر ومباشر جداً وبدون إطالة أو حشو): Answer in 2 to 4 concise bullet points or 1-2 short punchy sentences maximum. Directly provide the requested figures (Progress %, Budget, SPI, CPI, or specific activity status) without conversational filler.\n"
                            f"3. Strictly maintain the exact deterministic metrics from the database record without altering any numbers or dates.\n"
                            f"4. Respond in the same language as the user (Egyptian Arabic or English)."
                        )
                        gemini_res = await self._call_gemini_with_fallback(grounded_prompt)
                        response_text = gemini_res if gemini_res else rule_resp
                    else:
                        # Open conceptual reasoning, small talk, explanations
                        sources = detected_sources if detected_sources else [{"title": "Google Gemini Flash Engine", "category": "AI LLM", "type": "Cloud Model"}]
                        chat_prompt = (
                            f"{self.system_prompt}\n\n"
                            f"CURRENT ACTIVE PROJECT CONTEXT (Answer strictly for this project):\n{project_context}\n\n"
                            f"Conversation History:\n{conv_history}\n\n"
                            f"User Inquiry: {user_message}\n\n"
                            f"MANDATORY INSTRUCTIONS:\n"
                            f"1. STRICT PROJECT CONTEXT: Answer strictly about project '{prj_ctx['name']}' (Code: {prj_ctx['code']}).\n"
                            f"2. CONCISE & DIRECT (مختصر ومباشر): Keep your response brief, clear, and focused on key facts (maximum 2-3 short bullet points or 2 sentences). Avoid long essays or repetitive greetings.\n"
                            f"3. Respond in the same language as the user (Egyptian Arabic or English)."
                        )
                        gemini_res = await self._call_gemini_with_fallback(chat_prompt)
                        response_text = gemini_res if gemini_res else rule_resp

            except Exception as e:
                print(f"Gemini LLM error: {e}. Falling back to rule router.")
                print(f"[CHAT_ROUTING] path=rule")
                response_text, action_payload, sources = self._rule_based_router(user_message, prj_ctx)

        # 3. Fallback to Rule Router if still empty
        if response_text == "" and action_payload is None:
            print(f"[CHAT_ROUTING] path=rule")
            response_text, action_payload, sources = self._rule_based_router(user_message, prj_ctx)

        with Session(engine) as session:
            meta = json.dumps({
                "action_required": action_payload.model_dump() if action_payload else None,
                "sources": sources
            })
            asst_record = ChatMessage(session_id=session_id, role="assistant", content=response_text, metadata_json=meta)
            session.add(asst_record)
            session.commit()

        return ChatMessageResponse(
            session_id=session_id,
            response=response_text,
            action_required=action_payload,
            sources=sources
        )

# Singleton Agent Orchestrator
agent_orchestrator = PMAgentOrchestrator()
