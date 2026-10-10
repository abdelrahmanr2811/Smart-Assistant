import uuid
import json
from typing import Optional, Dict, Any
from email.message import EmailMessage
import aiosmtplib
from langchain_core.tools import tool
from sqlmodel import Session
from app.config import settings
from app.core.database import engine
from app.models.db_models import PendingAction

@tool
def send_notification_email(
    recipient_email: str,
    subject: str,
    message: str
) -> str:
    """
    Drafts a project notification email for site engineers or stakeholders.
    Enforces Human-In-The-Loop (HITL) strictly on the backend.
    This tool CANNOT send emails directly. It only creates a PendingAction record
    that requires explicit manual approval via the /api/v1/actions/approve endpoint.
    """
    action_id = f"act_mail_{uuid.uuid4().hex[:8]}"
    params = {
        "to": recipient_email.strip(),
        "subject": subject.strip(),
        "body": message.strip()
    }

    # Strict backend HITL: always write pending record to database
    with Session(engine) as session:
        pending = PendingAction(
            action_id=action_id,
            tool_name="send_notification_email",
            parameters_json=json.dumps(params, ensure_ascii=False),
            status="PENDING_CONFIRMATION",
            preview_title=f"Send Email: {subject[:40]}..."
        )
        session.add(pending)
        session.commit()

    action_payload = {
        "type": "ACTION_REQUIRED",
        "action_id": action_id,
        "tool": "send_notification_email",
        "parameters": params,
        "preview_title": f"📧 Email Dispatch Request to {recipient_email}",
        "preview_details": {
            "Recipient": recipient_email,
            "Subject": subject,
            "Preview": message[:120] + ("..." if len(message) > 120 else "")
        }
    }
    return json.dumps(action_payload, ensure_ascii=False)

async def execute_send_email(to_email: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Executes email dispatch ONLY when called by the authenticated /actions/approve route.
    """
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        return {
            "success": True,
            "mode": "simulation",
            "message": f"[Simulation Mode] Email '{subject}' approved and logged to {to_email}.",
            "details": {"to": to_email, "subject": subject, "body_length": len(body)}
        }

    try:
        msg = EmailMessage()
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            start_tls=settings.SMTP_USE_TLS,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD
        )
        return {
            "success": True,
            "mode": "live_smtp",
            "message": f"Email successfully sent to {to_email} via SMTP."
        }
    except Exception as e:
        return {
            "success": False,
            "mode": "error",
            "message": f"Failed to send email to {to_email}: {str(e)}"
        }
