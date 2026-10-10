from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class ActionRequiredPayload(BaseModel):
    type: str = "ACTION_REQUIRED"
    action_id: str
    tool: str
    parameters: Dict[str, Any]
    preview_title: Optional[str] = None
    preview_details: Optional[Dict[str, Any]] = None

class ChatMessageRequest(BaseModel):
    message: str = Field(..., description="User message or instruction")
    session_id: Optional[str] = Field(default=None, description="Session ID for multi-turn history")
    provider: Optional[str] = Field(default=None, description="Override LLM provider (openai/gemini)")
    project_id: Optional[str] = Field(default=None, description="Active selected project ID")

class ChatMessageResponse(BaseModel):
    session_id: str
    response: str
    action_required: Optional[ActionRequiredPayload] = None
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ActionApprovalRequest(BaseModel):
    action_id: str
    parameters: Optional[Dict[str, Any]] = Field(default=None, description="Optional edited parameters before execution")

class ActionApprovalResponse(BaseModel):
    action_id: str
    tool: str
    status: str  # "EXECUTED", "REJECTED", "FAILED"
    result: Optional[Dict[str, Any]] = None
    message: str

class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    category: str  # "Staff", "Schedule", "Materials", "Meeting", "General"
    file_size_bytes: int
    chunks_indexed: int
    status: str
    message: str

class StaffMemberSchema(BaseModel):
    id: Optional[int] = None
    full_name: str
    title: str
    department: str
    phone: str
    email: str
    reporting_manager: Optional[str] = None
    skills: Optional[str] = None

class ScheduleKPISchema(BaseModel):
    project_name: str
    period: str
    planned_value: float  # PV
    earned_value: float   # EV
    actual_cost: float    # AC
    schedule_performance_index: float  # SPI = EV / PV
    cost_performance_index: float      # CPI = EV / AC
    schedule_variance: float           # SV = EV - PV
    cost_variance: float               # CV = EV - AC
    schedule_status: str               # "Ahead of Schedule", "On Track", "Behind Schedule"
    cost_status: str                   # "Under Budget", "On Budget", "Over Budget"
    commentary: str

class DailyActivitySchema(BaseModel):
    activity_id: str
    name: str
    wbs: str
    start_date: str
    finish_date: str
    assigned_contractor: str
    predecessors: Optional[str] = None
    status: str  # "In Progress", "Not Started", "Completed", "Critical"

class MaterialLogSchema(BaseModel):
    id: Optional[int] = None
    material_description: str
    delivery_date: str
    delivery_note_number: str
    quantity: float
    unit: str
    supplier: str
    inspection_status: str  # "Passed", "Pending", "Rejected"
    notes: Optional[str] = None

class VoiceTranscribeResponse(BaseModel):
    transcript: str
    detected_language: str
    duration_seconds: Optional[float] = None
    execution_result: Optional[ChatMessageResponse] = None

class TeamChatMessageCreateSchema(BaseModel):
    channel_id: str = Field(default="general")
    sender_name: str = Field(default="Engr. Team Member")
    sender_email: Optional[str] = Field(default="director@company.com")
    content: str

