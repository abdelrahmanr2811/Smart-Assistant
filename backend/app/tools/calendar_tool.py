import uuid
import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from langchain_core.tools import tool
from sqlmodel import Session
from app.config import settings
from app.core.database import engine
from app.models.db_models import PendingAction

def generate_ics_calendar_content(title: str, start_iso: str, duration_minutes: int, location: str, attendees: List[str]) -> str:
    """Generates a valid standard RFC 5545 iCalendar (.ics) format."""
    now_str = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    try:
        dt = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
        start_str = dt.strftime('%Y%m%dT%H%M%SZ')
        end_str = (dt + timedelta(minutes=duration_minutes)).strftime('%Y%m%dT%H%M%SZ')
    except Exception:
        start_str = now_str
        end_str = now_str

    attendee_lines = "\r\n".join([f"ATTENDEE;CN={a}:mailto:{a}" for a in attendees]) if attendees else ""
    if attendee_lines:
        attendee_lines += "\r\n"

    return (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//Smart Assistant//Construction PM Controls//EN\r\n"
        "CALSCALE:GREGORIAN\r\n"
        "METHOD:REQUEST\r\n"
        "BEGIN:VEVENT\r\n"
        f"UID:{uuid.uuid4().hex}@smartassistant.local\r\n"
        f"DTSTAMP:{now_str}\r\n"
        f"DTSTART:{start_str}\r\n"
        f"DTEND:{end_str}\r\n"
        f"SUMMARY:{title}\r\n"
        f"LOCATION:{location}\r\n"
        f"{attendee_lines}"
        "STATUS:CONFIRMED\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )

@tool
def schedule_meeting(
    title: str,
    start_time_iso: str,
    duration_minutes: int = 45,
    attendees: Optional[List[str]] = None
) -> str:
    """
    Drafts a project coordination meeting invite (ICS Export Only).
    Enforces Human-In-The-Loop (HITL) strictly on the backend.
    This tool CANNOT finalize calendar events directly. It creates a PendingAction record
    that requires explicit manual approval via the /api/v1/actions/approve endpoint.
    """
    if attendees is None:
        attendees = []

    action_id = f"act_cal_{uuid.uuid4().hex[:8]}"
    
    try:
        start_dt = datetime.fromisoformat(start_time_iso.replace("Z", "+00:00"))
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        end_time_iso = end_dt.isoformat()
    except Exception:
        end_time_iso = "N/A"

    location = "Site Main Conference Room / Project Site Office"

    params = {
        "title": title,
        "start_time": start_time_iso,
        "end_time": end_time_iso,
        "duration_minutes": duration_minutes,
        "attendees": attendees,
        "location": location,
        "integration_mode": "ICS_EXPORT_ONLY"
    }

    # Strict backend HITL: always write pending record to database
    with Session(engine) as session:
        pending = PendingAction(
            action_id=action_id,
            tool_name="schedule_meeting",
            parameters_json=json.dumps(params, ensure_ascii=False),
            status="PENDING_CONFIRMATION",
            preview_title=f"Schedule Meeting: {title} (ICS Export Only)"
        )
        session.add(pending)
        session.commit()

    action_payload = {
        "type": "ACTION_REQUIRED",
        "action_id": action_id,
        "tool": "schedule_meeting",
        "parameters": params,
        "preview_title": f"📅 Meeting Invite: {title} (ICS Export Only)",
        "preview_details": {
            "Title": title,
            "Start Time": start_time_iso,
            "Duration": f"{duration_minutes} minutes",
            "Location": location,
            "Attendees": ", ".join(attendees) if attendees else "Project Team",
            "Export Mode": "iCalendar (.ics) RFC 5545 format"
        }
    }
    return json.dumps(action_payload, ensure_ascii=False)

async def execute_calendar_booking(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes calendar invite creation ONLY when called by the authenticated /actions/approve route.
    Generates standard .ics iCalendar file payload.
    """
    title = params.get("title", "Project Coordination Meeting")
    start_time = params.get("start_time", datetime.utcnow().isoformat())
    duration = int(params.get("duration_minutes", 45))
    location = params.get("location", "Site Main Office")
    attendees = params.get("attendees", [])

    ics_content = generate_ics_calendar_content(
        title=title,
        start_iso=start_time,
        duration_minutes=duration,
        location=location,
        attendees=attendees
    )

    return {
        "success": True,
        "integration_mode": "ICS_EXPORT_ONLY",
        "event_id": f"evt_{uuid.uuid4().hex[:10]}",
        "title": title,
        "ics_content": ics_content,
        "message": f"Calendar event '{title}' confirmed. Standard .ics iCalendar file generated successfully for Outlook / Google Calendar import."
    }
