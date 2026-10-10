from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Any, Optional
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.db_models import ChatSession, ChatMessage, TeamChatMessage
from app.models.schemas import ChatMessageRequest, ChatMessageResponse, ActionRequiredPayload, TeamChatMessageCreateSchema
from app.core.agent import agent_orchestrator
import json

router = APIRouter(prefix="/chat", tags=["Chat & Agent"])

@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(request: ChatMessageRequest):
    """
    Sends a message to the Smart Assistant agent.
    Returns agent text response and any action payloads requiring confirmation.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    response = await agent_orchestrator.process_message(
        user_message=request.message,
        session_id=request.session_id,
        provider_override=request.provider,
        project_id=request.project_id
    )
    return response

@router.get("/sessions", response_model=List[Dict[str, Any]])
def get_chat_sessions(db: Session = Depends(get_session)):
    """Lists all active chat sessions."""
    sessions = db.exec(select(ChatSession).order_by(ChatSession.updated_at.desc())).all()
    return [
        {
            "session_id": s.session_id,
            "title": s.title,
            "created_at": s.created_at.isoformat(),
            "updated_at": s.updated_at.isoformat()
        }
        for s in sessions
    ]

@router.get("/sessions/{session_id}/messages", response_model=List[Dict[str, Any]])
def get_session_messages(session_id: str, db: Session = Depends(get_session)):
    """Retrieves full message history for a specific chat session."""
    messages = db.exec(
        select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc())
    ).all()
    
    formatted = []
    for m in messages:
        action_payload = None
        if m.metadata_json:
            try:
                meta = json.loads(m.metadata_json)
                action_payload = meta.get("action_required")
            except Exception:
                pass
        
        formatted.append({
            "id": m.id,
            "session_id": m.session_id,
            "role": m.role,
            "content": m.content,
            "action_required": action_payload,
            "created_at": m.created_at.isoformat()
        })
    return formatted

@router.delete("/sessions/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_session)):
    """Deletes a chat session and its associated messages."""
    session = db.get(ChatSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    
    messages = db.exec(select(ChatMessage).where(ChatMessage.session_id == session_id)).all()
    for m in messages:
        db.delete(m)
    db.delete(session)
    db.commit()
    return {"message": f"Session {session_id} deleted successfully."}

@router.get("/team/messages", response_model=List[Dict[str, Any]])
def get_team_messages(channel_id: str = Query(default="general"), db: Session = Depends(get_session)):
    """Retrieves multi-user human team chat messages for a channel."""
    messages = db.exec(
        select(TeamChatMessage).where(TeamChatMessage.channel_id == channel_id).order_by(TeamChatMessage.created_at.asc())
    ).all()
    return [
        {
            "id": m.id,
            "channel_id": m.channel_id,
            "sender_name": m.sender_name,
            "sender_email": m.sender_email,
            "content": m.content,
            "created_at": m.created_at.isoformat()
        }
        for m in messages
    ]

@router.post("/team/messages", response_model=Dict[str, Any])
def send_team_message(msg: TeamChatMessageCreateSchema, db: Session = Depends(get_session)):
    """Posts a new team chat message for multi-user collaboration."""
    if not msg.content.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty.")
    
    new_msg = TeamChatMessage(
        channel_id=msg.channel_id,
        sender_name=msg.sender_name,
        sender_email=msg.sender_email,
        content=msg.content
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return {
        "id": new_msg.id,
        "channel_id": new_msg.channel_id,
        "sender_name": new_msg.sender_name,
        "sender_email": new_msg.sender_email,
        "content": new_msg.content,
        "created_at": new_msg.created_at.isoformat()
    }

