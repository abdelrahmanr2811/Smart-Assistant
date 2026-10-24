from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class ChatMessageRequest(BaseModel):
    session_id: Optional[str] = Field(default=None, description="Unique customer conversation session ID")
    customer_name: Optional[str] = Field(default="Guest", description="Name of the customer")
    message: str = Field(..., min_length=1, description="Message text sent by the customer")

class ChatMessageResponse(BaseModel):
    session_id: str
    reply: str
    intent: str
    needs_human_escalation: bool = False
    confidence: float = 0.95
    timestamp: datetime = Field(default_factory=utc_now)

class FAQItem(BaseModel):
    id: Optional[int] = None
    question: str
    answer: str
    category: str = "General"
    keywords: List[str] = []

class AnalyticsSummary(BaseModel):
    total_conversations: int
    resolution_rate_percent: float
    human_escalation_rate_percent: float
    average_response_time_seconds: float
    top_intents: List[str]
