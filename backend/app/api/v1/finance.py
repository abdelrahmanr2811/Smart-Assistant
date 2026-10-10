import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.db_models import PaymentCertificate, ScheduleActivity, Project

router = APIRouter(prefix="/finance", tags=["Cash Flow & IPC Billing"])

class GenerateIPCRequest(BaseModel):
    project_id: Optional[str] = "PRJ-01"
    period_month: Optional[str] = "November 2026"
    advance_recovery_pct: Optional[float] = 10.0 # 10%
    retention_pct: Optional[float] = 5.0 # 5%

class CashFlowForecastResponse(BaseModel):
    project_id: str
    months: List[str]
    cash_in_projected: List[float]
    cash_out_projected: List[float]
    net_monthly_flow: List[float]
    cumulative_cash_position: List[float]
    has_deficit_warning: bool
    deficit_month: Optional[str] = None
    deficit_amount: Optional[float] = 0.0
    recommendation: str

@router.get("/ipcs", response_model=List[PaymentCertificate])
def list_ipcs(
    project_id: Optional[str] = Query("PRJ-01"),
    session: Session = Depends(get_session)
):
    """List all Interim Payment Certificates (IPCs)."""
    statement = select(PaymentCertificate).where(PaymentCertificate.project_id == project_id)
    return session.exec(statement).all()

@router.post("/ipcs/generate", response_model=PaymentCertificate)
def generate_interim_payment_certificate(
    payload: GenerateIPCRequest,
    session: Session = Depends(get_session)
):
    """
    Generates a draft monthly IPC from active Earned Value (EV) and calculates:
    - Gross work done
    - Advance payment recovery (e.g. 10%)
    - Retention fund deduction (e.g. 5%)
    - Net payable amount to Contractor
    """
    activities = session.exec(select(ScheduleActivity).where(ScheduleActivity.project_id == payload.project_id)).all()
    gross_ev = sum(a.earned_value for a in activities) if activities else 450000.0
    materials_on_site = 125000.0

    gross_total = gross_ev + materials_on_site
    adv_deduction = (payload.advance_recovery_pct / 100.0) * gross_ev
    ret_deduction = (payload.retention_pct / 100.0) * gross_total
    net_payable = gross_total - adv_deduction - ret_deduction

    ipc_id = f"IPC-{uuid.uuid4().hex[:4].upper()}"
    cert_num = f"IPC-{datetime.now().strftime('%m%y')}-{uuid.uuid4().hex[:4].upper()}"

    new_ipc = PaymentCertificate(
        ipc_id=ipc_id,
        project_id=payload.project_id or "PRJ-01",
        certificate_number=cert_num,
        period_month=payload.period_month or "November 2026",
        gross_work_done=gross_ev,
        materials_on_site=materials_on_site,
        advance_payment_recovery=adv_deduction,
        retention_deduction=ret_deduction,
        net_payable_amount=net_payable,
        status="Draft",
        issue_date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        payment_due_date=datetime.fromtimestamp(datetime.now().timestamp() + 30*86400).strftime("%Y-%m-%d")
    )
    session.add(new_ipc)
    session.commit()
    session.refresh(new_ipc)
    return new_ipc

@router.get("/cash-flow", response_model=CashFlowForecastResponse)
def get_cash_flow_forecast(
    project_id: Optional[str] = Query("PRJ-01"),
    session: Session = Depends(get_session)
):
    """
    Calculates 6-month forward Cash Flow projection (Cash-In vs Cash-Out)
    and alerts if a cash deficit is forecasted in upcoming periods.
    """
    months = ["Oct 2026", "Nov 2026", "Dec 2026", "Jan 2027", "Feb 2027", "Mar 2027"]
    
    if project_id == "PRJ-03":
        # Project 3 has delay/deficit
        cash_in = [700000.0, 650000.0, 500000.0, 480000.0, 800000.0, 950000.0]
        cash_out = [850000.0, 920000.0, 780000.0, 600000.0, 720000.0, 800000.0]
    else:
        cash_in = [800000.0, 850000.0, 920000.0, 750000.0, 880000.0, 1100000.0]
        cash_out = [720000.0, 760000.0, 810000.0, 820000.0, 790000.0, 950000.0]

    net_flow = [cin - cout for cin, cout in zip(cash_in, cash_out)]
    
    cumulative = []
    curr = 150000.0 # Starting liquidity
    has_deficit = False
    deficit_month = None
    deficit_amount = 0.0

    for i, net in enumerate(net_flow):
        curr += net
        cumulative.append(curr)
        if curr < 0 and not has_deficit:
            has_deficit = True
            deficit_month = months[i]
            deficit_amount = abs(curr)

    recom = (
        f"⚠️ تنبيه سيولة نقدية: متوقع عجز مالي بقيمة {deficit_amount:,.2f} ر.س في شهر {deficit_month}. يُوصى بالإسراع في اعتماد مستخلصات الأعمال المنجزة لتجنب توقف المقاولين."
        if has_deficit else
        "✅ التدفق النقدي متزن والسيولة التراكمية في نطاق الأمان المالي المعتمد."
    )

    return CashFlowForecastResponse(
        project_id=project_id or "PRJ-01",
        months=months,
        cash_in_projected=cash_in,
        cash_out_projected=cash_out,
        net_monthly_flow=net_flow,
        cumulative_cash_position=cumulative,
        has_deficit_warning=has_deficit,
        deficit_month=deficit_month,
        deficit_amount=deficit_amount,
        recommendation=recom
    )
