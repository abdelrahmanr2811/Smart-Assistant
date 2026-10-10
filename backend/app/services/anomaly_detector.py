from datetime import datetime, timezone
from typing import List, Dict, Any
from sqlmodel import Session, select

from app.core.database import engine
from app.models.db_models import (
    Project, ScheduleActivity, MaterialLogRecord, NCRRecord, EarlyWarningAlert
)

def run_project_anomaly_audit(project_id: str = "PRJ-01") -> Dict[str, Any]:
    with Session(engine) as session:
        prj = session.exec(select(Project).where(Project.project_id == project_id)).first()
        if not prj:
            prj = session.exec(select(Project).where(Project.is_active == True)).first()
        
        prj_id = prj.project_id if prj else project_id

        activities = session.exec(select(ScheduleActivity)).all()
        ncrs = session.exec(select(NCRRecord)).all()
        materials = session.exec(select(MaterialLogRecord)).all()

        pv = sum(a.planned_value for a in activities) or 500000.0
        ev = sum(a.earned_value for a in activities) or 410000.0
        ac = sum(a.actual_cost for a in activities) or 415000.0

        spi = round(ev / pv, 3) if pv > 0 else 1.0
        cpi = round(ev / ac, 3) if ac > 0 else 1.0

        detected_alerts: List[Dict[str, Any]] = []

        # 1. SPI Anomaly Check (Schedule Delay)
        if spi < 0.85:
            detected_alerts.append({
                "alert_id": f"ALT-SPI-{prj_id}",
                "severity": "CRITICAL",
                "category": "SCHEDULE_SPI",
                "title": f"تأخير زمني حرج: مؤشر SPI انخفض إلى {spi:.3f} (< 0.85)",
                "description": f"القيمة المكتسبة المنفذة فعلياً (${ev:,.2f}) تقل بمقدار ${pv - ev:,.2f} عن المخطط (${pv:,.2f}).",
                "recommended_action": "تطبيق خطة تعافي فورية (Recovery Schedule / Fast-Tracking) لزيادة ساعات العمل ومعدلات الإنتاج."
            })
        elif spi < 0.95:
            detected_alerts.append({
                "alert_id": f"ALT-SPI-{prj_id}",
                "severity": "WARNING",
                "category": "SCHEDULE_SPI",
                "title": f"تنبيه زمني مبكر: مؤشر SPI = {spi:.3f}",
                "description": "تراجع طفيف في معدل تقدم الأنشطة عن الجدول المعتمد.",
                "recommended_action": "مراجعة معدلات الإنجاز الأسبوعية مع مقاولي الباطن."
            })

        # 2. CPI Anomaly Check (Cost Overrun)
        if cpi < 0.85:
            detected_alerts.append({
                "alert_id": f"ALT-CPI-{prj_id}",
                "severity": "CRITICAL",
                "category": "COST_CPI",
                "title": f"تجاوز حرج في الميزانية: مؤشر CPI انخفض إلى {cpi:.3f} (< 0.85)",
                "description": f"التكلفة الفعلية المنصرفة (${ac:,.2f}) تجاوزت القيمة المكتسبة (${ev:,.2f}).",
                "recommended_action": "إيقاف أوامر التغيير غير المعتمدة والتدقيق الفوري على أسعار التوريدات والمستخلصات."
            })

        # 3. Critical Path Overdue Activities
        crit_delayed = [a for a in activities if a.is_critical_path and a.status == "In Progress"]
        if crit_delayed:
            act_names = ", ".join([a.activity_id for a in crit_delayed[:2]])
            detected_alerts.append({
                "alert_id": f"ALT-CP-{prj_id}",
                "severity": "WARNING",
                "category": "CRITICAL_PATH",
                "title": f"أنشطة حرجة تحت المراقبة: ({act_names})",
                "description": f"يوجد {len(crit_delayed)} أنشطة تقع على المسار الحرج (Total Float = 0) ومتبقية قيد التنفيذ.",
                "recommended_action": "إعطاء الأولوية القصوى لتسليم حديد وصب هذه البنود لتجنب زحزحة تاريخ تسليم المشروع."
            })

        # 4. Open QA/QC NCRs
        open_ncrs = [n for n in ncrs if n.status == "Open"]
        if open_ncrs:
            detected_alerts.append({
                "alert_id": f"ALT-NCR-{prj_id}",
                "severity": "WARNING",
                "category": "QA_QC_NCR",
                "title": f"يوجد {len(open_ncrs)} تقارير عدم مطابقة (NCR) مفتوحة",
                "description": f"تقرير {open_ncrs[0].ncr_number}: {open_ncrs[0].title}",
                "recommended_action": "استكمال أعمال المعالجة وتقديم طلب فحص استشاري لإغلاق الـ NCR."
            })

        # Calculate Health Score (0 - 100%)
        health_score = 100
        for alt in detected_alerts:
            if alt["severity"] == "CRITICAL":
                health_score -= 20
            elif alt["severity"] == "WARNING":
                health_score -= 10
        health_score = max(20, min(100, health_score))

        return {
            "project_id": prj_id,
            "project_name": prj.name if prj else "Al-Narges Tower",
            "health_score": health_score,
            "health_status": "EXCELLENT" if health_score >= 85 else ("GOOD" if health_score >= 70 else "AT_RISK"),
            "spi": spi,
            "cpi": cpi,
            "total_alerts_count": len(detected_alerts),
            "alerts": detected_alerts,
            "audit_timestamp": datetime.now(timezone.utc).isoformat()
        }
