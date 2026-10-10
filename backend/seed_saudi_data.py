import sys
import os
from datetime import datetime, timezone
from sqlmodel import Session, select, delete

# Ensure backend directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.core.database import engine
from app.models.db_models import (
    Project, ScheduleActivity, EarlyWarningAlert, MaterialLogRecord,
    NCRRecord, MIRRecord
)

def populate_saudi_portfolio():
    print("Populating 100% Saudi Construction Mega-Projects Portfolio...")
    with Session(engine) as session:
        # 1. Clear old projects, activities, alerts, materials, NCRs
        session.exec(delete(ScheduleActivity))
        session.exec(delete(Project))
        session.exec(delete(EarlyWarningAlert))
        session.exec(delete(MaterialLogRecord))
        session.exec(delete(NCRRecord))
        session.exec(delete(MIRRecord))
        session.commit()

        # 2. Insert 6 Saudi Projects
        projects = [
            Project(
                project_id="PRJ-01",
                code="KKIA-T5",
                name="فرع مطار الملك خالد الدولي - الصالة 5 (King Khalid International Airport – Terminal 5)",
                client_name="الهيئة العامة للطيران المدني (GACA)",
                consultant_name="دار الهندسة للاستشارات (Dar Al-Handasah)",
                contractor_name="مجموعة بن لادن السعودية للمقاولات (Saudi Binladin Group)",
                baseline_start="2026-01-10",
                baseline_finish="2027-04-30",
                total_budget=28500000.0,
                currency="SAR",
                latitude=24.9576,
                longitude=46.6988,
                location_name="مطار الملك خالد الدولي، الرياض",
                health_status="ON_TRACK",
                is_active=True
            ),
            Project(
                project_id="PRJ-02",
                code="NARGES-TWR",
                name="برج النرجس المالي والأعمال - شمال الرياض (Al-Narges Financial Tower - Riyadh)",
                client_name="شركة روشن العقارية (ROSHN Group)",
                consultant_name="خطيب وعلمي للاستشارات (Khatib & Alami)",
                contractor_name="شركة الفوزان القابضة للمقاولات (Al-Fawzan)",
                baseline_start="2026-01-15",
                baseline_finish="2027-08-31",
                total_budget=32000000.0,
                currency="SAR",
                latitude=24.8421,
                longitude=46.6712,
                location_name="حي النرجس، طريق الملك سلمان، الرياض",
                health_status="WATCH",
                is_active=True
            ),
            Project(
                project_id="PRJ-03",
                code="NEEL-HOSP",
                name="مستشفى النيل التخصصي للرعاية الطبية - جدة (Al-Neel Specialized Hospital - Jeddah)",
                client_name="وزارة الصحة السعودية (Ministry of Health KSA)",
                consultant_name="زهير فايز ومشاركوه (Zuhair Fayez Partnership)",
                contractor_name="شركة المقاولون العرب السعودية (Arab Contractors KSA)",
                baseline_start="2026-02-01",
                baseline_finish="2027-12-15",
                total_budget=24500000.0,
                currency="SAR",
                latitude=21.7215,
                longitude=39.1245,
                location_name="أبحر الشمالية، طريق الملك عبد العزيز، جدة",
                health_status="ON_TRACK",
                is_active=True
            ),
            Project(
                project_id="PRJ-04",
                code="WAHA-RES",
                name="مجمع الواحة السكني الذكي - ضاحية خزام الرياض (Al-Waha Smart Residential Complex - Riyadh)",
                client_name="الشركة الوطنية للإسكان (National Housing Company - NHC)",
                consultant_name="بارسونز العالمية (Parsons International)",
                contractor_name="شركة نسما وشركاهم للمقاولات (Nesma & Partners)",
                baseline_start="2026-03-01",
                baseline_finish="2028-02-28",
                total_budget=18500000.0,
                currency="SAR",
                latitude=24.8912,
                longitude=46.7451,
                location_name="ضاحية خزام السكنية، شمال الرياض",
                health_status="WATCH",
                is_active=True
            ),
            Project(
                project_id="PRJ-05",
                code="HRMN-BRG",
                name="مجمع كباري وتقاطعات طريق الحرمين السريع - مكة المكرمة (Haramain Express Highway Bridges Complex)",
                client_name="وزارة النقل والخدمات اللوجستية (Ministry of Transport & Logistics)",
                consultant_name="إيس محرم باخوم للاستشارات (ACE Moharram Bakhoum)",
                contractor_name="شركة شبه الجزيرة للمقاولات (SAJCO)",
                baseline_start="2025-01-10",
                baseline_finish="2026-09-30",
                total_budget=26000000.0,
                currency="SAR",
                latitude=21.4225,
                longitude=39.8262,
                location_name="طريق الحرمين السريع، مكة المكرمة",
                health_status="COMPLETED",
                is_active=False
            ),
            Project(
                project_id="PRJ-06",
                code="KF-LOGIST",
                name="مركز الملك فهد اللوجستي ومستودعات التبريد - ميناء الدمام (King Fahd Logistics Hub - Dammam Port)",
                client_name="الهيئة العامة للموانئ (موانئ - MAWANI)",
                consultant_name="جاكوبس العالمية (Jacobs Engineering)",
                contractor_name="شركة البواني للمقاولات (Al-Bawani Co.)",
                baseline_start="2025-02-15",
                baseline_finish="2026-08-30",
                total_budget=19500000.0,
                currency="SAR",
                latitude=26.4382,
                longitude=50.1583,
                location_name="ميناء الملك عبد العزيز، الدمام، المنطقة الشرقية",
                health_status="COMPLETED",
                is_active=False
            )
        ]

        for p in projects:
            session.add(p)
        session.commit()

        # 3. Insert 17 Civil Activities with real Saudi project data
        activities = [
            # --- PRJ-01: KKIA-T5 ---
            ScheduleActivity(
                activity_id="ACT-4001",
                project_id="PRJ-01",
                name="تدعيم ورصف مهبط الطائرات ومسارات الصالة السريعة (Runway Taxiway High-Strength Paving)",
                wbs="0.01.01 Airside Civil Infrastructure",
                start_date="2026-08-01",
                finish_date="2026-09-20",
                planned_value=6800000.0,
                earned_value=6800000.0,
                actual_cost=6650000.0,
                predecessors=None,
                assigned_team="Engr. Mohammed Gassim",
                status="Completed",
                is_critical_path=False,
                float_days=10
            ),
            ScheduleActivity(
                activity_id="ACT-4010",
                project_id="PRJ-01",
                name="تركيب مظلات وهياكل التراس الفولاذية لصالة السفر 5 (Steel Truss Canopy Fabrication)",
                wbs="1.04.02 Terminal Building / Structural Steel",
                start_date="2026-09-25",
                finish_date="2026-10-28",
                planned_value=8500000.0,
                earned_value=8100000.0,
                actual_cost=8300000.0,
                predecessors="ACT-4001",
                assigned_team="Engr. Asem Othman",
                status="In Progress",
                is_critical_path=True,
                float_days=0
            ),
            ScheduleActivity(
                activity_id="ACT-4040",
                project_id="PRJ-01",
                name="أعمال عزل خرسانة خزانات مياه الإطفاء الأرضية (Water Tank Waterproofing & Leakage Test)",
                wbs="1.02.04 Substructure / Water Reservoir",
                start_date="2026-10-01",
                finish_date="2026-10-14",
                planned_value=3100000.0,
                earned_value=1800000.0,
                actual_cost=2400000.0,
                predecessors="ACT-4001",
                assigned_team="Engr. Saleh Mohammed",
                status="Delayed",
                is_critical_path=True,
                float_days=0
            ),
            ScheduleActivity(
                activity_id="ACT-4050",
                project_id="PRJ-01",
                name="معايرة واختبار سيور نقل الأمتعة الذكية BHS (Baggage Handling Systems Calibration)",
                wbs="2.03.01 Special Airport Systems",
                start_date="2026-10-10",
                finish_date="2026-11-05",
                planned_value=5200000.0,
                earned_value=4600000.0,
                actual_cost=4800000.0,
                predecessors="ACT-4010",
                assigned_team="Engr. Abu baker Mohammed",
                status="In Progress",
                is_critical_path=False,
                float_days=5
            ),

            # --- PRJ-02: NARGES-TWR ---
            ScheduleActivity(
                activity_id="ACT-1005",
                project_id="PRJ-02",
                name="أعمال الحفر العميق لـ 3 طوابق قبو وإحلال التربة (Deep Foundation Excavation 14m)",
                wbs="1.01.01 Substructure / Earthworks",
                start_date="2026-08-10",
                finish_date="2026-09-15",
                planned_value=3800000.0,
                earned_value=3800000.0,
                actual_cost=3650000.0,
                predecessors=None,
                assigned_team="Engr. Mohammed Gassim",
                status="Completed",
                is_critical_path=False,
                float_days=8
            ),
            ScheduleActivity(
                activity_id="ACT-1010",
                project_id="PRJ-02",
                name="صب خرسانة اللبشة المسلحة C50 Zone B (Raft Foundation Concrete Pouring 3200m3)",
                wbs="1.02.01 Substructure / Raft Foundation",
                start_date="2026-09-20",
                finish_date="2026-10-18",
                planned_value=4500000.0,
                earned_value=4200000.0,
                actual_cost=4350000.0,
                predecessors="ACT-1005",
                assigned_team="Engr. Mohammed Gassim",
                status="In Progress",
                is_critical_path=True,
                float_days=0
            ),
            ScheduleActivity(
                activity_id="ACT-1020",
                project_id="PRJ-02",
                name="توريد وتركيب حديد تسليح حوائط القص والكور - الدور 4 (Shear Wall & Core Rebar Fixing)",
                wbs="1.03.01 Superstructure / Vertical Core Walls",
                start_date="2026-10-02",
                finish_date="2026-10-12",
                planned_value=3200000.0,
                earned_value=1900000.0,
                actual_cost=2600000.0,
                predecessors="ACT-1010",
                assigned_team="Engr. Mohammed Gassim",
                status="Delayed",
                is_critical_path=True,
                float_days=0
            ),
            ScheduleActivity(
                activity_id="ACT-1030",
                project_id="PRJ-02",
                name="أعمال الشدات المعدنية وأعمدة الطابق المتكرر 5 (Formwork & Columns Casting Level 5)",
                wbs="1.03.02 Superstructure / Columns & Slabs",
                start_date="2026-10-08",
                finish_date="2026-10-24",
                planned_value=2800000.0,
                earned_value=2500000.0,
                actual_cost=2650000.0,
                predecessors="ACT-1010",
                assigned_team="Engr. Asem Othman",
                status="In Progress",
                is_critical_path=False,
                float_days=3
            ),
            ScheduleActivity(
                activity_id="ACT-1040",
                project_id="PRJ-02",
                name="تمديدات مواسير التغذية والصرف الصحي الرأسي MEP (Vertical Chilled Water & Drainage Risers)",
                wbs="2.01.02 MEP / Plumbing & HVAC Risers",
                start_date="2026-10-12",
                finish_date="2026-11-02",
                planned_value=2100000.0,
                earned_value=1600000.0,
                actual_cost=1800000.0,
                predecessors="ACT-1030",
                assigned_team="Engr. Abu baker Mohammed",
                status="In Progress",
                is_critical_path=False,
                float_days=4
            ),

            # --- PRJ-03: NEEL-HOSP ---
            ScheduleActivity(
                activity_id="ACT-2005",
                project_id="PRJ-03",
                name="أعمال سند الجوانب بالخوازيق المتقاطعة Secant Piles (Deep Shoring & Ground Anchors)",
                wbs="1.01.03 Substructure / Shoring Works",
                start_date="2026-08-15",
                finish_date="2026-09-25",
                planned_value=5400000.0,
                earned_value=5400000.0,
                actual_cost=5200000.0,
                predecessors=None,
                assigned_team="Engr. Saleh Mohammed",
                status="Completed",
                is_critical_path=False,
                float_days=12
            ),
            ScheduleActivity(
                activity_id="ACT-2015",
                project_id="PRJ-03",
                name="توريد وتركيب تشيلرات التكييف المركزي ووحدات مناولة الهواء AHU (Central Chillers & AHU Roof Units)",
                wbs="2.01.03 MEP / HVAC Hospital Chillers",
                start_date="2026-10-01",
                finish_date="2026-10-16",
                planned_value=4200000.0,
                earned_value=2100000.0,
                actual_cost=3100000.0,
                predecessors="ACT-2005",
                assigned_team="Engr. Rafat Mohammed",
                status="Delayed",
                is_critical_path=True,
                float_days=0
            ),
            ScheduleActivity(
                activity_id="ACT-2020",
                project_id="PRJ-03",
                name="شبكة الغازات الطبية ومحطة التغذية الكهربائية الطارئة (Medical Gas Network & Dual Substations)",
                wbs="2.02.01 MEP / Medical Gas & Power",
                start_date="2026-10-10",
                finish_date="2026-10-30",
                planned_value=3900000.0,
                earned_value=3100000.0,
                actual_cost=3300000.0,
                predecessors="ACT-2005",
                assigned_team="Engr. Saleh Mohammed",
                status="In Progress",
                is_critical_path=False,
                float_days=6
            ),

            # --- PRJ-04: WAHA-RES ---
            ScheduleActivity(
                activity_id="ACT-6010",
                project_id="PRJ-04",
                name="حفر وتجهيز قواعد وميد الفيلات السكنية Cluster 1 (Residential Villas Footing Excavation)",
                wbs="1.01.02 Earthworks & Foundations",
                start_date="2026-10-04",
                finish_date="2026-10-22",
                planned_value=4800000.0,
                earned_value=3900000.0,
                actual_cost=4100000.0,
                predecessors=None,
                assigned_team="Engr. Rafat Mohammed",
                status="In Progress",
                is_critical_path=False,
                float_days=4
            ),
            ScheduleActivity(
                activity_id="ACT-6020",
                project_id="PRJ-04",
                name="البنية التحتية لشبكات الاتصالات والألياف الضوئية والري (Smart Grid & Irrigation Subsurface Utilities)",
                wbs="3.01.01 Utilities / Smart Infrastructure",
                start_date="2026-10-14",
                finish_date="2026-11-10",
                planned_value=3500000.0,
                earned_value=2200000.0,
                actual_cost=2400000.0,
                predecessors="ACT-6010",
                assigned_team="Engr. Mohammed Gassim",
                status="In Progress",
                is_critical_path=False,
                float_days=5
            ),

            # --- PRJ-05: HRMN-BRG (Completed) ---
            ScheduleActivity(
                activity_id="ACT-3001",
                project_id="PRJ-05",
                name="تنفيذ الركائز الخرسانية والكمرات سابقة الإجهاد (Pier Columns & Prestressed Girder Launching)",
                wbs="1.02.01 Bridge Substructure & Superstructure",
                start_date="2025-06-01",
                finish_date="2026-08-30",
                planned_value=14000000.0,
                earned_value=14000000.0,
                actual_cost=13600000.0,
                predecessors=None,
                assigned_team="Engr. Saleh Mohammed",
                status="Completed",
                is_critical_path=False,
                float_days=0
            ),
            ScheduleActivity(
                activity_id="ACT-3002",
                project_id="PRJ-05",
                name="أعمال الرصف الإسفلتي وفواصل التمدد وحواجز الأمان (Asphalt Wearing Course & Expansion Joints)",
                wbs="1.03.01 Bridge Decking & Road Surfacing",
                start_date="2026-08-15",
                finish_date="2026-09-28",
                planned_value=12000000.0,
                earned_value=12000000.0,
                actual_cost=11850000.0,
                predecessors="ACT-3001",
                assigned_team="Engr. Mohammed Gassim",
                status="Completed",
                is_critical_path=False,
                float_days=0
            ),

            # --- PRJ-06: KF-LOGIST (Completed) ---
            ScheduleActivity(
                activity_id="ACT-5001",
                project_id="PRJ-06",
                name="الهياكل الإنشائية المعدنية للمستودعات اللوجستية الذكية (Steel Portal Warehouse Frames)",
                wbs="1.04.01 Warehouse Heavy Steel Structures",
                start_date="2025-08-01",
                finish_date="2026-07-20",
                planned_value=11000000.0,
                earned_value=11000000.0,
                actual_cost=10700000.0,
                predecessors=None,
                assigned_team="Engr. Asem Othman",
                status="Completed",
                is_critical_path=False,
                float_days=0
            ),
            ScheduleActivity(
                activity_id="ACT-5002",
                project_id="PRJ-06",
                name="غرف ومستودعات التبريد المركزي ومنظومة الطاقة المتجددة (Cold Storage Plant & Solar Power Integration)",
                wbs="2.04.01 Refrigeration & Photovoltaic Solar",
                start_date="2026-07-15",
                finish_date="2026-08-25",
                planned_value=8500000.0,
                earned_value=8500000.0,
                actual_cost=8300000.0,
                predecessors="ACT-5001",
                assigned_team="Engr. Abu baker Mohammed",
                status="Completed",
                is_critical_path=False,
                float_days=0
            )
        ]

        for a in activities:
            session.add(a)
        session.commit()

        # 4. Insert Early Warning Alerts directly tied to the 3 delayed activities
        alerts = [
            EarlyWarningAlert(
                alert_id="ALT-001",
                project_id="PRJ-02",
                severity="CRITICAL",
                category="SCHEDULE_SPI",
                title="تأخير زمني حرج: مؤشر SPI انخفض إلى 0.810 (حديد حوائط الكور - ACT-1020)",
                description="انحراف الجدول الزمني في برج النرجس بالرياض بسبب تأخر اعتماد استشاري دار الهندسة لشهادات اختبار حديد التسليح سابك (متأخر 6 أيام على المسار الحرج).",
                recommended_action="تكثيف ورديات الحدادين (Double Shift) وتطبيق خطة التعجيل (Fast-Tracking) لاعتماد المهندس المقيم قبل موعد الصب."
            ),
            EarlyWarningAlert(
                alert_id="ALT-002",
                project_id="PRJ-03",
                severity="CRITICAL",
                category="PROCUREMENT_CUSTOMS",
                title="تأخير توريدات حرج: فحص تشيلرات التكييف المركزي بميناء جدة (ACT-2015)",
                description="تأخر فسح وحدات التبريد المركزية Chilled Water بميناء جدة الإسلامي لمستشفى النيل التخصصي (+12 يوماً بسبب متطلبات هيئة الغذاء والدواء).",
                recommended_action="إصدار خطاب إفراج وتخليص عاجل بالتعاون مع هيئة الزكاة والضريبة والجمارك (ZATCA) لتفادي تأخير غرف العمليات والعناية المركزة."
            ),
            EarlyWarningAlert(
                alert_id="ALT-003",
                project_id="PRJ-01",
                severity="WARNING",
                category="DEWATERING_SITE",
                title="تأخير مسار غير حرج: عزل خزانات مياه الإطفاء بمطار الملك خالد (ACT-4040)",
                description="تأخر دهان العزل الإيبوكسي لخزان المياه الأرضي بالصالة 5 نتيجة زيادة الرطوبة ونزح المياه السطحية (+5 أيام).",
                recommended_action="زيادة طلمبات النزح السطحي Wellpoint Pumps وتجفيف القاع بمدافع الهواء الساخن لاعتماد اختبار العزل المائي."
            )
        ]

        for al in alerts:
            session.add(al)
        session.commit()

        # 5. Materials Logs in Saudi Mega Projects
        materials = [
            MaterialLogRecord(
                project_id="PRJ-01",
                material_description="Ready-Mix Concrete C50 Micro-Silica (Runway Apron)",
                delivery_date="2026-10-05",
                delivery_note_number="DN-KSA-9901",
                quantity=650.0,
                unit="Cubic Meters (m3)",
                supplier="Saudi Ready Mix Concrete Co.",
                inspection_status="Passed",
                notes="Approved for airport apron pavement section C"
            ),
            MaterialLogRecord(
                project_id="PRJ-02",
                material_description="High-Tensile Deformed Steel Rebar 32mm Grade 60 (SABIC)",
                delivery_date="2026-10-06",
                delivery_note_number="DN-KSA-9902",
                quantity=120.0,
                unit="Tons",
                supplier="SABIC Saudi Basic Industries",
                inspection_status="Pending",
                notes="Mill test certificate under Dar Al-Handasah review"
            ),
            MaterialLogRecord(
                project_id="PRJ-03",
                material_description="Dual Centrifugal Water Chillers 850TR (Carrier KSA)",
                delivery_date="2026-10-04",
                delivery_note_number="DN-KSA-9903",
                quantity=2.0,
                unit="Units",
                supplier="Carrier Saudi Arabia - Jeddah Port Consignment",
                inspection_status="Pending",
                notes="Awaiting SASO customs release certification"
            )
        ]
        for m in materials:
            session.add(m)
        session.commit()

        print("Successfully populated 100% Saudi Construction Mega-Projects Portfolio!")

if __name__ == "__main__":
    populate_saudi_portfolio()
