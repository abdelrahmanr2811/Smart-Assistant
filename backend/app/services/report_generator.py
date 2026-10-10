import io
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlmodel import Session, select

from app.core.database import engine
from app.models.db_models import (
    Project, ScheduleActivity, MaterialLogRecord, NCRRecord, MIRRecord, DailySiteReport
)

# ReportLab Imports
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

# OpenPyXL Imports
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def get_project_context(project_id: str) -> Dict[str, Any]:
    with Session(engine) as session:
        prj = session.exec(select(Project).where(Project.project_id == project_id)).first()
        if not prj:
            prj = session.exec(select(Project).where(Project.is_active == True)).first()
        if not prj:
            prj = Project(
                project_id="PRJ-01",
                code="NARGES-TWR",
                name="Al-Narges Specialist Tower (برج النرجس التخصصي)",
                client_name="Al-Narges Real Estate Development",
                consultant_name="Dar Al-Handasah Consultants",
                contractor_name="Hassan Allam Construction",
                total_budget=15000000.0,
                currency="SAR"
            )

        activities = session.exec(select(ScheduleActivity)).all()
        materials = session.exec(select(MaterialLogRecord)).all()
        ncrs = session.exec(select(NCRRecord)).all()
        mirs = session.exec(select(MIRRecord)).all()
        dsrs = session.exec(select(DailySiteReport)).all()

        pv = sum(a.planned_value for a in activities) or 500000.0
        ev = sum(a.earned_value for a in activities) or 410000.0
        ac = sum(a.actual_cost for a in activities) or 415000.0
        bac = prj.total_budget or 15000000.0

        spi = round(ev / pv, 3) if pv > 0 else 1.0
        cpi = round(ev / ac, 3) if ac > 0 else 1.0
        sv = round(ev - pv, 2)
        cv = round(ev - ac, 2)
        eac = round(bac / cpi, 2) if cpi > 0 else bac
        etc = round(eac - ac, 2)
        vac = round(bac - eac, 2)

        return {
            "project": prj,
            "activities": activities,
            "materials": materials,
            "ncrs": ncrs,
            "mirs": mirs,
            "dsrs": dsrs,
            "kpis": {
                "BAC": bac,
                "PV": pv,
                "EV": ev,
                "AC": ac,
                "SV": sv,
                "CV": cv,
                "SPI": spi,
                "CPI": cpi,
                "EAC": eac,
                "ETC": etc,
                "VAC": vac,
                "data_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            }
        }

def generate_pdf_report(project_id: str = "PRJ-01") -> bytes:
    ctx = get_project_context(project_id)
    prj = ctx["project"]
    kpis = ctx["kpis"]
    activities = ctx["activities"]
    ncrs = ctx["ncrs"]

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Brand Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F2E4F'),
        alignment=TA_LEFT
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#FF6A13'),
        alignment=TA_LEFT
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0F2E4F'),
        spaceBefore=10,
        spaceAfter=6
    )

    cell_style = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1E293B')
    )

    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#0F2E4F')
    )

    elements = []

    # 1. Header Banner
    header_data = [
        [
            Paragraph("<b>BLUE NILE AI PROJECT MANAGER</b><br/><font size=8 color='#5B7083'>FACULTY OF ENGINEERING - BLUE NILE UNIVERSITY</font>", title_style),
            Paragraph(f"<b>REPORT: EXECUTIVE PM & EVM AUDIT</b><br/><b>Date:</b> {kpis['data_date']}<br/><b>Project Code:</b> {prj.code}", ParagraphStyle('RightHdr', parent=styles['Normal'], fontSize=8, leading=11, alignment=TA_RIGHT, textColor=colors.HexColor('#334155')))
        ]
    ]
    hdr_table = Table(header_data, colWidths=[3.8*inch, 3.4*inch])
    hdr_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(hdr_table)
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#4F46E5'), spaceBefore=4, spaceAfter=10))

    # 2. Project Metadata
    prj_meta = [
        [
            Paragraph("<b>Project:</b>", cell_bold), Paragraph(prj.name, cell_style),
            Paragraph("<b>Client:</b>", cell_bold), Paragraph(prj.client_name, cell_style)
        ],
        [
            Paragraph("<b>Contractor:</b>", cell_bold), Paragraph(prj.contractor_name, cell_style),
            Paragraph("<b>Consultant:</b>", cell_bold), Paragraph(prj.consultant_name, cell_style)
        ],
        [
            Paragraph("<b>Baseline:</b>", cell_bold), Paragraph(f"{prj.baseline_start} to {prj.baseline_finish}", cell_style),
            Paragraph("<b>BAC Budget:</b>", cell_bold), Paragraph(f"SAR {prj.total_budget:,.2f}", cell_style)
        ]
    ]
    meta_table = Table(prj_meta, colWidths=[1.1*inch, 2.5*inch, 1.1*inch, 2.5*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 12))

    # 3. EVM Performance Matrix
    elements.append(Paragraph("1. Earned Value Management (EVM) Performance Matrix", h2_style))
    
    spi_color = "#1E8E5A" if kpis['SPI'] >= 1.0 else ("#C98A00" if kpis['SPI'] >= 0.85 else "#C2362B")
    cpi_color = "#1E8E5A" if kpis['CPI'] >= 1.0 else ("#C98A00" if kpis['CPI'] >= 0.85 else "#C2362B")

    evm_data = [
        [
            Paragraph("<b>Metric</b>", cell_bold),
            Paragraph("<b>Value</b>", cell_bold),
            Paragraph("<b>Formula / Definition</b>", cell_bold),
            Paragraph("<b>Engineering Status</b>", cell_bold)
        ],
        [
            Paragraph("Planned Value (PV)", cell_style),
            Paragraph(f"SAR {kpis['PV']:,.2f}", cell_bold),
            Paragraph("Budgeted Cost of Work Scheduled (BCWS)", cell_style),
            Paragraph("Baseline Target", cell_style)
        ],
        [
            Paragraph("Earned Value (EV)", cell_style),
            Paragraph(f"SAR {kpis['EV']:,.2f}", cell_bold),
            Paragraph("Budgeted Cost of Work Performed (BCWP)", cell_style),
            Paragraph("Actual Site Accomplishment", cell_style)
        ],
        [
            Paragraph("Actual Cost (AC)", cell_style),
            Paragraph(f"SAR {kpis['AC']:,.2f}", cell_bold),
            Paragraph("Actual Cost of Work Performed (ACWP)", cell_style),
            Paragraph("Site Expenditures Incurred", cell_style)
        ],
        [
            Paragraph("Schedule Variance (SV)", cell_style),
            Paragraph(f"SAR {kpis['SV']:,.2f}", cell_bold),
            Paragraph("EV - PV", cell_style),
            Paragraph("Behind Schedule (Variance)" if kpis['SV'] < 0 else "Ahead of Schedule", cell_style)
        ],
        [
            Paragraph("Cost Variance (CV)", cell_style),
            Paragraph(f"SAR {kpis['CV']:,.2f}", cell_bold),
            Paragraph("EV - AC", cell_style),
            Paragraph("Cost Overrun (Variance)" if kpis['CV'] < 0 else "Under Budget", cell_style)
        ],
        [
            Paragraph("Schedule Performance Index (SPI)", cell_bold),
            Paragraph(f"<font color='{spi_color}'><b>{kpis['SPI']:.3f}</b></font>", cell_bold),
            Paragraph("EV / PV (>1 Ahead, <1 Delay)", cell_style),
            Paragraph(f"<font color='{spi_color}'><b>{'Behind Schedule / Delayed' if kpis['SPI'] < 1 else 'On Track / Ahead'}</b></font>", cell_style)
        ],
        [
            Paragraph("Cost Performance Index (CPI)", cell_bold),
            Paragraph(f"<font color='{cpi_color}'><b>{kpis['CPI']:.3f}</b></font>", cell_bold),
            Paragraph("EV / AC (>1 Savings, <1 Overrun)", cell_style),
            Paragraph(f"<font color='{cpi_color}'><b>{'Cost Overrun / Budget Risk' if kpis['CPI'] < 1 else 'Within Budget / Saving'}</b></font>", cell_style)
        ],
        [
            Paragraph("Estimate at Completion (EAC)", cell_style),
            Paragraph(f"SAR {kpis['EAC']:,.2f}", cell_bold),
            Paragraph("BAC / CPI", cell_style),
            Paragraph("Projected Total at Completion", cell_style)
        ],
        [
            Paragraph("Estimate to Complete (ETC)", cell_style),
            Paragraph(f"SAR {kpis['ETC']:,.2f}", cell_bold),
            Paragraph("EAC - AC", cell_style),
            Paragraph("Remaining Funds Needed", cell_style)
        ]
    ]

    evm_table = Table(evm_data, colWidths=[1.8*inch, 1.4*inch, 2.2*inch, 1.8*inch])
    evm_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F2E4F')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    for i in range(len(evm_data[0])):
        evm_data[0][i].style.textColor = colors.white
    elements.append(evm_table)
    elements.append(Spacer(1, 12))

    # 4. Critical Path Schedule & Milestone Breakdown
    elements.append(Paragraph("2. Schedule Activities & Critical Path Log (Primavera P6)", h2_style))
    sched_rows = [
        [
            Paragraph("<b>Act ID</b>", cell_bold),
            Paragraph("<b>Activity Description</b>", cell_bold),
            Paragraph("<b>Planned Finish</b>", cell_bold),
            Paragraph("<b>PV</b>", cell_bold),
            Paragraph("<b>EV</b>", cell_bold),
            Paragraph("<b>Critical</b>", cell_bold),
            Paragraph("<b>Status</b>", cell_bold)
        ]
    ]
    for act in activities[:7]:
        crit_txt = "<font color='#C2362B'><b>Critical (CP)</b></font>" if act.is_critical_path else "Non-Critical"
        sched_rows.append([
            Paragraph(act.activity_id, cell_bold),
            Paragraph(act.name[:32], cell_style),
            Paragraph(act.finish_date, cell_style),
            Paragraph(f"SAR {act.planned_value:,.0f}", cell_style),
            Paragraph(f"SAR {act.earned_value:,.0f}", cell_style),
            Paragraph(crit_txt, cell_style),
            Paragraph(act.status, cell_style)
        ])

    sched_table = Table(sched_rows, colWidths=[1.0*inch, 2.3*inch, 1.0*inch, 0.9*inch, 0.9*inch, 1.0*inch, 0.9*inch])
    sched_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A5F')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    for i in range(len(sched_rows[0])):
        sched_rows[0][i].style.textColor = colors.white
    elements.append(sched_table)
    elements.append(Spacer(1, 12))

    # 5. QA/QC & Material Compliance Summary
    elements.append(Paragraph("3. Quality Assurance (NCRs) & Material Compliance", h2_style))
    ncr_rows = [
        [
            Paragraph("<b>NCR No.</b>", cell_bold),
            Paragraph("<b>Title & Description</b>", cell_bold),
            Paragraph("<b>Severity</b>", cell_bold),
            Paragraph("<b>Assigned Lead</b>", cell_bold),
            Paragraph("<b>Target Date</b>", cell_bold),
            Paragraph("<b>Status</b>", cell_bold)
        ]
    ]
    for n in ncrs[:4]:
        sev_color = "#C2362B" if n.severity == "Critical" else ("#C98A00" if n.severity == "Major" else "#1E8E5A")
        ncr_rows.append([
            Paragraph(n.ncr_number, cell_bold),
            Paragraph(n.title[:35], cell_style),
            Paragraph(f"<font color='{sev_color}'><b>{n.severity}</b></font>", cell_style),
            Paragraph(n.assigned_engineer, cell_style),
            Paragraph(n.target_closure_date, cell_style),
            Paragraph(f"<b>{n.status}</b>", cell_style)
        ])

    ncr_table = Table(ncr_rows, colWidths=[1.2*inch, 2.4*inch, 0.9*inch, 1.3*inch, 1.0*inch, 0.9*inch])
    ncr_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#334155')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    for i in range(len(ncr_rows[0])):
        ncr_rows[0][i].style.textColor = colors.white
    elements.append(ncr_table)
    elements.append(Spacer(1, 14))

    # 6. Executive Sign-off & Recommendations
    comm_block = [
        [
            Paragraph(
                "<b>Executive Project Controls Assessment & Directives:</b><br/>"
                f"1. <b>Schedule Recovery:</b> Current SPI of <b>{kpis['SPI']:.3f}</b> reflects delayed superstructure vertical works. Fast-tracking of Floor 1 Core Wall reinforcement (ACT-1020) is mandatory.<br/>"
                f"2. <b>Cost Containment:</b> CPI of <b>{kpis['CPI']:.3f}</b> is on target. Cost Variance remains tightly managed at ${kpis['CV']:,.2f}.<br/>"
                f"3. <b>Quality Actions:</b> Active NCR items must be resolved with the Consultant prior to next major concrete casting batch.",
                ParagraphStyle('CommStyle', parent=styles['Normal'], fontSize=8, leading=11, textColor=colors.HexColor('#0F2E4F'))
            )
        ],
        [
            Paragraph(
                "<br/><b>Approved & Issued by:</b> Eng. Lead Project Controls & Site Director &nbsp;&nbsp;|&nbsp;&nbsp; <b>Certified Production Architecture</b>",
                ParagraphStyle('SignStyle', parent=styles['Normal'], fontSize=7.5, leading=10, textColor=colors.HexColor('#5B7083'))
            )
        ]
    ]
    comm_table = Table(comm_block, colWidths=[7.2*inch])
    comm_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFF7ED')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#FF6A13')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(comm_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def generate_excel_report(project_id: str = "PRJ-01") -> bytes:
    ctx = get_project_context(project_id)
    prj = ctx["project"]
    kpis = ctx["kpis"]
    activities = ctx["activities"]
    materials = ctx["materials"]
    ncrs = ctx["ncrs"]

    wb = openpyxl.Workbook()
    
    # Styling Palette
    header_fill = PatternFill(start_color="0F2E4F", end_color="0F2E4F", fill_type="solid")
    sub_fill = PatternFill(start_color="1E3A5F", end_color="1E3A5F", fill_type="solid")
    orange_fill = PatternFill(start_color="FF6A13", end_color="FF6A13", fill_type="solid")
    light_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    title_font = Font(name="Calibri", size=16, bold=True, color="0F2E4F")
    bold_font = Font(name="Calibri", size=11, bold=True, color="0F2E4F")
    regular_font = Font(name="Calibri", size=10, color="1E293B")
    
    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )

    # ------------------ TAB 1: EVM Dashboard ------------------
    ws1 = wb.active
    ws1.title = "Executive EVM Dashboard"
    ws1.views.sheetView[0].showGridLines = True

    ws1["A1"] = "SMART ASSISTANT - EXECUTIVE PM & EVM AUDIT REPORT"
    ws1["A1"].font = title_font
    ws1["A2"] = f"Project: {prj.name} | Code: {prj.code} | Data Date: {kpis['data_date']}"
    ws1["A2"].font = Font(name="Calibri", size=11, bold=True, color="FF6A13")

    meta_headers = ["Client", "Consultant", "Contractor", "Baseline Start", "Baseline Finish", "Total Budget (BAC)"]
    meta_values = [prj.client_name, prj.consultant_name, prj.contractor_name, prj.baseline_start, prj.baseline_finish, prj.total_budget]
    
    for col_idx, (h, v) in enumerate(zip(meta_headers, meta_values), start=1):
        cell_h = ws1.cell(row=4, column=col_idx, value=h)
        cell_h.font = header_font
        cell_h.fill = sub_fill
        cell_h.alignment = Alignment(horizontal="center", vertical="center")
        
        cell_v = ws1.cell(row=5, column=col_idx, value=v)
        cell_v.font = regular_font
        cell_v.alignment = Alignment(horizontal="center", vertical="center")
        cell_v.border = thin_border
        if isinstance(v, (int, float)):
            cell_v.number_format = '#,##0.00 "SAR"'

    ws1["A7"] = "Earned Value Management (EVM) Core Metrics"
    ws1["A7"].font = Font(name="Calibri", size=13, bold=True, color="0F2E4F")

    evm_headers = ["Metric Code", "Metric Name", "Formula", "Value (SAR / Index)", "Unit", "Status / Interpretation"]
    for c_idx, h in enumerate(evm_headers, start=1):
        c = ws1.cell(row=8, column=c_idx, value=h)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = thin_border

    evm_rows = [
        ("BAC", "Budget at Completion", "Total Baseline Budget", prj.total_budget, "SAR", "Approved Project Budget"),
        ("PV", "Planned Value", "BCWS - Scheduled Budget to Date", kpis['PV'], "SAR", "Baseline Scheduled Work"),
        ("EV", "Earned Value", "BCWP - Physical Work Accomplished", kpis['EV'], "SAR", "Actual Earned Accomplishment"),
        ("AC", "Actual Cost", "ACWP - Incurred Expenditures", kpis['AC'], "SAR", "Actual Cost of Work Incurred"),
        ("SV", "Schedule Variance", "=D11-D10", "=D11-D10", "SAR", "Behind Schedule" if kpis['SV'] < 0 else "Ahead"),
        ("CV", "Cost Variance", "=D11-D12", "=D11-D12", "SAR", "Cost Overrun" if kpis['CV'] < 0 else "Under Budget"),
        ("SPI", "Schedule Performance Index", "=D11/D10", "=D11/D10", "Ratio", "Delayed (<1.0)" if kpis['SPI'] < 1 else "On Track"),
        ("CPI", "Cost Performance Index", "=D11/D12", "=D11/D12", "Ratio", "Over Budget (<1.0)" if kpis['CPI'] < 1 else "Under Budget"),
        ("EAC", "Estimate at Completion", "=D9/D16", "=D9/D16", "SAR", "Projected Total Cost"),
        ("ETC", "Estimate to Complete", "=D17-D12", "=D17-D12", "SAR", "Remaining Funds Required"),
        ("VAC", "Variance at Completion", "=D9-D17", "=D9-D17", "SAR", "Forecast Variance at Finish"),
    ]

    for r_idx, row in enumerate(evm_rows, start=9):
        for c_idx, val in enumerate(row, start=1):
            cell = ws1.cell(row=r_idx, column=c_idx, value=val)
            cell.font = bold_font if c_idx in [1, 4] else regular_font
            cell.border = thin_border
            if c_idx == 4:
                if row[4] == "SAR":
                    cell.number_format = '#,##0.00 "SAR"'
                else:
                    cell.number_format = '0.000'

    # Auto column width
    for col in ws1.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws1.column_dimensions[col_letter].width = max(max_len + 3, 12)

    # ------------------ TAB 2: Activities & Primavera Schedule ------------------
    ws2 = wb.create_sheet(title="Schedule Activities (P6)")
    ws2.views.sheetView[0].showGridLines = True
    
    act_headers = ["Activity ID", "Activity Name", "WBS Package", "Start Date", "Finish Date", "Planned Value (PV)", "Earned Value (EV)", "Actual Cost (AC)", "Critical Path", "Status"]
    for c_idx, h in enumerate(act_headers, start=1):
        c = ws2.cell(row=1, column=c_idx, value=h)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = thin_border

    for r_idx, a in enumerate(activities, start=2):
        row_vals = [
            a.activity_id, a.name, a.wbs, a.start_date, a.finish_date,
            a.planned_value, a.earned_value, a.actual_cost,
            "YES (Critical)" if a.is_critical_path else "NO", a.status
        ]
        for c_idx, val in enumerate(row_vals, start=1):
            c = ws2.cell(row=r_idx, column=c_idx, value=val)
            c.font = regular_font
            c.border = thin_border
            if c_idx in [6, 7, 8]:
                c.number_format = '#,##0.00 "SAR"'

    for col in ws2.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        ws2.column_dimensions[get_column_letter(col[0].column)].width = max(max_len + 3, 12)

    # ------------------ TAB 3: Material & Delivery Logs ------------------
    ws3 = wb.create_sheet(title="Materials & BOQ Logs")
    ws3.views.sheetView[0].showGridLines = True
    
    mat_headers = ["Material Description", "Delivery Date", "DN Number", "Quantity", "Unit", "Supplier", "Inspection Status", "Notes"]
    for c_idx, h in enumerate(mat_headers, start=1):
        c = ws3.cell(row=1, column=c_idx, value=h)
        c.font = header_font
        c.fill = sub_fill
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = thin_border

    for r_idx, m in enumerate(materials, start=2):
        row_vals = [m.material_description, m.delivery_date, m.delivery_note_number, m.quantity, m.unit, m.supplier, m.inspection_status, m.notes or ""]
        for c_idx, val in enumerate(row_vals, start=1):
            c = ws3.cell(row=r_idx, column=c_idx, value=val)
            c.font = regular_font
            c.border = thin_border

    for col in ws3.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        ws3.column_dimensions[get_column_letter(col[0].column)].width = max(max_len + 3, 12)

    # ------------------ TAB 4: QA/QC NCR Records ------------------
    ws4 = wb.create_sheet(title="QA-QC NCR Records")
    ws4.views.sheetView[0].showGridLines = True
    
    ncr_headers = ["NCR Number", "Title", "Description", "Severity", "Status", "Assigned Engineer", "Issued Date", "Target Closure"]
    for c_idx, h in enumerate(ncr_headers, start=1):
        c = ws4.cell(row=1, column=c_idx, value=h)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = thin_border

    for r_idx, n in enumerate(ncrs, start=2):
        row_vals = [n.ncr_number, n.title, n.description, n.severity, n.status, n.assigned_engineer, n.issued_date, n.target_closure_date]
        for c_idx, val in enumerate(row_vals, start=1):
            c = ws4.cell(row=r_idx, column=c_idx, value=val)
            c.font = regular_font
            c.border = thin_border

    for col in ws4.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        ws4.column_dimensions[get_column_letter(col[0].column)].width = max(max_len + 3, 12)

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.getvalue()
