from typing import Optional
from langchain_core.tools import tool
from sqlmodel import Session, select
from app.core.database import engine
from app.models.db_models import StaffRecord
from app.core.rag_engine import rag_engine

@tool
def query_staff_directory(role: str = "", query: str = "") -> str:
    """
    Query the construction project staff directory.
    Filters metadata by role or fuzzy-matches team member attributes
    (Full Name, Title, Department, Phone, Email, Reporting Manager).
    """
    results = []
    
    with Session(engine) as session:
        statement = select(StaffRecord)
        staff_list = session.exec(statement).all()
        
        # Keyword & fuzzy matching
        q_lower = (query or "").lower().strip()
        role_lower = (role or "").lower().strip()
        
        for staff in staff_list:
            match = False
            
            # Check role match
            if role_lower:
                if role_lower in staff.title.lower() or role_lower in staff.department.lower():
                    match = True
            
            # Check general query match
            if q_lower:
                if (q_lower in staff.full_name.lower() or
                    q_lower in staff.title.lower() or
                    q_lower in staff.department.lower() or
                    q_lower in staff.email.lower() or
                    q_lower in staff.phone.lower() or
                    (staff.skills and q_lower in staff.skills.lower()) or
                    (staff.reporting_manager and q_lower in staff.reporting_manager.lower())):
                    match = True
            
            # If neither filter was given, match all
            if not role_lower and not q_lower:
                match = True
                
            if match:
                results.append(
                    f"• Name: {staff.full_name}\n"
                    f"  Title: {staff.title}\n"
                    f"  Department: {staff.department}\n"
                    f"  Phone: {staff.phone}\n"
                    f"  Email: {staff.email}\n"
                    f"  Manager: {staff.reporting_manager or 'N/A'}\n"
                    f"  Key Skills: {staff.skills or 'N/A'}"
                )

    # If nothing found in SQLite, fallback to semantic search in ChromaDB staff_collection
    if not results:
        chroma_res = rag_engine.query_collection("staff_collection", f"{role} {query}".strip(), n_results=3)
        for c in chroma_res:
            results.append(f"• {c['content']}")

    if not results:
        return f"No staff member found matching role='{role}' or query='{query}'."

    return "=== Staff Directory Results ===\n" + "\n\n".join(results)
