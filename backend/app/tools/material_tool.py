from typing import Optional
from langchain_core.tools import tool
from sqlmodel import Session, select
from app.core.database import engine
from app.models.db_models import MaterialLogRecord
from app.core.rag_engine import rag_engine

@tool
def query_material_log(material_name: str = "", date: Optional[str] = None) -> str:
    """
    Searches incoming site delivery logs, BOQ tracking, and delivery notes.
    Returns Material Description, Delivery Date, Delivery Note Number, Quantity,
    Supplier, and Site Inspection Status (Passed/Pending/Rejected).
    """
    with Session(engine) as session:
        logs = session.exec(select(MaterialLogRecord)).all()

    mat_lower = (material_name or "").lower().strip()
    date_clean = (date or "").strip()

    matches = []
    for m in logs:
        match = True
        if mat_lower and mat_lower not in m.material_description.lower() and mat_lower not in m.supplier.lower():
            match = False
        if date_clean and date_clean != m.delivery_date:
            match = False
        
        if match:
            matches.append(m)

    if not matches:
        # Fallback to ChromaDB search
        chroma_res = rag_engine.query_collection("materials_collection", f"{material_name} {date or ''}".strip(), n_results=3)
        if chroma_res:
            res_text = "\n".join([f"• {c['content']}" for c in chroma_res])
            return f"=== Material Delivery Log (Vector Search) ===\n{res_text}"
        return f"No material delivery records found matching '{material_name}' (date: {date or 'any'})."

    output = ["📦 === Site Material & Delivery Log Results ==="]
    for item in matches:
        status_symbol = "✅" if item.inspection_status == "Passed" else ("⏳" if item.inspection_status == "Pending" else "❌")
        output.append(
            f"• Description: {item.material_description}\n"
            f"  - Delivery Note: {item.delivery_note_number}\n"
            f"  - Date: {item.delivery_date}\n"
            f"  - Quantity: {item.quantity:,.1f} {item.unit}\n"
            f"  - Supplier: {item.supplier}\n"
            f"  - Inspection Status: {status_symbol} {item.inspection_status}\n"
            f"  - Notes: {item.notes or 'None'}"
        )

    return "\n\n".join(output)
