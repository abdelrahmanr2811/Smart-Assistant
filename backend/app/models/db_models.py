from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

# 0. Multi-Project Management
class Project(SQLModel, table=True):
    __tablename__ = "projects"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: str = Field(unique=True, index=True) # e.g. "PRJ-01"
    name: str = Field(index=True)
    code: str = Field(unique=True, index=True)
    client_name: str = Field(default="Al-Narges Real Estate Development")
    consultant_name: str = Field(default="Dar Al-Handasah Consultants")
    contractor_name: str = Field(default="Hassan Allam Construction")
    baseline_start: str = Field(default="2026-01-15")
    baseline_finish: str = Field(default="2027-06-30")
    total_budget: float = Field(default=15000000.0)
    currency: str = Field(default="SAR")
    latitude: float = Field(default=30.0270) # GIS Latitude
    longitude: float = Field(default=31.4913) # GIS Longitude
    location_name: str = Field(default="New Cairo, Egypt")
    health_status: str = Field(default="WATCH", description="ON_TRACK, WATCH, CRITICAL")
    is_active: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utc_now)

# 1. Security & RBAC User Management
class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str
    role: str = Field(default="SITE_MANAGER", description="PROJECT_DIRECTOR, SITE_MANAGER, PLANNING_ENGINEER, QA_QC_MANAGER, PROCUREMENT_OFFICER, VIEWER")
    phone: str = Field(default="+966 50 123 4567")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now)

# 2. Immutable Enterprise Audit Logs
class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    log_id: str = Field(unique=True, index=True)
    user_id: str = Field(index=True)
    user_email: str
    action_type: str = Field(index=True, description="CREATE, UPDATE, APPROVE, REJECT, DELETE, QUERY, AI_PROMPT")
    entity_name: str = Field(index=True, description="SCHEDULE, MATERIAL, EMAIL_DISPATCH, NCR, MIR, RAG_DOCUMENT, PROJECT")
    entity_id: Optional[str] = None
    ip_address: Optional[str] = None
    details_json: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)

# 3. Chat Conversations & Sessions
class ChatSession(SQLModel, table=True):
    __tablename__ = "chat_sessions"
    
    session_id: str = Field(default=None, primary_key=True)
    title: str = Field(default="New PM Conversation")
    project_id: str = Field(default="PRJ-01", index=True)
    user_id: Optional[str] = Field(default="usr_admin_01", index=True)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str = Field(index=True)
    role: str = Field(description="'user', 'assistant', 'system'")
    content: str
    metadata_json: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=utc_now)

class TeamChatMessage(SQLModel, table=True):
    __tablename__ = "team_chat_messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    channel_id: str = Field(default="general", index=True)
    sender_name: str = Field(default="Engr. Team Member")
    sender_email: Optional[str] = Field(default="director@company.com")
    content: str
    created_at: datetime = Field(default_factory=utc_now)

class PendingAction(SQLModel, table=True):
    __tablename__ = "pending_actions"
    
    action_id: str = Field(default=None, primary_key=True)
    session_id: Optional[str] = Field(default=None, index=True)
    project_id: str = Field(default="PRJ-01", index=True)
    tool_name: str
    parameters_json: str
    status: str = Field(default="PENDING_CONFIRMATION", description="PENDING_CONFIRMATION, APPROVED, REJECTED, EXECUTED, FAILED")
    preview_title: Optional[str] = None
    result_json: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

# 4. Staff & Resources
class StaffRecord(SQLModel, table=True):
    __tablename__ = "staff_records"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: str = Field(default="PRJ-01", index=True)
    full_name: str = Field(index=True)
    title: str
    department: str = Field(index=True)
    phone: str
    email: str
    reporting_manager: Optional[str] = None
    skills: Optional[str] = None

# 5. Project Schedule & EVM
class ScheduleActivity(SQLModel, table=True):
    __tablename__ = "schedule_activities"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: str = Field(default="PRJ-01", index=True)
    activity_id: str = Field(index=True, unique=True)
    name: str
    wbs: str = Field(index=True)
    start_date: str = Field(index=True)  # YYYY-MM-DD
    finish_date: str = Field(index=True) # YYYY-MM-DD
    planned_value: float = Field(default=0.0)
    earned_value: float = Field(default=0.0)
    actual_cost: float = Field(default=0.0)
    predecessors: Optional[str] = None
    assigned_team: str
    status: str = Field(default="In Progress")
    is_critical_path: bool = Field(default=False)
    float_days: int = Field(default=0)

# 6. Materials & Supply Chain Logs
class MaterialLogRecord(SQLModel, table=True):
    __tablename__ = "material_logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: str = Field(default="PRJ-01", index=True)
    material_description: str = Field(index=True)
    delivery_date: str = Field(index=True) # YYYY-MM-DD
    delivery_note_number: str = Field(unique=True)
    quantity: float
    unit: str
    supplier: str = Field(index=True)
    inspection_status: str = Field(default="Pending") # Passed, Pending, Rejected
    notes: Optional[str] = None

