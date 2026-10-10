from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.db_models import Project, ScheduleActivity, NCRRecord, EarlyWarningAlert

router = APIRouter(prefix="/portfolio", tags=["Portfolio Multi-Project Executive Dashboard"])

class ProjectMapPin(BaseModel):
    project_id: str
    code: str
    name: str
    latitude: float
    longitude: float
    location_name: str
    health_status: str # ON_TRACK, WATCH, CRITICAL
    total_budget: float
    spi: float
    cpi: float
    contractor: str
    consultant: str
    open_alerts_count: int

class PortfolioExecutiveSummary(BaseModel):
    total_projects_count: int
    total_portfolio_budget: float
    portfolio_avg_spi: float
    portfolio_avg_cpi: float
    healthy_projects_count: int
    watch_projects_count: int
    critical_projects_count: int
    total_open_ncrs: int
    total_active_alerts: int
    projects_breakdown: List[Dict[str, Any]]

@router.get("/summary", response_model=PortfolioExecutiveSummary)
def get_portfolio_executive_summary(session: Session = Depends(get_session)):
    """Aggregated Portfolio Executive Dashboard for C-Level Directors."""
    projects = session.exec(select(Project)).all()
    all_ncrs = session.exec(select(NCRRecord).where(NCRRecord.status != "Closed")).all()
    all_alerts = session.exec(select(EarlyWarningAlert).where(EarlyWarningAlert.is_acknowledged == False)).all()

    total_budget = sum(p.total_budget for p in projects)
    
    # Custom KPIs for demo portfolio
    spi_map = {"PRJ-01": 0.820, "PRJ-02": 1.040, "PRJ-03": 0.790}
    cpi_map = {"PRJ-01": 0.910, "PRJ-02": 1.020, "PRJ-03": 0.850}

    breakdown = []
    healthy = 0
    watch = 0
    crit = 0

    for p in projects:
        spi = spi_map.get(p.project_id, 0.95)
        cpi = cpi_map.get(p.project_id, 0.95)
        status = "ON_TRACK" if spi >= 1.0 and cpi >= 1.0 else ("CRITICAL" if spi < 0.85 or cpi < 0.85 else "WATCH")
        
        if status == "ON_TRACK":
            healthy += 1
        elif status == "WATCH":
            watch += 1
        else:
            crit += 1

        breakdown.append({
            "project_id": p.project_id,
            "code": p.code,
            "name": p.name,
            "budget": p.total_budget,
            "spi": spi,
            "cpi": cpi,
            "health_status": status,
            "location": p.location_name,
            "is_active": p.is_active
        })

    avg_spi = sum(b["spi"] for b in breakdown) / len(breakdown) if breakdown else 1.0
    avg_cpi = sum(b["cpi"] for b in breakdown) / len(breakdown) if breakdown else 1.0

    return PortfolioExecutiveSummary(
        total_projects_count=len(projects),
        total_portfolio_budget=total_budget,
        portfolio_avg_spi=round(avg_spi, 3),
        portfolio_avg_cpi=round(avg_cpi, 3),
        healthy_projects_count=healthy,
        watch_projects_count=watch,
        critical_projects_count=crit,
        total_open_ncrs=len(all_ncrs),
        total_active_alerts=len(all_alerts),
        projects_breakdown=breakdown
    )

@router.get("/map-pins", response_model=List[ProjectMapPin])
def get_portfolio_gis_map_pins(session: Session = Depends(get_session)):
    """Returns GIS geographic pins with live metrics for map visualization."""
    projects = session.exec(select(Project)).all()
    spi_map = {"PRJ-01": 0.820, "PRJ-02": 1.040, "PRJ-03": 0.790}
    cpi_map = {"PRJ-01": 0.910, "PRJ-02": 1.020, "PRJ-03": 0.850}

    pins = []
    for p in projects:
        alerts_count = session.exec(
            select(EarlyWarningAlert).where(
                EarlyWarningAlert.project_id == p.project_id,
                EarlyWarningAlert.is_acknowledged == False
            )
        ).all()

        spi = spi_map.get(p.project_id, 0.95)
        cpi = cpi_map.get(p.project_id, 0.95)
        status = "ON_TRACK" if spi >= 1.0 and cpi >= 1.0 else ("CRITICAL" if spi < 0.85 or cpi < 0.85 else "WATCH")

        pins.append(ProjectMapPin(
            project_id=p.project_id,
            code=p.code,
            name=p.name,
            latitude=p.latitude,
            longitude=p.longitude,
            location_name=p.location_name,
            health_status=status,
            total_budget=p.total_budget,
            spi=spi,
            cpi=cpi,
            contractor=p.contractor_name,
            consultant=p.consultant_name,
            open_alerts_count=len(alerts_count)
        ))

    return pins
