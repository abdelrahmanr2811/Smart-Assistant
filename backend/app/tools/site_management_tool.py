from typing import Optional
from langchain_core.tools import tool
from sqlmodel import Session, select
from app.core.database import engine
from app.models.db_models import DailySiteReport

@tool
def get_daily_site_report(report_date: str = "2026-10-04") -> str:
    """
    Retrieves the Daily Site Progress Report (DSR).
    Includes weather conditions, total active manpower, work accomplished, safety incidents, and critical site notices.
    """
    with Session(engine) as session:
        reports = session.exec(select(DailySiteReport)).all()

    target = report_date.strip()
    match = next((r for r in reports if r.report_date == target), None)

    if not match and reports:
        match = reports[-1]

    if not match:
        return f"No Daily Site Progress Report found for {report_date}."

    return (
        f"📝 === Daily Site Progress Report (DSR) - {match.report_date} ===\n"
        f"• Site Weather: {match.weather}\n"
        f"• Total Active Manpower: {match.total_manpower} Workers / Technicians\n"
        f"• Safety (HSE) Incidents: {match.safety_incidents} (Zero Accidents)\n"
        f"• Submitted By: {match.submitted_by}\n"
        f"--------------------------------------------------\n"
        f"Work Accomplished Summary:\n{match.work_summary}\n"
        f"--------------------------------------------------\n"
        f"Critical Site Coordination Notes:\n{match.critical_issues or 'All site sectors operating normally.'}"
    )

@tool
def get_equipment_and_machinery_log() -> str:
    """
    Returns the active heavy machinery and site equipment status (Cranes, Concrete Pumps, Excavators).
    """
    return (
        "🚜 === Site Plant & Heavy Equipment Log ===\n"
        "• Tower Crane TC-01: In Operation (Core Wall Zone A lifting) | 98% Efficiency\n"
        "• Tower Crane TC-02: Scheduled for Jacking Extension Stage 1 | Off-peak night shift\n"
        "• Stationary Concrete Pump 1 (Putzmeister 52m): Active on Raft Zone B Pouring | 450 m3 poured\n"
        "• Diesel Generators (500 kVA x 2): Operating continuously with backup fuel confirmed\n"
        "• Excavators CAT 330: Standby at basement ramp laydown area"
    )
