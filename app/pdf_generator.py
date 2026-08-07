from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from datetime import datetime


def _list_to_text(items):
    """Convert list to multiline string."""
    if not items:
        return "Not Available"

    return "<br/>".join([f"• {item}" for item in items])


def generate_pdf(
    output_path,
    info,
    prediction,
    confidence
):
    """
    Generate Plant Disease Report PDF.

    Parameters
    ----------
    output_path : str
        Path where PDF will be saved.

    info : dict
        Disease information dictionary.

    prediction : str

    confidence : str
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=(8.27 * inch, 11.69 * inch)
    )

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.darkgreen

    heading_style = styles["Heading2"]
    heading_style.textColor = colors.darkgreen

    normal = styles["BodyText"]

    story = []

    # ==========================================
    # Title
    # ==========================================

    story.append(
        Paragraph(
            "🌿 Smart Agriculture Disease Advisor",
            title_style
        )
    )

    story.append(
        Paragraph(
            "AI Plant Disease Diagnosis Report",
            heading_style
        )
    )

    story.append(Spacer(1, 0.30 * inch))

    # ==========================================
    # Prediction Table
    # ==========================================

    table_data = [

        ["Prediction", prediction],

        ["Confidence", confidence],

        ["Risk Level", info.get("Risk_Level", "-")],

        ["Crop", info.get("Crop", "-")],

        ["Scientific Name", info.get("Scientific_Name", "-")],

        ["Pathogen", info.get("Pathogen", "-")],

        ["Category", info.get("Category", "-")]

    ]

    table = Table(
        table_data,
        colWidths=[2.3 * inch, 4.5 * inch]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (0, -1), colors.darkgreen),

            ("TEXTCOLOR", (0, 0), (0, -1), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (1, 0), (1, -1), colors.beige),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

            ("TOPPADDING", (0, 0), (-1, -1), 8),

            ("VALIGN", (0, 0), (-1, -1), "TOP")

        ])

    )

    story.append(table)

    story.append(Spacer(1, 0.35 * inch))

    # ==========================================
    # Description
    # ==========================================

    story.append(
        Paragraph(
            "Description",
            heading_style
        )
    )

    story.append(
        Paragraph(
            info.get("Description", "Not Available"),
            normal
        )
    )

    story.append(Spacer(1, 0.20 * inch))

    # ==========================================
    # Symptoms
    # ==========================================

    story.append(
        Paragraph(
            "Symptoms",
            heading_style
        )
    )

    story.append(
        Paragraph(
            _list_to_text(
                info.get("Symptoms", [])
            ),
            normal
        )
    )

    story.append(Spacer(1, 0.20 * inch))

    # ==========================================
    # Treatment
    # ==========================================

    story.append(
        Paragraph(
            "Treatment",
            heading_style
        )
    )

    story.append(
        Paragraph(
            _list_to_text(
                info.get("Treatment", [])
            ),
            normal
        )
    )

    story.append(Spacer(1, 0.20 * inch))

    # ==========================================
    # Organic Treatment
    # ==========================================

    story.append(
        Paragraph(
            "Organic Treatment",
            heading_style
        )
    )

    story.append(
        Paragraph(
            _list_to_text(
                info.get("Organic_Treatment", [])
            ),
            normal
        )
    )

    story.append(Spacer(1, 0.20 * inch))

    # ==========================================
    # Chemicals
    # ==========================================

    story.append(
        Paragraph(
            "Recommended Chemicals",
            heading_style
        )
    )

    story.append(
        Paragraph(
            _list_to_text(
                info.get("Recommended_Chemicals", [])
            ),
            normal
        )
    )

    story.append(Spacer(1, 0.20 * inch))

    # ==========================================
    # Prevention
    # ==========================================

    story.append(
        Paragraph(
            "Prevention",
            heading_style
        )
    )

    story.append(
        Paragraph(
            _list_to_text(
                info.get("Prevention", [])
            ),
            normal
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # ==========================================
    # Timeline
    # ==========================================

    story.append(
        Paragraph(
            "Disease Timeline",
            heading_style
        )
    )

    timeline = info.get("Age_Cycle", {})

    timeline_table = Table(

        [

            ["Early", timeline.get("Early", "-")],

            ["Moderate", timeline.get("Moderate", "-")],

            ["Severe", timeline.get("Severe", "-")],

            ["Estimated", timeline.get("Estimated", "-")]

        ],

        colWidths=[2 * inch, 4.8 * inch]

    )

    timeline_table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 0), (0, -1), colors.lightgreen),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8)

        ])

    )

    story.append(timeline_table)

    story.append(Spacer(1, 0.30 * inch))

    # ==========================================
    # Footer
    # ==========================================

    story.append(

        Paragraph(

            f"Generated on : {datetime.now().strftime('%d %B %Y %I:%M %p')}",

            normal

        )

    )

    story.append(

        Paragraph(

            "Generated by Smart Agriculture Disease Advisor",

            normal

        )

    )

    doc.build(story)

    return output_path