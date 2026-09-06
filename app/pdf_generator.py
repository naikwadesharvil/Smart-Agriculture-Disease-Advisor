import os
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as ReportLabImage,
    KeepTogether
)


# ==========================================
# Dynamic Page Numbering & Footer Canvas
# ==========================================

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw total page numbers
    and professional header/footer rules on every page.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#6c757d"))
        
        # A4 portrait: 210mm width x 297mm height
        margin = 18 * mm
        page_width = 210 * mm
        
        # Footer rule line
        self.setStrokeColor(colors.HexColor("#e0e0e0"))
        self.setLineWidth(0.5)
        self.line(margin, 14 * mm, page_width - margin, 14 * mm)
        
        # Footer text
        self.drawString(margin, 9 * mm, "Smart Agriculture Disease Advisor • AI Diagnosis & Advisory Report")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(page_width - margin, 9 * mm, page_text)
        self.restoreState()


# ==========================================
# Helper Functions
# ==========================================

def safe_value(value, default="Not available"):
    """
    Safely format text values, returning 'Not available' for empty/null fields.
    """
    if value is None:
        return default
    if isinstance(value, str):
        cleaned = value.strip()
        if cleaned == "" or cleaned.lower() in ["none", "unknown", "information not available.", "information not available"]:
            return default
        return cleaned
    return str(value)


def safe_list(value):
    """
    Safely extract a list of items from dictionary fields.
    """
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if item is not None and str(item).strip() != ""]
    if isinstance(value, str) and value.strip() != "":
        return [value.strip()]
    return []


# ==========================================
# Generate Complete PDF Report
# ==========================================

