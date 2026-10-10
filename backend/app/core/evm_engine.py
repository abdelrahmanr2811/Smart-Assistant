from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class EVMMetricsResult(BaseModel):
    status: str = Field(description="'SUCCESS' or 'INSUFFICIENT_DATA'")
    message: str
    data_date: str
    budget_at_completion_bac: float = 0.0
    planned_value_pv: float = 0.0
    earned_value_ev: float = 0.0
    actual_cost_ac: float = 0.0
    schedule_performance_index_spi: Optional[float] = None
    cost_performance_index_cpi: Optional[float] = None
    schedule_variance_sv: float = 0.0
    cost_variance_cv: float = 0.0
    estimate_at_completion_eac: Optional[float] = None
    estimate_to_complete_etc: Optional[float] = None
    variance_at_completion_vac: Optional[float] = None
    to_complete_performance_index_tcpi: Optional[float] = None
    schedule_health: str = "N/A"
    cost_health: str = "N/A"
    activities_analyzed_count: int = 0

class EVMEngine:
    """
    Deterministic Earned Value Management (EVM) calculation engine in pure Python.
    No LLM is involved in calculating any numbers.
    Adheres to PMI / ISO 21508 standards.
    """

    @staticmethod
    def calculate_evm(
        activities: List[Dict[str, Any]],
        actual_costs_source: Optional[Dict[str, float]] = None,
        data_date: Optional[str] = None
    ) -> EVMMetricsResult:
        """
        Calculates all EVM parameters deterministically.
        
        activities: list of dicts with keys:
          - activity_id (str)
          - planned_value (float, BAC of task)
          - earned_value (float, or percent_complete * planned_value)
          - actual_cost (optional float, fallback if not in actual_costs_source)
        actual_costs_source: optional mapping of activity_id -> actual_cost from finance
        data_date: reporting cutoff date (ISO format YYYY-MM-DD)
        """
        if not activities:
            return EVMMetricsResult(
                status="INSUFFICIENT_DATA",
                message="No cost-loaded activities provided for EVM calculation.",
                data_date=data_date or "N/A"
            )

        total_bac = 0.0
        total_pv = 0.0
        total_ev = 0.0
        total_ac = 0.0

        for act in activities:
            pv = float(act.get("planned_value", 0.0) or 0.0)
            ev = float(act.get("earned_value", 0.0) or 0.0)
            act_id = str(act.get("activity_id", ""))

            # Resolve AC from finance source first, fallback to activity record
            if actual_costs_source and act_id in actual_costs_source:
                ac = float(actual_costs_source[act_id] or 0.0)
            else:
                ac = float(act.get("actual_cost", 0.0) or 0.0)

            total_bac += pv
            total_pv += pv
            total_ev += ev
            total_ac += ac

        if total_pv <= 0 and total_ev <= 0 and total_ac <= 0:
            return EVMMetricsResult(
                status="INSUFFICIENT_DATA",
                message="Cost values (PV/EV/AC) are all zero or missing. Cannot compute EVM metrics.",
                data_date=data_date or "N/A"
            )

        # 1. Variances
        sv = total_ev - total_pv
        cv = total_ev - total_ac

        # 2. Performance Indices with safe division
        spi = (total_ev / total_pv) if total_pv > 0 else None
        cpi = (total_ev / total_ac) if total_ac > 0 else None

        # 3. Forecasts
        # Standard EAC = BAC / CPI (when current variance is typical)
        if cpi is not None and cpi > 0:
            eac = total_bac / cpi
            etc = eac - total_ac
            vac = total_bac - eac
        else:
            eac = None
            etc = None
            vac = None

        # 4. TCPI = (BAC - EV) / (BAC - AC)
        denom_tcpi = total_bac - total_ac
        if denom_tcpi > 0:
            tcpi = (total_bac - total_ev) / denom_tcpi
        else:
            tcpi = None

        # 5. Health Status Classification
        if spi is not None:
            if spi >= 1.05:
                sched_health = "Ahead of Schedule (متقدم)"
            elif spi >= 0.95:
                sched_health = "On Track (على المسار)"
            else:
                sched_health = "Behind Schedule / Delayed (متأخر)"
        else:
            sched_health = "N/A"

        if cpi is not None:
            if cpi >= 1.05:
                cost_health = "Under Budget (وفورات تكلفة)"
            elif cpi >= 0.95:
                cost_health = "On Budget (مطابق للميزانية)"
            else:
                cost_health = "Over Budget / Cost Overrun (تجاوز تكلفة)"
        else:
            cost_health = "N/A"

        return EVMMetricsResult(
            status="SUCCESS",
            message="EVM metrics computed deterministically from project controls data.",
            data_date=data_date or datetime.utcnow().strftime("%Y-%m-%d"),
            budget_at_completion_bac=round(total_bac, 2),
            planned_value_pv=round(total_pv, 2),
            earned_value_ev=round(total_ev, 2),
            actual_cost_ac=round(total_ac, 2),
            schedule_performance_index_spi=round(spi, 3) if spi is not None else None,
            cost_performance_index_cpi=round(cpi, 3) if cpi is not None else None,
            schedule_variance_sv=round(sv, 2),
            cost_variance_cv=round(cv, 2),
            estimate_at_completion_eac=round(eac, 2) if eac is not None else None,
            estimate_to_complete_etc=round(etc, 2) if etc is not None else None,
            variance_at_completion_vac=round(vac, 2) if vac is not None else None,
            to_complete_performance_index_tcpi=round(tcpi, 3) if tcpi is not None else None,
            schedule_health=sched_health,
            cost_health=cost_health,
            activities_analyzed_count=len(activities)
        )
