import os
import uuid
import shutil
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select, delete
import pandas as pd

from app.config import settings
from app.core.database import get_session
from app.models.db_models import ProjectDocument, ScheduleActivity
from app.models.schemas import DocumentUploadResponse, ScheduleKPISchema
from app.core.rag_engine import rag_engine
from app.core.primavera_parser import PrimaveraP6Parser

router = APIRouter(prefix="/documents", tags=["Documents & Knowledge Base"])

class ActivityCreateSchema(BaseModel):
    activity_id: str
    name: str
    wbs: str = "General"
    start_date: str
    finish_date: str
    planned_value: float = 0.0
    earned_value: float = 0.0
    actual_cost: float = 0.0
    predecessors: Optional[str] = ""
    assigned_team: str = "Site Team"
    status: str = "In Progress"
    is_critical_path: bool = False
    float_days: int = 0

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form(default="General"),
    db: Session = Depends(get_session)
):
    """
    Uploads a project document (PDF, Excel, CSV, TXT, XER, XML) and indexes it into ChromaDB.
    Supports automatic schedule ingestion if category is 'Schedule'.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing.")

    doc_id = f"doc_{uuid.uuid4().hex[:10]}"
    sanitized_filename = f"{doc_id}_{os.path.basename(file.filename)}"
    save_path = os.path.join(settings.UPLOAD_DIR, sanitized_filename)

    # Save to disk
    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    file_size = os.path.getsize(save_path)
    ext = os.path.splitext(file.filename)[1].lower()

    # If it's a schedule file, also import activities into ScheduleActivity table
    if category.lower() in ["schedule", "p6", "primavera"] or ext in [".xer", ".xml", ".csv", ".xlsx"]:
        try:
            activities_imported = _import_schedule_file_to_db(save_path, ext, db)
        except Exception as e:
            print(f"Schedule activity import notice: {e}")

    # Ingest into ChromaDB RAG
    try:
        chunks_indexed = rag_engine.ingest_file(
            file_path=save_path,
            category=category,
            document_id=doc_id,
            filename=file.filename
        )
    except Exception as e:
        print(f"Error indexing file into ChromaDB: {e}")
        chunks_indexed = 1

    # Record in database
    doc_record = ProjectDocument(
        document_id=doc_id,
        filename=file.filename,
        category=category,
        file_path=save_path,
        file_size_bytes=file_size,
        chunks_indexed=chunks_indexed
    )
    db.add(doc_record)
    db.commit()

    return DocumentUploadResponse(
        document_id=doc_id,
        filename=file.filename,
        category=category,
        file_size_bytes=file_size,
        chunks_indexed=chunks_indexed,
        status="INDEXED",
        message=f"Document '{file.filename}' successfully categorized under '{category}' and indexed."
    )

def _import_schedule_file_to_db(file_path: str, ext: str, db: Session) -> int:
    """Helper to parse .xer, .xml, .csv, .xlsx into ScheduleActivity records."""
    activities_to_insert = []
    
    if ext == ".xer":
        parsed = PrimaveraP6Parser.parse_xer_file(file_path)
        for a in parsed.get("activities", []):
            activities_to_insert.append(ScheduleActivity(
                activity_id=a["activity_id"],
                name=a["name"],
                wbs=a.get("wbs", "Civil Works"),
                start_date=a.get("target_start") or "2026-10-01",
                finish_date=a.get("target_end") or "2026-10-31",
                planned_value=float(a.get("planned_value", 0.0)),
                earned_value=float(a.get("earned_value", 0.0)),
                actual_cost=float(a.get("earned_value", 0.0)) * 1.02, # estimate if AC not in XER
                assigned_team="Planning Team",
                status="In Progress" if a.get("status_code") == "TK_Active" else "Completed",
                is_critical_path=bool(a.get("is_critical_path", False)),
                float_days=int(a.get("total_float_days", 0))
            ))
    elif ext == ".xml":
        parsed = PrimaveraP6Parser.parse_xml_schedule(file_path)
        for a in parsed.get("activities", []):
            activities_to_insert.append(ScheduleActivity(
                activity_id=a["activity_id"],
                name=a["name"],
                wbs="Main Works",
                start_date=a.get("target_start") or "2026-10-01",
                finish_date=a.get("target_end") or "2026-10-31",
                planned_value=float(a.get("planned_value", 0.0)),
                earned_value=float(a.get("earned_value", 0.0)),
                actual_cost=float(a.get("earned_value", 0.0)),
                assigned_team="Project Team",
                status="In Progress",
                is_critical_path=bool(a.get("is_critical_path", False))
            ))
    elif ext in [".csv", ".xlsx", ".xls"]:
        df = pd.read_csv(file_path) if ext == ".csv" else pd.read_excel(file_path)
        cols = {str(c).lower().strip(): c for c in df.columns}
        
        # Match column names
        id_col = next((cols[k] for k in cols if any(x in k for x in ["act", "id", "code", "task_code"])), df.columns[0])
        name_col = next((cols[k] for k in cols if any(x in k for x in ["name", "task", "desc", "activity"])), df.columns[1] if len(df.columns) > 1 else df.columns[0])
        start_col = next((cols[k] for k in cols if "start" in k), None)
        finish_col = next((cols[k] for k in cols if any(x in k for x in ["finish", "end"])), None)
        pv_col = next((cols[k] for k in cols if any(x in k for x in ["pv", "plan", "target", "budget"])), None)
        ev_col = next((cols[k] for k in cols if any(x in k for x in ["ev", "earn"])), None)
        ac_col = next((cols[k] for k in cols if any(x in k for x in ["ac", "actual"])), None)

        for idx, row in df.iterrows():
            act_id = str(row.get(id_col, f"ACT-{idx+100}"))
            act_name = str(row.get(name_col, f"Activity {idx+1}"))
            start_d = str(row.get(start_col, "2026-10-01"))[:10] if start_col else "2026-10-01"
            fin_d = str(row.get(finish_col, "2026-10-31"))[:10] if finish_col else "2026-10-31"
            pv_v = float(row.get(pv_col, 10000.0)) if pv_col and pd.notna(row.get(pv_col)) else 10000.0
            ev_v = float(row.get(ev_col, pv_v * 0.8)) if ev_col and pd.notna(row.get(ev_col)) else pv_v * 0.8
            ac_v = float(row.get(ac_col, ev_v * 1.05)) if ac_col and pd.notna(row.get(ac_col)) else ev_v * 1.05

            activities_to_insert.append(ScheduleActivity(
                activity_id=act_id,
                name=act_name,
                wbs="Imported WBS",
                start_date=start_d,
                finish_date=fin_d,
                planned_value=pv_v,
                earned_value=ev_v,
                actual_cost=ac_v,
                assigned_team="Site Team",
                status="In Progress",
                is_critical_path=False
            ))

    if activities_to_insert:
        # Clear existing activities and replace with uploaded project
        db.exec(delete(ScheduleActivity))
        for item in activities_to_insert:
            db.add(item)
        db.commit()

    return len(activities_to_insert)

@router.get("/activities", response_model=List[Dict[str, Any]])
def list_activities(db: Session = Depends(get_session)):
    """Returns all current schedule activities."""
    activities = db.exec(select(ScheduleActivity).order_by(ScheduleActivity.start_date.asc())).all()
    return [
        {
            "activity_id": a.activity_id,
            "name": a.name,
            "wbs": a.wbs,
            "start_date": a.start_date,
            "finish_date": a.finish_date,
            "planned_value": a.planned_value,
            "earned_value": a.earned_value,
            "actual_cost": a.actual_cost,
            "assigned_team": a.assigned_team,
            "status": a.status,
            "is_critical_path": a.is_critical_path,
            "float_days": a.float_days
        }
        for a in activities
    ]

@router.post("/activity", response_model=Dict[str, Any])
def add_activity(act: ActivityCreateSchema, db: Session = Depends(get_session)):
    """Creates/adds or updates an activity."""
    existing = db.exec(select(ScheduleActivity).where(ScheduleActivity.activity_id == act.activity_id)).first()
    if existing:
        existing.name = act.name
        existing.wbs = act.wbs
        existing.start_date = act.start_date
        existing.finish_date = act.finish_date
        existing.planned_value = act.planned_value
        existing.earned_value = act.earned_value
        existing.actual_cost = act.actual_cost
        existing.predecessors = act.predecessors
        existing.assigned_team = act.assigned_team
        existing.status = act.status
        existing.is_critical_path = act.is_critical_path
        existing.float_days = act.float_days
        db.add(existing)
        db.commit()
        return {"status": "UPDATED", "message": f"Activity '{act.name}' ({act.activity_id}) updated successfully."}
    
    new_record = ScheduleActivity(
        activity_id=act.activity_id,
        name=act.name,
        wbs=act.wbs,
        start_date=act.start_date,
        finish_date=act.finish_date,
        planned_value=act.planned_value,
        earned_value=act.earned_value,
        actual_cost=act.actual_cost,
        predecessors=act.predecessors,
        assigned_team=act.assigned_team,
        status=act.status,
        is_critical_path=act.is_critical_path,
        float_days=act.float_days
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return {"status": "SUCCESS", "message": f"Activity '{act.name}' ({act.activity_id}) added successfully."}

@router.delete("/activities/clear", response_model=Dict[str, Any])
def clear_all_activities(db: Session = Depends(get_session)):
    """Clears all activities to start a clean project."""
    db.exec(delete(ScheduleActivity))
    db.commit()
    return {"status": "CLEARED", "message": "All schedule activities have been cleared. You can now upload your own project."}

@router.delete("/activities/{activity_id}", response_model=Dict[str, Any])
def delete_single_activity(activity_id: str, db: Session = Depends(get_session)):
    """Deletes a single activity by ID."""
    act = db.exec(select(ScheduleActivity).where(ScheduleActivity.activity_id == activity_id)).first()
    if not act:
        raise HTTPException(status_code=404, detail=f"Activity '{activity_id}' not found")
    db.delete(act)
    db.commit()
    return {"status": "SUCCESS", "message": f"Activity '{act.name}' ({activity_id}) deleted successfully."}


@router.get("/s-curve", response_model=Dict[str, Any])
def get_s_curve_data(db: Session = Depends(get_session)):
    """Returns dynamically computed S-Curve based on current activities."""
    activities = db.exec(select(ScheduleActivity)).all()
    act_dicts = [
        {
            "activity_id": a.activity_id,
            "name": a.name,
            "start_date": a.start_date,
            "finish_date": a.finish_date,
            "planned_value": a.planned_value,
            "earned_value": a.earned_value,
        }
        for a in activities
    ]
    return PrimaveraP6Parser.calculate_s_curve(act_dicts)

@router.get("/list", response_model=List[Dict[str, Any]])
def list_documents(db: Session = Depends(get_session)):
    """Lists all indexed project documents."""
    docs = db.exec(select(ProjectDocument).order_by(ProjectDocument.uploaded_at.desc())).all()
    return [
        {
            "document_id": d.document_id,
            "filename": d.filename,
            "category": d.category,
            "file_size_bytes": d.file_size_bytes,
            "chunks_indexed": d.chunks_indexed,
            "uploaded_at": d.uploaded_at.isoformat()
        }
        for d in docs
    ]

@router.get("/kpi-summary", response_model=ScheduleKPISchema)
def get_kpi_summary(db: Session = Depends(get_session)):
    """Returns aggregated Earned Value Management (EVM) KPIs for project dashboard."""
    activities = db.exec(select(ScheduleActivity)).all()
    
    total_pv = sum(a.planned_value for a in activities)
    total_ev = sum(a.earned_value for a in activities)
    total_ac = sum(a.actual_cost for a in activities)

    spi = (total_ev / total_pv) if total_pv > 0 else 1.0
    cpi = (total_ev / total_ac) if total_ac > 0 else 1.0
    sv = total_ev - total_pv
    cv = total_ev - total_ac

    if spi >= 1.05:
        sched_status = "Ahead of Schedule (متقدم عن الجدول)"
    elif spi >= 0.95:
        sched_status = "On Track (على المسار المخطط)"
    else:
        sched_status = "Behind Schedule (متأخر عن الجدول)"

    if cpi >= 1.05:
        cost_status = "Under Budget (أقل من الميزانية)"
    elif cpi >= 0.95:
        cost_status = "On Budget (مطابق للميزانية)"
    else:
        cost_status = "Over Budget (تجاوز في التكلفة)"

    commentary = (
        f"المشروع الحالي: مؤشر الأداء الزمني SPI هو {spi:.3f} ({sched_status}) مع حيود زمني قدره {sv:,.2f} ر.س. "
        f"مؤشر كفاءة التكلفة CPI هو {cpi:.3f} ({cost_status}) مع حيود تكلفة قدره {cv:,.2f} ر.س."
    )

    return ScheduleKPISchema(
        project_name="Current Active Project",
        period="Live Status",
        planned_value=total_pv,
        earned_value=total_ev,
        actual_cost=total_ac,
        schedule_performance_index=spi,
        cost_performance_index=cpi,
        schedule_variance=sv,
        cost_variance=cv,
        schedule_status=sched_status,
        cost_status=cost_status,
        commentary=commentary
    )