def generate_pdf(
    output_path,
    info,
    prediction,
    confidence,
    image_path=None
):
    """
    Generates a professional A4 Portrait plant disease advisory report.
    """
    if not isinstance(info, dict):
        info = {}

    # Total printable width on A4 Portrait (210mm - 2*18mm margins = 174mm)
    printable_width = 174 * mm

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#198754"),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#555555"),
        spaceAfter=12
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#198754"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#212529"),
        spaceAfter=4,
        alignment=TA_JUSTIFY
    )

    bullet_style = ParagraphStyle(
        "ReportBullet",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#212529"),
        leftIndent=12,
        spaceAfter=3
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#198754")
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#212529")
    )

    disclaimer_style = ParagraphStyle(
        "ReportDisclaimer",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#6c757d")
    )

    story = []

    # 1. Header (Title & Subtitle)
    story.append(Paragraph("Smart Agriculture Disease Advisor", title_style))
    story.append(Paragraph("AI-Powered Plant Disease Analysis Report", subtitle_style))
    story.append(Spacer(1, 4))

    # 2. Uploaded Leaf Image (Preserve Aspect Ratio & Constrain Dimensions)
    if image_path and os.path.exists(image_path):
        try:
            with PILImage.open(image_path) as pil_image:
                img_w, img_h = pil_image.size
                max_w = 80 * mm
                max_h = 55 * mm
                scale = min(max_w / img_w, max_h / img_h)
                disp_w = img_w * scale
                disp_h = img_h * scale

            story.append(Paragraph("Uploaded Leaf Image", heading_style))
            leaf_img = ReportLabImage(image_path, width=disp_w, height=disp_h)
            leaf_img.hAlign = "CENTER"
            story.append(leaf_img)
            story.append(Spacer(1, 6))
        except Exception as img_err:
            print("⚠️ Note: Could not render image in PDF:", img_err)

    # 3. Prediction Summary Table
    story.append(Paragraph("Prediction Summary", heading_style))
    summary_rows = [
        [Paragraph("<b>Predicted Disease</b>", table_header_style), Paragraph(safe_value(prediction), table_cell_style)],
        [Paragraph("<b>Confidence</b>", table_header_style), Paragraph(safe_value(confidence), table_cell_style)],
        [Paragraph("<b>Crop</b>", table_header_style), Paragraph(safe_value(info.get("Crop")), table_cell_style)],
        [Paragraph("<b>Scientific Name</b>", table_header_style), Paragraph(safe_value(info.get("Scientific_Name")), table_cell_style)],
        [Paragraph("<b>Pathogen Type</b>", table_header_style), Paragraph(safe_value(info.get("Pathogen_Type")), table_cell_style)],
        [Paragraph("<b>Risk Level</b>", table_header_style), Paragraph(safe_value(info.get("Risk_Level")), table_cell_style)],
        [Paragraph("<b>Severity</b>", table_header_style), Paragraph(safe_value(info.get("Severity")), table_cell_style)]
    ]

    summary_table = Table(summary_rows, colWidths=[52 * mm, 122 * mm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eaf7ef")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdcdc")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4)
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 6))

    # 4. Disease Description
    story.append(Paragraph("Disease Description", heading_style))
    story.append(Paragraph(safe_value(info.get("Description")), body_style))
    story.append(Spacer(1, 4))

    # 5. Disease Profile
    story.append(Paragraph("Disease Profile", heading_style))
    profile_rows = [
        [Paragraph("<b>Pathogen</b>", table_header_style), Paragraph(safe_value(info.get("Pathogen")), table_cell_style)],
        [Paragraph("<b>Category</b>", table_header_style), Paragraph(safe_value(info.get("Category")), table_cell_style)],
        [Paragraph("<b>Affected Part</b>", table_header_style), Paragraph(safe_value(info.get("Affected_Part")), table_cell_style)],
        [Paragraph("<b>Environment</b>", table_header_style), Paragraph(safe_value(info.get("Environment")), table_cell_style)],
        [Paragraph("<b>Spread</b>", table_header_style), Paragraph(safe_value(info.get("Spread")), table_cell_style)]
    ]

    profile_table = Table(profile_rows, colWidths=[52 * mm, 122 * mm])
    profile_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f8f9fa")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdcdc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4)
    ]))
    story.append(profile_table)
    story.append(Spacer(1, 6))

    # Helper function to append structured bullet point sections
    def append_bullet_section(title, items, empty_msg="Not available"):
        story.append(Paragraph(title, heading_style))
        if items:
            for item in items:
                story.append(Paragraph(f"• {safe_value(item)}", bullet_style))
        else:
            story.append(Paragraph(empty_msg, body_style))
        story.append(Spacer(1, 4))

    # 6. Symptoms
    append_bullet_section("Symptoms", safe_list(info.get("Symptoms")), "No specific symptoms reported.")

    # 7. Causes
    append_bullet_section("Causes", safe_list(info.get("Cause")), "No specific cause factors recorded.")

    # 8. Treatment
    append_bullet_section("Treatment", safe_list(info.get("Treatment")), "No specific treatment methods recorded.")

    # 9. Organic Treatment
    append_bullet_section("Organic Treatment", safe_list(info.get("Organic_Treatment")), "No specific organic remedies recorded.")

    # 10. Recommended Chemicals
    append_bullet_section("Recommended Chemicals", safe_list(info.get("Recommended_Chemicals")), "No chemical recommendations recorded.")

    # 11. Prevention
    append_bullet_section("Prevention", safe_list(info.get("Prevention")), "No prevention guidelines recorded.")

    # 12. Recommended Actions
    append_bullet_section("Recommended Actions", safe_list(info.get("Recommended_Actions")), "No immediate actions recorded.")

    # 13. Disease Progression Table
    age_cycle = info.get("Age_Cycle") if isinstance(info.get("Age_Cycle"), dict) else {}
    story.append(Paragraph("Disease Progression", heading_style))
    progression_rows = [
        [
            Paragraph("<b>Stage</b>", ParagraphStyle("H1", parent=table_header_style, textColor=colors.white)),
            Paragraph("<b>Estimated Information</b>", ParagraphStyle("H2", parent=table_cell_style, fontName="Helvetica-Bold", textColor=colors.white))
        ],
        [Paragraph("<b>Early</b>", table_cell_style), Paragraph(safe_value(age_cycle.get("Early")), table_cell_style)],
        [Paragraph("<b>Moderate</b>", table_cell_style), Paragraph(safe_value(age_cycle.get("Moderate")), table_cell_style)],
        [Paragraph("<b>Severe</b>", table_cell_style), Paragraph(safe_value(age_cycle.get("Severe")), table_cell_style)],
        [Paragraph("<b>Estimated Duration</b>", table_cell_style), Paragraph(safe_value(age_cycle.get("Estimated")), table_cell_style)]
    ]

    progression_table = Table(progression_rows, colWidths=[45 * mm, 129 * mm])
    progression_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#198754")),
        ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#f8f9fa")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdcdc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4)
    ]))
    story.append(progression_table)
    story.append(Spacer(1, 10))

    # 14. Disclaimer
    story.append(Paragraph(
        "<b>Disclaimer:</b> This report provides AI-generated plant pathology decision-support guidance. "
        "Diagnostic predictions and chemical recommendations should be confirmed by a certified agronomist or extension officer "
        "before large-scale field application.",
        disclaimer_style
    ))

    # Build PDF with dynamic page numbering
    document.build(story, canvasmaker=NumberedCanvas)