# 7. QA/QC: NCR (Non-Conformance Reports) & MIR (Material Inspection Requests)
class NCRRecord(SQLModel, table=True):
    __tablename__ = "ncr_records"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: str = Field(default="PRJ-01", index=True)
    ncr_number: str = Field(unique=True, index=True) # e.g. NCR-STR-2026-004
    title: str
    description: str
    root_cause: Optional[str] = None
    corrective_action: Optional[str] = None
    severity: str = Field(default="Major") # Critical, Major, Minor
    status: str = Field(default="Open") # Open, Under Review, Closed
    assigned_engineer: str
    issued_date: str
    target_closure_date: str

class MIRRecord(SQLModel, table=True):
    __tablename__ = "mir_records"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: str = Field(default="PRJ-01", index=True)
    mir_number: str = Field(unique=True, index=True) # e.g. MIR-MEP-2026-089
    material_name: str
    supplier: str
    boq_item_ref: str
    quantity_inspected: float
    unit: str
    status: str = Field(default="Approved") # Approved, Approved as Noted, Rejected
    inspector: str
    inspection_date: str
    comments: Optional[str] = None

# 8. Site Management: Daily Site Progress Reports (DSR) & Equipment
class DailySiteReport(SQLModel, table=True):
    __tablename__ = "daily_site_reports"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: str = Field(default="PRJ-01", index=True)
    report_date: str = Field(unique=True, index=True) # YYYY-MM-DD
    weather: str = Field(default="Sunny 28°C")
    total_manpower: int = Field(default=180)
    work_summary: str
    critical_issues: Optional[str] = None
    safety_incidents: int = Field(default=0)
    submitted_by: str

# 9. Knowledge Base & RAG Documents
class ProjectDocument(SQLModel, table=True):
    __tablename__ = "project_documents"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: str = Field(default="PRJ-01", index=True)
    document_id: str = Field(unique=True, index=True)
    filename: str
    file_format: str = Field(default="CSV") # XER, XML, MPP, XLSX, CSV, PDF, TXT
    category: str
    file_path: str
    file_size_bytes: int
    chunks_indexed: int
    uploaded_at: datetime = Field(default_factory=utc_now)

# 10. Early-Warning Anomaly Alerts
class EarlyWarningAlert(SQLModel, table=True):
    __tablename__ = "early_warning_alerts"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    alert_id: str = Field(unique=True, index=True)
    project_id: str = Field(default="PRJ-01", index=True)
    severity: str = Field(default="WARNING", description="CRITICAL, WARNING, INFO")
    category: str = Field(description="SCHEDULE_SPI, COST_CPI, CRITICAL_PATH, QA_QC_NCR, MATERIAL_SHORTAGE")
    title: str
    description: str
    metrics_snapshot: Optional[str] = None
    recommended_action: str
    is_acknowledged: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utc_now)

# 11. FIDIC Claims & Extension of Time (EOT)
class ContractClaim(SQLModel, table=True):
    __tablename__ = "contract_claims"

    id: Optional[int] = Field(default=None, primary_key=True)
    claim_id: str = Field(unique=True, index=True) # e.g. "CLM-2026-001"
    project_id: str = Field(default="PRJ-01", index=True)
    title: str
    claim_type: str = Field(default="EOT_AND_COST", description="EOT_ONLY, COST_ONLY, EOT_AND_COST, FIDIC_DISRUPTION")
    fidic_clause_ref: str = Field(default="FIDIC Sub-Clause 20.1 & 8.4")
    delay_days_claimed: int = Field(default=0)
    cost_claimed: float = Field(default=0.0)
    status: str = Field(default="Draft", description="Draft, Submitted, Under Review, Approved, Rejected")
    cause_of_delay: str
    responsible_party: str = Field(default="Employer / Engineer", description="Employer / Engineer, Contractor, Force Majeure")
    narrative_letter: Optional[str] = None
    submitted_date: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)

# 12. Variation Orders (VO Log)
class VariationOrder(SQLModel, table=True):
    __tablename__ = "variation_orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    vo_id: str = Field(unique=True, index=True) # e.g. "VO-001"
    project_id: str = Field(default="PRJ-01", index=True)
    vo_number: str = Field(unique=True, index=True)
    title: str
    description: str
    cost_impact: float = Field(default=0.0)
    schedule_days_impact: int = Field(default=0)
    status: str = Field(default="Under Evaluation", description="Requested, Under Evaluation, Approved, Rejected")
    requested_by: str = Field(default="Owner Representative")
    approved_amount: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=utc_now)

# 13. Financial Cash Flow & Interim Payment Certificates (IPC)
class PaymentCertificate(SQLModel, table=True):
    __tablename__ = "payment_certificates"

    id: Optional[int] = Field(default=None, primary_key=True)
    ipc_id: str = Field(unique=True, index=True) # e.g. "IPC-01"
    project_id: str = Field(default="PRJ-01", index=True)
    certificate_number: str = Field(unique=True, index=True)
    period_month: str = Field(index=True) # e.g. "October 2026"
    gross_work_done: float = Field(default=0.0)
    materials_on_site: float = Field(default=0.0)
    advance_payment_recovery: float = Field(default=0.0)
    retention_deduction: float = Field(default=0.0)
    net_payable_amount: float = Field(default=0.0)
    status: str = Field(default="Draft", description="Draft, Certified, Paid")
    issue_date: str = Field(default="2026-10-05")
    payment_due_date: str = Field(default="2026-11-05")
    created_at: datetime = Field(default_factory=utc_now)
