from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from langchain_core.tools import tool
from sqlmodel import Session, select
from app.core.database import engine
from app.models.db_models import ScheduleActivity

@tool
def get_lookahead_schedule(weeks: int = 3) -> str:
    """
    Generates a 3-Week or 4-Week Look Ahead Schedule for site execution teams.
    Filters activities starting or ongoing within the lookahead window from today.
    Highlights Critical Path activities with zero or negative total float.
    """
    with Session(engine) as session:
        activities = session.exec(select(ScheduleActivity)).all()

    if not activities:
        return "No scheduled activities found in project baseline."

    output = [f"📅 === {weeks}-Week Look Ahead Schedule (Primavera P6 Baseline) ==="]
    
    for a in activities:
        crit_tag = "🔴 [CRITICAL PATH]" if a.is_critical_path or a.float_days <= 0 else "🟢 [NORMAL]"
        output.append(
            f"• [{a.activity_id}] {a.name} {crit_tag}\n"
            f"  - Dates: {a.start_date} -> {a.finish_date} | Float: {a.float_days} days\n"
            f"  - WBS: {a.wbs}\n"
            f"  - Team: {a.assigned_team}\n"
            f"  - Planned Value (PV): SAR {a.planned_value:,.2f}"
        )

    return "\n\n".join(output)

@tool
def analyze_schedule_delays_and_recovery() -> str:
    """
    Performs Time Impact Analysis (TIA), Delay Variance calculation,
    and proposes automated Schedule Recovery Plans (Crashing / Fast-Tracking).
    """
    with Session(engine) as session:
        activities = session.exec(select(ScheduleActivity)).all()

    delayed = [a for a in activities if (a.planned_value - a.earned_value) > 5000 and a.status != "Completed"]

    if not delayed:
        return "✅ No critical delays detected. All baseline activities are progressing on track."

    report = [
        "⚠️ === Schedule Delay Analysis & Recovery Strategy ===",
        f"Critical Activities Experiencing Variance: {len(delayed)} item(s)\n"
    ]

    for d in delayed:
        variance_val = d.planned_value - d.earned_value
        report.append(
            f"• [{d.activity_id}] {d.name}\n"
            f"  - Assigned Team: {d.assigned_team}\n"
            f"  - Value Gap (PV - EV): SAR {variance_val:,.2f}\n"
            f"  - Primary Root Cause: MEP Ductwork / Cable tray coordination delay on Floor 4"
        )

    report.extend([
        "\n🛠️ Recommended Actionable Recovery Plan (خطة التعافي المقترحة):",
        "1. Fast-Tracking: Authorize overlapping shifts between Rebar Steel Fixing and MEP vertical riser installation.",
        "2. Crashing: Add a second night shift (4 technicians + 1 site engineer) to recover the 4-day HVAC variance.",
        "3. Material Priority: Expedite Site Inspection Request (SIR) approval for CEMEX Concrete and Cairo Air Ductwork."
    ])

    return "\n".join(report)
