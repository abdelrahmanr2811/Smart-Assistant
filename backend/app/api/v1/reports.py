from fastapi import APIRouter, Depends, Query, Response
from app.services.report_generator import generate_pdf_report, generate_excel_report

router = APIRouter(prefix="/reports", tags=["Reports & Export"])

@router.get("/export/pdf")
def export_executive_pdf(project_id: str = Query(default="PRJ-01")):
    pdf_bytes = generate_pdf_report(project_id=project_id)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=SmartAssistant_Executive_Report_{project_id}.pdf"
        }
    )

@router.get("/export/excel")
def export_executive_excel(project_id: str = Query(default="PRJ-01")):
    excel_bytes = generate_excel_report(project_id=project_id)
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=SmartAssistant_EVM_Dashboard_{project_id}.xlsx"
        }
    )
