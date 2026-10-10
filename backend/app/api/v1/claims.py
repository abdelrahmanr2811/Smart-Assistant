import uuid
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.db_models import ContractClaim, VariationOrder, Project
from app.config import settings

router = APIRouter(prefix="/claims", tags=["FIDIC Claims & Variation Orders"])

class GenerateNoticeRequest(BaseModel):
    project_id: Optional[str] = "PRJ-01"
    event_title: str
    cause_description: str
    delay_days: int = 14
    estimated_cost: float = 35000.0
    clause_ref: Optional[str] = "FIDIC Red Book Sub-Clause 20.1 & 8.4"
    responsible_party: Optional[str] = "Employer / Engineer"

class NoticeResponse(BaseModel):
    claim_id: str
    project_id: str
    clause_ref: str
    formal_letter: str
    delay_days: int
    cost_claimed: float

class CreateVariationRequest(BaseModel):
    project_id: Optional[str] = "PRJ-01"
    vo_number: str
    title: str
    description: str
    cost_impact: float
    schedule_days_impact: int
    requested_by: str = "Owner Representative"

@router.get("", response_model=List[ContractClaim])
def list_claims(
    project_id: Optional[str] = Query("PRJ-01"),
    session: Session = Depends(get_session)
):
    """List all FIDIC claims and EOT requests for the project."""
    statement = select(ContractClaim).where(ContractClaim.project_id == project_id)
    return session.exec(statement).all()

@router.post("/generate-notice", response_model=NoticeResponse)
def generate_fidic_notice(
    payload: GenerateNoticeRequest,
    session: Session = Depends(get_session)
):
    """
    Generates a formal FIDIC Contract Notice of Claim (Sub-Clause 20.1 / 8.4)
    and saves the claim draft into the project database.
    """
    prj = session.exec(select(Project).where(Project.project_id == payload.project_id)).first()
    prj_name = prj.name if prj else "Al-Narges Tower Project"
    consultant = prj.consultant_name if prj else "The Engineer"
    contractor = prj.contractor_name if prj else "The Main Contractor"
    today_str = datetime.now(timezone.utc).strftime("%d %B %Y")
    claim_id = f"CLM-{datetime.now().year}-{uuid.uuid4().hex[:4].upper()}"

    formal_letter = f"""Ref: {claim_id}/NOT-20.1
Date: {today_str}

To: {consultant} (The Engineer)
Project: {prj_name}
Subject: Formal Notice of Claim for Extension of Time (EOT) and Additional Costs
Clause Reference: {payload.clause_ref}

Dear Sir / Madam,

Pursuant to {payload.clause_ref} of the General Conditions of Contract, we hereby give formal notice of the occurrence of an event and circumstance giving rise to an entitlement for an Extension of Time for Completion and reimbursement of additional Cost:

1. EVENT DESCRIPTION:
{payload.event_title}

2. CAUSE AND PARTICULARS:
{payload.cause_description}

3. PRELIMINARY IMPACT ASSESSMENT:
• Critical Path Schedule Delay: {payload.delay_days} Calendar Days
• Estimated Direct Cost & Disruption: SAR {payload.estimated_cost:,.2f}
• Attributable Cause: {payload.responsible_party}

In accordance with contractual requirements, full contemporaneous records are being maintained on site and a fully detailed claim submission with schedule network analysis (As-Planned vs. As-Built) will be submitted within the 42-day contractual window.

Yours faithfully,

For and on behalf of {contractor}
Project Director / Commercial & Contracts Lead
"""

    new_claim = ContractClaim(
        claim_id=claim_id,
        project_id=payload.project_id or "PRJ-01",
        title=payload.event_title,
        claim_type="EOT_AND_COST",
        fidic_clause_ref=payload.clause_ref or "FIDIC Sub-Clause 20.1 & 8.4",
        delay_days_claimed=payload.delay_days,
        cost_claimed=payload.estimated_cost,
        status="Submitted",
        cause_of_delay=payload.cause_description,
        responsible_party=payload.responsible_party or "Employer / Engineer",
        narrative_letter=formal_letter,
        submitted_date=today_str
    )
    session.add(new_claim)
    session.commit()

    return NoticeResponse(
        claim_id=claim_id,
        project_id=payload.project_id or "PRJ-01",
        clause_ref=payload.clause_ref or "FIDIC Sub-Clause 20.1 & 8.4",
        formal_letter=formal_letter,
        delay_days=payload.delay_days,
        cost_claimed=payload.estimated_cost
    )

@router.get("/variations", response_model=List[VariationOrder])
def list_variation_orders(
    project_id: Optional[str] = Query("PRJ-01"),
    session: Session = Depends(get_session)
):
    """List all Variation Orders (VO Log) for the project."""
    statement = select(VariationOrder).where(VariationOrder.project_id == project_id)
    return session.exec(statement).all()

@router.post("/variations", response_model=VariationOrder)
def create_variation_order(
    payload: CreateVariationRequest,
    session: Session = Depends(get_session)
):
    """Registers a new Variation Order / Scope Change."""
    vo_id = f"VO-{uuid.uuid4().hex[:4].upper()}"
    new_vo = VariationOrder(
        vo_id=vo_id,
        project_id=payload.project_id or "PRJ-01",
        vo_number=payload.vo_number,
        title=payload.title,
        description=payload.description,
        cost_impact=payload.cost_impact,
        schedule_days_impact=payload.schedule_days_impact,
        status="Under Evaluation",
        requested_by=payload.requested_by,
        approved_amount=0.0
    )
    session.add(new_vo)
    session.commit()
    session.refresh(new_vo)
    return new_vo
