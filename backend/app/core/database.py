import os
import json
from datetime import datetime, timezone
from sqlmodel import SQLModel, create_engine, Session, select
from app.config import settings
from app.models.db_models import (
    Project, EarlyWarningAlert, User, AuditLog, ChatSession, ChatMessage, PendingAction,
    StaffRecord, ScheduleActivity, MaterialLogRecord, ProjectDocument,
    NCRRecord, MIRRecord, DailySiteReport, ContractClaim, VariationOrder, PaymentCertificate
)

# Connect to Database (PostgreSQL / SQLite fallback)
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
engine = create_engine(settings.DATABASE_URL, echo=False, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

def _migrate_sqlite_schema():
    with engine.connect() as conn:
        tables_to_check = [
            "staff_records", "schedule_activities", "material_logs",
            "ncr_records", "mir_records", "daily_site_reports",
            "project_documents", "chat_sessions", "pending_actions",
            "contract_claims", "variation_orders", "payment_certificates"
        ]
        for tbl in tables_to_check:
            try:
                res = conn.exec_driver_sql(f"PRAGMA table_info({tbl})").fetchall()
                col_names = [r[1] for r in res]
                if col_names and "project_id" not in col_names:
                    conn.exec_driver_sql(f"ALTER TABLE {tbl} ADD COLUMN project_id TEXT DEFAULT 'PRJ-01'")
                    conn.commit()
            except Exception as e:
                pass
        
        # Check GIS columns on projects table
        try:
            res = conn.exec_driver_sql("PRAGMA table_info(projects)").fetchall()
            cols = [r[1] for r in res]
            if "latitude" not in cols:
                conn.exec_driver_sql("ALTER TABLE projects ADD COLUMN latitude REAL DEFAULT 30.0270")
            if "longitude" not in cols:
                conn.exec_driver_sql("ALTER TABLE projects ADD COLUMN longitude REAL DEFAULT 31.4913")
            if "location_name" not in cols:
                conn.exec_driver_sql("ALTER TABLE projects ADD COLUMN location_name TEXT DEFAULT 'New Cairo, Egypt'")
            if "health_status" not in cols:
                conn.exec_driver_sql("ALTER TABLE projects ADD COLUMN health_status TEXT DEFAULT 'WATCH'")
            conn.commit()
        except Exception:
            pass

        # Check phone column on users table
        try:
            res = conn.exec_driver_sql("PRAGMA table_info(users)").fetchall()
            cols = [r[1] for r in res]
            if "phone" not in cols:
                conn.exec_driver_sql("ALTER TABLE users ADD COLUMN phone TEXT DEFAULT '+966 50 123 4567'")
            conn.commit()
        except Exception:
            pass


from app.core.security import hash_password

def ensure_team_users(session: Session):
    team_data = [
        {
            "user_id": "usr_asem_01",
            "email": "asem.othman@company.com",
            "full_name": "Engr. Asem Othman",
            "role": "PROJECT_DIRECTOR",
            "title": "Project Manager",
            "phone": "+966 50 555 4101"
        },
        {
            "user_id": "usr_saleh_02",
            "email": "saleh.mohammed@company.com",
            "full_name": "Engr. Saleh Mohammed",
            "role": "SITE_MANAGER",
            "title": "Site Manager",
            "phone": "+966 55 234 5678"
        },
        {
            "user_id": "usr_mohammed_03",
            "email": "mohammed.gassim@company.com",
            "full_name": "Engr. Mohammed Gassim",
            "role": "QA_QC_MANAGER",
            "title": "Quality Engineer",
            "phone": "+966 56 345 6789"
        },
        {
            "user_id": "usr_rafat_04",
            "email": "rafat.mohammed@company.com",
            "full_name": "Engr. Rafat Mohammed",
            "role": "PLANNING_ENGINEER",
            "title": "Planning Engineer",
            "phone": "+966 57 456 7890"
        },
        {
            "user_id": "usr_abubaker_05",
            "email": "abubaker.mohammed@company.com",
            "full_name": "Engr. Abu baker Mohammed",
            "role": "SITE_MANAGER",
            "title": "Civil Engineer",
            "phone": "+966 58 567 8901"
        },
    ]

    hashed = hash_password("Admin123")
    for t in team_data:
        u = session.exec(select(User).where((User.user_id == t["user_id"]) | (User.email == t["email"]))).first()
        if not u:
            u = User(
                user_id=t["user_id"],
                email=t["email"],
                hashed_password=hashed,
                full_name=t["full_name"],
                role=t["role"]
            )
            session.add(u)
        else:
            u.full_name = t["full_name"]
            u.hashed_password = hashed
            session.add(u)

        s = session.exec(select(StaffRecord).where(StaffRecord.email == t["email"])).first()
        if not s:
            s = StaffRecord(
                full_name=t["full_name"],
                title=t["title"],
                department="Engineering",
                phone=t["phone"],
                email=t["email"],
                reporting_manager="Engr. Asem Othman"
            )
            session.add(s)

    session.commit()

def init_db():
    SQLModel.metadata.create_all(engine)
    _migrate_sqlite_schema()
    with Session(engine) as session:
        ensure_team_users(session)
    seed_initial_data()

def seed_initial_data():
    with Session(engine) as session:
        ensure_team_users(session)

        # Check projects - auto migrate if Cairo projects found or empty
        existing_prj = session.exec(select(Project).where(Project.project_id == "PRJ-01")).first()
        if not existing_prj or "Cairo" in str(getattr(existing_prj, 'location_name', '')) or "القاهرة" in str(getattr(existing_prj, 'name', '')):
            try:
                import sys
                cur_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                if cur_dir not in sys.path:
                    sys.path.insert(0, cur_dir)
                from seed_saudi_data import populate_saudi_portfolio
                populate_saudi_portfolio()
                return
            except Exception as e:
                print("Could not auto-seed Saudi portfolio:", e)

        # Check alerts
        existing_alert = session.exec(select(EarlyWarningAlert).where(EarlyWarningAlert.alert_id == "ALT-001")).first()
        if not existing_alert:
            alerts = [
                EarlyWarningAlert(
                    alert_id="ALT-001",
                    project_id="PRJ-01",
                    severity="CRITICAL",
                    category="SCHEDULE_SPI",
                    title="تأخير زمني حرج: مؤشر SPI انخفض إلى 0.820",
                    description="انحراف الجدول الزمني بمقدار 90,000 ر.س (Schedule Variance = -90,000 SAR) عن الخطة المعتمدة لشهر أكتوبر 2026.",
                    recommended_action="تطبيق خطة تعافي (Fast-Tracking) وتكثيف ورديات صب الأعمدة وحوائط الكور."
                ),
                EarlyWarningAlert(
                    alert_id="ALT-002",
                    project_id="PRJ-01",
                    severity="WARNING",
                    category="CRITICAL_PATH",
                    title="نشاط حرج متأخر: حديد حوائط الكور (ACT-1020)",
                    description="النشاط ACT-1020 يقع على المسار الحرج وتاريخ النهاية المتوقع متأخر 4 أيام عن موعد الصب المخطط.",
                    recommended_action="زيادة طاقم الحدادين التابع للمقاول الباطن لاعتماد التسليح قبل ميعاد الاستشاري."
                ),
                EarlyWarningAlert(
                    alert_id="ALT-003",
                    project_id="PRJ-01",
                    severity="WARNING",
                    category="QA_QC_NCR",
                    title="تقرير عدم مطابقة مفتوح: تعشيش خرسانة القواعد (NCR-STR-2026-004)",
                    description="ملاحظة جودة غير مغلقة منذ 4 أيام تخص معالجة تعشيش خرسانة قواعد المحول C12 بمونة إيبوكسية غير منكمشة.",
                    recommended_action="متابعة تقديم نتائج اختبار الكور والتأكد من توقيع استشاري المالك على إغلاق الـ NCR."
                ),
            ]
            for a in alerts:
                session.add(a)
            session.commit()

        print("Seeding initial Enterprise Construction Project data into Database...")
        
        # 0. Initial Users (RBAC)
        existing_user = session.exec(select(User).where(User.user_id == "usr_admin_01")).first()
        if not existing_user:
            users = [
                User(
                    user_id="usr_admin_01",
                    email="director@company.com",
                    hashed_password="hashed_dev_password",
                    full_name="Eng. Yasser (Project Director)",
                    role="PROJECT_DIRECTOR"
                ),
                User(
                    user_id="usr_site_02",
                    email="sherif.site@company.com",
                    hashed_password="hashed_dev_password",
                    full_name="Eng. Sherif Mostafa (Site Construction Manager)",
                    role="SITE_MANAGER"
                ),
            ]
            for u in users:
                session.add(u)
            session.commit()

        # 1. Staff Members
        existing_staff = session.exec(select(StaffRecord).where(StaffRecord.email == "sherif.site@company.com")).first()
        if not existing_staff:
            staff_members = [
                StaffRecord(
                    full_name="Eng. Sherif Mostafa",
                    title="Site Construction Manager",
                    department="Site Operations",
                    phone="+20 100 123 4567",
                    email="sherif.site@company.com",
                    reporting_manager="Eng. Yasser (Project Director)",
                    skills="Civil Engineering, Site Logistics, Heavy Pouring, Safety Supervision"
                ),
                StaffRecord(
                    full_name="Eng. Ahmed El-Sayed",
                    title="Lead Planning & Scheduling Engineer",
                    department="Project Controls",
                    phone="+20 101 234 5678",
                    email="ahmed.planning@company.com",
                    reporting_manager="Eng. Sherif Mostafa",
                    skills="Primavera P6, MS Project, Earned Value Management (EVM), Delay Analysis, S-Curve"
                ),
                StaffRecord(
                    full_name="Eng. Nourhan Tarek",
                    title="QA/QC Quality Manager",
                    department="Quality Assurance",
                    phone="+20 102 345 6789",
                    email="nourhan.qc@company.com",
                    reporting_manager="Eng. Sherif Mostafa",
                    skills="Concrete Testing, Non-Destructive Testing, Site Inspection Requests (SIR), NCR Resolution"
                ),
                StaffRecord(
                    full_name="Eng. Tarek Al-Banna",
                    title="Procurement & Materials Manager",
                    department="Supply Chain",
                    phone="+20 103 456 7890",
                    email="tarek.procurement@company.com",
                    reporting_manager="Eng. Yasser (Project Director)",
                    skills="BOQ Tracking, Supplier Negotiations, Rebar & Cement Contracts, MIR Tracking"
                ),
                StaffRecord(
                    full_name="Eng. Khaled Zaki",
                    title="MEP Project Engineer",
                    department="MEP Engineering",
                    phone="+20 104 567 8901",
                    email="khaled.mep@company.com",
                    reporting_manager="Eng. Sherif Mostafa",
                    skills="HVAC Risers, Firefighting Systems, LV Panels, Plumbing Drainage"
                ),
                StaffRecord(
                    full_name="Eng. Sara Hassan",
                    title="Structural Design & Shop Drawing Lead",
                    department="Technical Office",
                    phone="+20 105 678 9012",
                    email="sara.techoffice@company.com",
                    reporting_manager="Eng. Sherif Mostafa",
                    skills="AutoCAD, Revit Structure, RFI Resolution, Bar Bending Schedules (BBS)"
                ),
            ]
            for s in staff_members:
                session.add(s)
            session.commit()

        # 2. Schedule Activities
        existing_act = session.exec(select(ScheduleActivity).where(ScheduleActivity.activity_id == "ACT-1010")).first()
        if not existing_act:
            activities = [
                ScheduleActivity(
                    activity_id="ACT-1010",
                    name="Raft Foundation Concrete Pouring Zone B",
                    wbs="1.02.01 Substructure / Foundation",
                    start_date="2026-10-01",
                    finish_date="2026-10-06",
                    planned_value=120000.0,
                    earned_value=115000.0,
                    actual_cost=118000.0,
                    predecessors="ACT-1005 (Excavation & Blinding)",
                    assigned_team="Arab Contractors & ReadyMix Team",
                    status="In Progress",
                    is_critical_path=True,
                    float_days=0
                ),
                ScheduleActivity(
                    activity_id="ACT-1020",
                    name="Core Wall Reinforcement Steel Fixing Floor 1",
                    wbs="1.03.01 Superstructure / Vertical Elements",
                    start_date="2026-10-04",
                    finish_date="2026-10-12",
                    planned_value=85000.0,
                    earned_value=80000.0,
                    actual_cost=82000.0,
                    predecessors="ACT-1010",
                    assigned_team="Steel Rebar Subcontractor Team 3",
                    status="In Progress",
                    is_critical_path=True,
                    float_days=0
                ),
                ScheduleActivity(
                    activity_id="ACT-1030",
                    name="Basement 2 Waterproofing Membrane Application",
                    wbs="1.02.04 Substructure / Protection",
                    start_date="2026-09-28",
                    finish_date="2026-10-04",
                    planned_value=45000.0,
                    earned_value=45000.0,
                    actual_cost=42000.0,
                    predecessors="ACT-1008",
                    assigned_team="Modern Waterproofing Specialists",
                    status="Completed",
                    is_critical_path=False,
                    float_days=5
                ),
                ScheduleActivity(
                    activity_id="ACT-1040",
                    name="MEP Chilled Water Vertical Riser Installation",
                    wbs="2.01.03 MEP / HVAC",
                    start_date="2026-10-04",
                    finish_date="2026-10-18",
                    planned_value=95000.0,
                    earned_value=70000.0,
                    actual_cost=74000.0,
                    predecessors="ACT-1015",
                    assigned_team="Electro-Mechanical Engineering Team A",
                    status="In Progress",
                    is_critical_path=False,
                    float_days=3
                ),
                ScheduleActivity(
                    activity_id="ACT-1050",
                    name="Tower Crane 2 Jacking & Extension (Stage 1)",
                    wbs="0.04.02 Site Logistics / Plant & Equipment",
                    start_date="2026-10-05",
                    finish_date="2026-10-07",
                    planned_value=30000.0,
                    earned_value=0.0,
                    actual_cost=0.0,
                    predecessors="ACT-1020",
                    assigned_team="Heavy Lifting Plant Division",
                    status="Not Started",
                    is_critical_path=True,
                    float_days=0
                ),
                ScheduleActivity(
                    activity_id="ACT-1060",
                    name="Electrical Cable Tray 1st Fix Floor 2",
                    wbs="2.02.01 MEP / Electrical",
                    start_date="2026-10-04",
                    finish_date="2026-10-14",
                    planned_value=50000.0,
                    earned_value=40000.0,
                    actual_cost=41000.0,
                    predecessors="ACT-1030",
                    assigned_team="PowerTech Electrical Subcontractors",
                    status="In Progress",
                    is_critical_path=False,
                    float_days=8
                ),
                ScheduleActivity(
                    activity_id="ACT-1070",
                    name="Structural Steel Canopy Fabrication Zone D",
                    wbs="1.04.01 Superstructure / Steelwork",
                    start_date="2026-10-10",
                    finish_date="2026-10-25",
                    planned_value=65000.0,
                    earned_value=20000.0,
                    actual_cost=22000.0,
                    predecessors="ACT-1020",
                    assigned_team="Zamil Structural Steel Co.",
                    status="In Progress",
                    is_critical_path=False,
                    float_days=4
                )
            ]
            for a in activities:
                session.add(a)
            session.commit()

        # 3. Materials Logs
        existing_mat = session.exec(select(MaterialLogRecord)).first()
        if not existing_mat:
            materials = [
                MaterialLogRecord(
                    material_description="Ready-Mix Concrete C50 Silica Fume (Zone B Raft)",
                    delivery_date="2026-10-04",
                    delivery_note_number="DN-2026-8812",
                    quantity=450.0,
                    unit="Cubic Meters (m3)",
                    supplier="CEMEX Egypt ReadyMix",
                    inspection_status="Passed",
                    notes="Slump test 180mm passed, temperature 27C, 12 cube samples collected by QC."
                ),
                MaterialLogRecord(
                    material_description="Deformed High-Tensile Steel Rebar Grade 60 (32mm & 25mm)",
                    delivery_date="2026-10-03",
                    delivery_note_number="DN-2026-8805",
                    quantity=120.0,
                    unit="Tons",
                    supplier="Ezz Steel Industries",
                    inspection_status="Passed",
                    notes="Mill test certificates verified by Eng. Nourhan Tarek. Tensile yield strength confirmed."
                ),
                MaterialLogRecord(
                    material_description="Galvanized Sheet Metal Ductwork (0.8mm & 1.0mm)",
                    delivery_date="2026-10-04",
                    delivery_note_number="DN-2026-8819",
                    quantity=85.0,
                    unit="Square Meters (m2)",
                    supplier="Cairo Air Duct Fabricators",
                    inspection_status="Pending",
                    notes="Delivered to Zone C laydown area. Site Inspection Request (SIR) scheduled for QA/QC."
                ),
            ]
            for m in materials:
                session.add(m)
            session.commit()

        # 4. QA/QC: NCRs & MIRs
        existing_ncr = session.exec(select(NCRRecord)).first()
        if not existing_ncr:
            ncrs = [
                NCRRecord(
                    ncr_number="NCR-STR-2026-004",
                    title="Concrete Cover Spacers Displacement on Core Wall Zone 1",
                    description="Insufficient concrete cover observed on western face rebar cage (observed 25mm instead of 50mm specified).",
                    root_cause="Improper spacer tying during rapid rebar installation shift.",
                    corrective_action="Subcontractor instructed to replace plastic chairs with heavy-duty concrete spacer blocks at 600mm centers.",
                    severity="Major",
                    status="Under Review",
                    assigned_engineer="Eng. Sherif Mostafa",
                    issued_date="2026-10-03",
                    target_closure_date="2026-10-06"
                )
            ]
            for n in ncrs:
                session.add(n)
            session.commit()

        existing_mir = session.exec(select(MIRRecord)).first()
        if not existing_mir:
            mirs = [
                MIRRecord(
                    mir_number="MIR-CIV-2026-112",
                    material_name="CEMEX Ready-Mix Concrete C50 Silica Fume",
                    supplier="CEMEX Egypt",
                    boq_item_ref="BOQ-SEC-02.04",
                    quantity_inspected=450.0,
                    unit="m3",
                    status="Approved",
                    inspector="Eng. Nourhan Tarek (QA/QC)",
                    inspection_date="2026-10-04",
                    comments="All batch plant delivery tickets and slump tests fully compliant."
                ),
                MIRRecord(
                    mir_number="MIR-MEP-2026-089",
                    material_name="Galvanized Sheet Metal Ducts 1.0mm",
                    supplier="Cairo Air Duct Fabricators",
                    boq_item_ref="BOQ-SEC-04.12",
                    quantity_inspected=85.0,
                    unit="m2",
                    status="Under Inspection",
                    inspector="Eng. Nourhan Tarek (QA/QC)",
                    inspection_date="2026-10-04",
                    comments="Physical thickness gauge measurement pending."
                )
            ]
            for m in mirs:
                session.add(m)
            session.commit()

        # 5. Site Management: Daily Site Progress Report (DSR)
        existing_dsr = session.exec(select(DailySiteReport)).first()
        if not existing_dsr:
            dsr = DailySiteReport(
                report_date="2026-10-04",
                weather="Sunny 28°C",
                total_manpower=185,
                work_summary="Completed 450 m3 continuous raft pouring at Zone B. Core wall steel fixing ongoing for Floor 1. Basement 2 waterproofing inspection signed off by consultant.",
                critical_issues="Tower Crane 2 jacking scheduled for night shift to prevent site congestion.",
                safety_incidents=0,
                submitted_by="Eng. Sherif Mostafa (Site Manager)"
            )
            session.add(dsr)
            session.commit()

        # 6. FIDIC Claims & EOT Initial Data
        existing_claim = session.exec(select(ContractClaim)).first()
        if not existing_claim:
            claims = [
                ContractClaim(
                    claim_id="CLM-2026-001",
                    project_id="PRJ-01",
                    title="EOT Claim: Late Consultant Review of Basement Structural Shop Drawings",
                    claim_type="EOT_AND_COST",
                    fidic_clause_ref="FIDIC Red Book Sub-Clause 20.1 & 8.4(b)",
                    delay_days_claimed=18,
                    cost_claimed=45000.0,
                    status="Submitted",
                    cause_of_delay="Delayed approval of Raft foundation reinforcement shop drawings by 24 calendar days beyond contractual turnaround.",
                    responsible_party="Employer / Engineer",
                    narrative_letter="Formal Notice of Claim under FIDIC Sub-Clause 20.1 submitted regarding delayed drawings.",
                    submitted_date="2026-09-20"
                )
            ]
            for c in claims:
                session.add(c)
            session.commit()

        # 7. Variation Orders (VO Log)
        existing_vo = session.exec(select(VariationOrder)).first()
        if not existing_vo:
            vos = [
                VariationOrder(
                    vo_id="VO-001",
                    project_id="PRJ-01",
                    vo_number="VO-STR-01",
                    title="Additional High-Strength Shear Links in Core Wall Zone",
                    description="Consultant instruction to upgrade shear links from 10mm to 12mm high-tensile steel.",
                    cost_impact=28500.0,
                    schedule_days_impact=3,
                    status="Approved",
                    requested_by="Dar Al-Handasah Consultants",
                    approved_amount=28500.0
                ),
                VariationOrder(
                    vo_id="VO-002",
                    project_id="PRJ-01",
                    vo_number="VO-MEP-02",
                    title="HVAC Chilled Water Bypass Routing Adjustment",
                    description="Owner request to re-route chilled water risers around the central electrical substation.",
                    cost_impact=62000.0,
                    schedule_days_impact=7,
                    status="Under Evaluation",
                    requested_by="Owner Project Director",
                    approved_amount=0.0
                )
            ]
            for v in vos:
                session.add(v)
            session.commit()

        # 8. Interim Payment Certificates (IPC)
        existing_ipc = session.exec(select(PaymentCertificate)).first()
        if not existing_ipc:
            ipcs = [
                PaymentCertificate(
                    ipc_id="IPC-01",
                    project_id="PRJ-01",
                    certificate_number="IPC-01-SEP-2026",
                    period_month="September 2026",
                    gross_work_done=650000.0,
                    materials_on_site=120000.0,
                    advance_payment_recovery=65000.0,
                    retention_deduction=38500.0,
                    net_payable_amount=666500.0,
                    status="Paid",
                    issue_date="2026-09-25",
                    payment_due_date="2026-10-25"
                ),
                PaymentCertificate(
                    ipc_id="IPC-02",
                    project_id="PRJ-01",
                    certificate_number="IPC-02-OCT-2026",
                    period_month="October 2026",
                    gross_work_done=780000.0,
                    materials_on_site=145000.0,
                    advance_payment_recovery=78000.0,
                    retention_deduction=46250.0,
                    net_payable_amount=800750.0,
                    status="Certified",
                    issue_date="2026-10-04",
                    payment_due_date="2026-11-04"
                )
            ]
            for ipc in ipcs:
                session.add(ipc)
            session.commit()

        print("Initial Enterprise Construction data seeded successfully.")
