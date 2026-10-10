import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.security import get_current_user, require_roles, UserRole
from app.models.db_models import PendingAction
from app.models.schemas import ActionApprovalRequest, ActionApprovalResponse
from app.tools.email_tool import execute_send_email
from app.tools.calendar_tool import execute_calendar_booking

router = APIRouter(prefix="/actions", tags=["Human In The Loop (HITL) Actions"])

@router.get("/pending", response_model=List[Dict[str, Any]])
def list_pending_actions(
    db: Session = Depends(get_session),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Lists all actions currently awaiting Human-In-The-Loop approval (Authenticated)."""
    actions = db.exec(
        select(PendingAction).where(PendingAction.status == "PENDING_CONFIRMATION").order_by(PendingAction.created_at.desc())
    ).all()
    
    results = []
    for a in actions:
        params = {}
        try:
            params = json.loads(a.parameters_json)
        except Exception:
            pass
        
        results.append({
            "action_id": a.action_id,
            "session_id": a.session_id,
            "tool_name": a.tool_name,
            "preview_title": a.preview_title,
            "parameters": params,
            "status": a.status,
            "created_at": a.created_at.isoformat()
        })
    return results

@router.post("/approve", response_model=ActionApprovalResponse)
async def approve_action(
    payload: ActionApprovalRequest,
    db: Session = Depends(get_session),
    current_user: Dict[str, Any] = Depends(require_roles([
        UserRole.PROJECT_DIRECTOR,
        UserRole.SITE_MANAGER,
        UserRole.PLANNING_ENGINEER,
        UserRole.QA_QC_MANAGER,
        UserRole.FIELD_ENGINEER
    ]))
):
    """
    Approves and executes a pending action (e.g. Email dispatch or Calendar invite).
    Requires authorized engineer role (Viewers cannot approve).
    """
    action = db.get(PendingAction, payload.action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found.")
    
    if action.status not in ["PENDING_CONFIRMATION", "FAILED"]:
        raise HTTPException(status_code=400, detail=f"Action is already {action.status}.")

    # Parse stored parameters or use updated ones
    params = json.loads(action.parameters_json)
    if payload.parameters:
        params.update(payload.parameters)

    execution_result = {}
    success = False

    try:
        if action.tool_name == "send_notification_email":
            execution_result = await execute_send_email(
                to_email=params.get("to", ""),
                subject=params.get("subject", ""),
                body=params.get("body", "")
            )
            success = execution_result.get("success", True)
        elif action.tool_name == "schedule_meeting":
            execution_result = await execute_calendar_booking(params)
            success = execution_result.get("success", True)
        else:
            # Generic action execution
            execution_result = {"success": True, "message": f"Action {action.tool_name} executed successfully."}
            success = True

        action.status = "EXECUTED" if success else "FAILED"
        action.result_json = json.dumps(execution_result, ensure_ascii=False)
        action.updated_at = datetime.now(timezone.utc)
        db.add(action)
        db.commit()

        return ActionApprovalResponse(
            action_id=action.action_id,
            tool=action.tool_name,
            status=action.status,
            result=execution_result,
            message=execution_result.get("message", "Action successfully executed.")
        )
    except Exception as e:
        action.status = "FAILED"
        action.result_json = json.dumps({"error": str(e)})
        db.add(action)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Failed to execute action: {str(e)}")

@router.post("/reject", response_model=ActionApprovalResponse)
def reject_action(
    payload: ActionApprovalRequest,
    db: Session = Depends(get_session),
    current_user: Dict[str, Any] = Depends(require_roles([
        UserRole.PROJECT_DIRECTOR,
        UserRole.SITE_MANAGER,
        UserRole.PLANNING_ENGINEER,
        UserRole.QA_QC_MANAGER,
        UserRole.FIELD_ENGINEER
    ]))
):
    """Rejects/Cancels a pending action."""
    action = db.get(PendingAction, payload.action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found.")
    
    action.status = "REJECTED"
    action.updated_at = datetime.now(timezone.utc)
    db.add(action)
    db.commit()

    return ActionApprovalResponse(
        action_id=action.action_id,
        tool=action.tool_name,
        status="REJECTED",
        result={"rejected": True},
        message=f"Action '{action.tool_name}' was successfully cancelled by the user."
    )
