from typing import Optional
from langchain_core.tools import tool
from sqlmodel import Session, select
from app.core.database import engine
from app.models.db_models import NCRRecord, MIRRecord

@tool
def query_ncr_records(status: str = "ALL") -> str:
    """
    Queries Non-Conformance Reports (NCR) issued on site.
    Filters by status: 'Open', 'Under Review', 'Closed', or 'ALL'.
    Returns NCR number, description, severity, assigned engineer, and target closure date.
    """
    with Session(engine) as session:
        ncrs = session.exec(select(NCRRecord)).all()

    stat_filter = status.upper().strip()
    matches = [n for n in ncrs if stat_filter == "ALL" or n.status.upper() == stat_filter]

    if not matches:
        return f"No Non-Conformance Reports (NCR) found with status='{status}'."

    output = [f"📋 === Site Quality Non-Conformance Reports (NCR) [{status}] ==="]
    for n in matches:
        sev_icon = "🔴" if n.severity == "Critical" else ("🟠" if n.severity == "Major" else "🟡")
        output.append(
            f"• [{n.ncr_number}] {n.title} {sev_icon} ({n.severity})\n"
            f"  - Status: {n.status}\n"
            f"  - Description: {n.description}\n"
            f"  - Assigned Engineer: {n.assigned_engineer}\n"
            f"  - Issued: {n.issued_date} | Target Closure: {n.target_closure_date}\n"
            f"  - Corrective Action: {n.corrective_action or 'Pending Proposal'}"
        )

    return "\n\n".join(output)

@tool
def query_mir_inspection_requests(material: str = "") -> str:
    """
    Queries Material Inspection Requests (MIR) and Site Inspection Requests (SIR).
    Returns MIR Number, Material, Supplier, Inspection Date, Inspector, and Status (Approved/Rejected).
    """
    with Session(engine) as session:
        mirs = session.exec(select(MIRRecord)).all()

    mat_filter = material.lower().strip()
    matches = [m for m in mirs if not mat_filter or mat_filter in m.material_name.lower() or mat_filter in m.supplier.lower()]

    if not matches:
        return f"No Material Inspection Requests (MIR) found matching material='{material}'."

    output = [f"🔬 === Material Inspection Requests (MIR / SIR Tracking) ==="]
    for m in matches:
        stat_icon = "✅" if "Approved" in m.status else "❌"
        output.append(
            f"• [{m.mir_number}] {m.material_name} {stat_icon} ({m.status})\n"
            f"  - Supplier: {m.supplier} | BOQ Ref: {m.boq_item_ref}\n"
            f"  - Qty Inspected: {m.quantity_inspected:,.1f} {m.unit}\n"
            f"  - Inspector: {m.inspector} | Date: {m.inspection_date}\n"
            f"  - Comments: {m.comments or 'Compliant with project specification'}"
        )

    return "\n\n".join(output)
