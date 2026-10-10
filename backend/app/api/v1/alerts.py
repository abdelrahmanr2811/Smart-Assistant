from fastapi import APIRouter, Depends, Query
from typing import Dict, Any
from app.services.anomaly_detector import run_project_anomaly_audit

router = APIRouter(prefix="/alerts", tags=["Early Warning & Anomaly Detection"])

@router.get("/audit", response_model=Dict[str, Any])
def get_project_alerts_audit(project_id: str = Query(default="PRJ-01")):
    return run_project_anomaly_audit(project_id=project_id)

@router.post("/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: str):
    return {
        "status": "success",
        "alert_id": alert_id,
        "message": "Alert acknowledged by Site Project Controls Manager."
    }
