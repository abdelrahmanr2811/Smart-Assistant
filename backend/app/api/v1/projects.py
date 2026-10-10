import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel

from app.core.database import get_session
from app.models.db_models import Project, ScheduleActivity, NCRRecord, MIRRecord, MaterialLogRecord

router = APIRouter(prefix="/projects", tags=["Projects Management"])

class ProjectCreatePayload(BaseModel):
    name: str
    code: str
    client_name: Optional[str] = "Owner / Client"
    consultant_name: Optional[str] = "Consultant Engineering Firm"
    contractor_name: Optional[str] = "Main Contractor"
    baseline_start: Optional[str] = "2026-01-01"
    baseline_finish: Optional[str] = "2027-12-31"
    total_budget: Optional[float] = 10000000.0
    currency: Optional[str] = "SAR"

class ProjectResponse(BaseModel):
    project_id: str
    code: str
    name: str
    client_name: str
    consultant_name: str
    contractor_name: str
    baseline_start: str
    baseline_finish: str
    total_budget: float
    currency: str
    is_active: bool
    activities_count: int = 0
    open_ncrs_count: int = 0

@router.get("", response_model=List[ProjectResponse])
def list_projects(session: Session = Depends(get_session)):
    projects = session.exec(select(Project).order_by(Project.id.asc())).all()
    res = []
    for p in projects:
        act_cnt = len(session.exec(select(ScheduleActivity).where(ScheduleActivity.project_id == p.project_id)).all())
        ncr_cnt = len(session.exec(select(NCRRecord).where(NCRRecord.project_id == p.project_id, NCRRecord.status == "Open")).all())
        res.append(ProjectResponse(
            project_id=p.project_id,
            code=p.code,
            name=p.name,
            client_name=p.client_name,
            consultant_name=p.consultant_name,
            contractor_name=p.contractor_name,
            baseline_start=p.baseline_start,
            baseline_finish=p.baseline_finish,
            total_budget=p.total_budget,
            currency=p.currency,
            is_active=p.is_active,
            activities_count=act_cnt,
            open_ncrs_count=ncr_cnt
        ))
    return res

@router.get("/active", response_model=ProjectResponse)
def get_active_project(session: Session = Depends(get_session)):
    prj = session.exec(select(Project).where(Project.is_active == True)).first()
    if not prj:
        prj = session.exec(select(Project)).first()
        if prj:
            prj.is_active = True
            session.add(prj)
            session.commit()
    if not prj:
        raise HTTPException(status_code=404, detail="No projects configured")
    
    act_cnt = len(session.exec(select(ScheduleActivity).where(ScheduleActivity.project_id == prj.project_id)).all())
    ncr_cnt = len(session.exec(select(NCRRecord).where(NCRRecord.project_id == prj.project_id, NCRRecord.status == "Open")).all())
    return ProjectResponse(
        project_id=prj.project_id,
        code=prj.code,
        name=prj.name,
        client_name=prj.client_name,
        consultant_name=prj.consultant_name,
        contractor_name=prj.contractor_name,
        baseline_start=prj.baseline_start,
        baseline_finish=prj.baseline_finish,
        total_budget=prj.total_budget,
        currency=prj.currency,
        is_active=True,
        activities_count=act_cnt,
        open_ncrs_count=ncr_cnt
    )

@router.post("/{project_id}/activate")
def activate_project(project_id: str, session: Session = Depends(get_session)):
    target = session.exec(select(Project).where(Project.project_id == project_id)).first()
    if not target:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    
    # Deactivate all others
    all_prjs = session.exec(select(Project)).all()
    for p in all_prjs:
        p.is_active = (p.project_id == project_id)
        session.add(p)
    session.commit()
    return {"status": "success", "active_project_id": project_id, "name": target.name}

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreatePayload, session: Session = Depends(get_session)):
    code_exists = session.exec(select(Project).where(Project.code == payload.code.upper().strip())).first()
    if code_exists:
        raise HTTPException(status_code=400, detail="Project with this code already exists")
    
    new_id = f"PRJ-{uuid.uuid4().hex[:6].upper()}"
    new_prj = Project(
        project_id=new_id,
        code=payload.code.upper().strip(),
        name=payload.name.strip(),
        client_name=payload.client_name,
        consultant_name=payload.consultant_name,
        contractor_name=payload.contractor_name,
        baseline_start=payload.baseline_start,
        baseline_finish=payload.baseline_finish,
        total_budget=payload.total_budget,
        currency=payload.currency,
        is_active=False
    )
    session.add(new_prj)
    session.commit()
    session.refresh(new_prj)
    
    return ProjectResponse(
        project_id=new_prj.project_id,
        code=new_prj.code,
        name=new_prj.name,
        client_name=new_prj.client_name,
        consultant_name=new_prj.consultant_name,
        contractor_name=new_prj.contractor_name,
        baseline_start=new_prj.baseline_start,
        baseline_finish=new_prj.baseline_finish,
        total_budget=new_prj.total_budget,
        currency=new_prj.currency,
        is_active=False,
        activities_count=0,
        open_ncrs_count=0
    )

@router.delete("/{project_id}")
def delete_project(project_id: str, session: Session = Depends(get_session)):
    target = session.exec(select(Project).where(Project.project_id == project_id)).first()
    if not target:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    
    all_prjs = session.exec(select(Project)).all()
    if len(all_prjs) <= 1:
        raise HTTPException(status_code=400, detail="Cannot delete the only remaining project in the portfolio")
    
    was_active = target.is_active
    
    # Delete associated activities
    acts = session.exec(select(ScheduleActivity).where(ScheduleActivity.project_id == project_id)).all()
    for a in acts:
        session.delete(a)
        
    session.delete(target)
    session.commit()
    
    # If deleted project was active, activate another one
    if was_active:
        remaining = session.exec(select(Project)).first()
        if remaining:
            remaining.is_active = True
            session.add(remaining)
            session.commit()
            
    return {"status": "success", "message": f"Project '{target.name}' deleted successfully"}

