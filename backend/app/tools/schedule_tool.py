import json
from typing import Optional
from langchain_core.tools import tool
from sqlmodel import Session, select
from app.core.database import engine
from app.models.db_models import ScheduleActivity
from app.core.evm_engine import EVMEngine
from app.core.rag_engine import rag_engine

@tool
def get_schedule_metrics(kpi_name: str = "ALL", period_or_month: str = "October 2026") -> str:
    """
    Parses schedule and Earned Value Management (EVM) data (Primavera P6 / MS Project).
    Computes PV, EV, AC, SPI, CPI, SV, CV, EAC, ETC, VAC, and TCPI deterministically in pure Python.
    No LLM is involved in computing numbers.
    """
    with Session(engine) as session:
        activities_records = session.exec(select(ScheduleActivity)).all()

    if not activities_records:
        return json.dumps({
            "status": "INSUFFICIENT_DATA",
            "message": "No schedule activities found in project database."
        }, ensure_ascii=False)

    activities_data = [
        {
            "activity_id": a.activity_id,
            "planned_value": a.planned_value,
            "earned_value": a.earned_value,
            "actual_cost": a.actual_cost,
            "name": a.name
        }
        for a in activities_records
    ]

    evm_res = EVMEngine.calculate_evm(activities=activities_data, data_date="2026-10-04")
    
    # Format structured report
    spi_val = f"{evm_res.schedule_performance_index_spi:.3f}" if evm_res.schedule_performance_index_spi is not None else "N/A"
    cpi_val = f"{evm_res.cost_performance_index_cpi:.3f}" if evm_res.cost_performance_index_cpi is not None else "N/A"
    eac_val = f"SAR {evm_res.estimate_at_completion_eac:,.2f}" if evm_res.estimate_at_completion_eac is not None else "N/A"
    etc_val = f"SAR {evm_res.estimate_to_complete_etc:,.2f}" if evm_res.estimate_to_complete_etc is not None else "N/A"
    vac_val = f"SAR {evm_res.variance_at_completion_vac:,.2f}" if evm_res.variance_at_completion_vac is not None else "N/A"
    tcpi_val = f"{evm_res.to_complete_performance_index_tcpi:.3f}" if evm_res.to_complete_performance_index_tcpi is not None else "N/A"

    report = (
        f"📊 === Project EVM & Schedule Performance Report (Deterministic) ===\n"
        f"Period / Baseline: {period_or_month.upper()} | Data Date: {evm_res.data_date}\n"
        f"--------------------------------------------------\n"
        f"• Planned Value (PV):  SAR {evm_res.planned_value_pv:,.2f}\n"
        f"• Earned Value (EV):   SAR {evm_res.earned_value_ev:,.2f}\n"
        f"• Actual Cost (AC):    SAR {evm_res.actual_cost_ac:,.2f}\n"
        f"• Schedule Variance (SV = EV - PV): SAR {evm_res.schedule_variance_sv:,.2f}\n"
        f"• Cost Variance (CV = EV - AC):     SAR {evm_res.cost_variance_cv:,.2f}\n"
        f"• SPI (EV / PV):       {spi_val} -> {evm_res.schedule_health}\n"
        f"• CPI (EV / AC):       {cpi_val} -> {evm_res.cost_health}\n"
        f"--------------------------------------------------\n"
        f"Forecasting & Completion Metrics (EVM Forecasts):\n"
        f"• Estimate at Completion (EAC = BAC/CPI): {eac_val}\n"
        f"• Estimate to Complete (ETC = EAC - AC): {etc_val}\n"
        f"• Variance at Completion (VAC = BAC - EAC): {vac_val}\n"
        f"• To-Complete Index (TCPI): {tcpi_val}\n"
        f"--------------------------------------------------\n"
        f"Analyzed Activities: {evm_res.activities_analyzed_count} cost-loaded tasks."
    )

    return report

@tool
def get_daily_activities(target_date: str) -> str:
    """
    Queries schedule database and Primavera P6 sheets for site activities
    where Start_Date <= target_date <= Finish_Date or Start_Date == target_date.
    Returns Activity ID, Name, WBS, Predecessors, and Assigned Contractor/Team.
    """
    target = target_date.strip()
    
    with Session(engine) as session:
        activities = session.exec(select(ScheduleActivity)).all()

    matching = []
    for a in activities:
        if a.start_date == target or a.finish_date == target:
            matching.append(a)
        elif a.start_date <= target <= a.finish_date:
            matching.append(a)

    if not matching:
        chroma_res = rag_engine.query_collection("schedule_collection", f"activities on {target}", n_results=3)
        if chroma_res:
            res_text = "\n".join([f"• {c['content']}" for c in chroma_res])
            return f"=== Site Activities for {target} (ChromaDB Index) ===\n{res_text}"
        return f"No scheduled activities found for date {target}."

    output = [f"📅 === Scheduled Site Activities for {target} ==="]
    for act in matching:
        output.append(
            f"• [{act.activity_id}] {act.name}\n"
            f"  - WBS: {act.wbs}\n"
            f"  - Timeline: {act.start_date} to {act.finish_date} (Status: {act.status})\n"
            f"  - Assigned Contractor/Team: {act.assigned_team}\n"
            f"  - Predecessors: {act.predecessors or 'None'}\n"
            f"  - EVM: PV=SAR {act.planned_value:,.2f} | EV=SAR {act.earned_value:,.2f}"
        )

    return "\n\n".join(output)
