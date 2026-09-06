from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image as ReportLabImage
)

import os
from PIL import Image as PILImage


# ==========================================
# Helper Functions
# ==========================================

def safe_value(value, default="Information not available."):
    """
    Safely convert a value into printable text.
    """

    if value is None:
        return default

    if isinstance(value, str):

        if value.strip() == "":
            return default

        return value

    return str(value)


def safe_list(value):
    """
    Safely convert a database value into a list.
    """

    if value is None:
        return []

    if isinstance(value, list):
        return value

    return [value]


# ==========================================
# Generate PDF Report
# ==========================================

def generate_pdf(
    output_path,
    info,
    prediction,
    confidence,
    image_path=None
):

    # ==========================================
    # Document
    # ==========================================

    document = SimpleDocTemplate(

        output_path,

        pagesize=A4,

        rightMargin=18 * mm,

        leftMargin=18 * mm,

        topMargin=18 * mm,

        bottomMargin=18 * mm

    )


    # ==========================================
    # Styles
    # ==========================================

    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(

        "ReportTitle",

        parent=styles["Title"],

        alignment=TA_CENTER,

        fontSize=20,

        leading=24,

        textColor=colors.HexColor(
            "#198754"
        ),

        spaceAfter=12

    )


    heading_style = ParagraphStyle(

        "ReportHeading",

        parent=styles["Heading2"],

        fontSize=14,

        leading=18,

        textColor=colors.HexColor(
            "#198754"
        ),

        spaceBefore=12,

        spaceAfter=8

    )


    normal_style = ParagraphStyle(

        "ReportNormal",

        parent=styles["BodyText"],

        fontSize=9.5,

        leading=14,

        spaceAfter=6

    )


    small_style = ParagraphStyle(

        "ReportSmall",

        parent=styles["BodyText"],

        fontSize=8,

        leading=11,

        textColor=colors.HexColor(
            "#666666"
        )

    )


    # ==========================================
    # Story
    # ==========================================

    story = []

    # ==========================================
    # Header
    # ==========================================

    story.append(
        Paragraph(
            "Smart Agriculture Disease Advisor",
            title_style
        )
    )

    story.append(
        Paragraph(
            "AI-Powered Plant Disease Analysis Report",
            ParagraphStyle(
                "Subtitle",
                parent=normal_style,
                alignment=TA_CENTER,
                textColor=colors.HexColor(
                    "#666666"
                )
            )
        )
    )

    story.append(
        Spacer(1, 8)
    )

    # ==========================================
    # Uploaded Leaf Image
    # ==========================================

    if not isinstance(info, dict):
        info = {}

    if image_path and os.path.exists(image_path):
        try:
            with PILImage.open(image_path) as pil_image:
                image_width, image_height = pil_image.size
                max_width = 90 * mm
                max_height = 70 * mm
                scale = min(max_width / image_width, max_height / image_height)
                display_width = image_width * scale
                display_height = image_height * scale

            story.append(Paragraph("Uploaded Leaf Image", heading_style))
            leaf_image = ReportLabImage(image_path, width=display_width, height=display_height)
            story.append(leaf_image)
            story.append(Spacer(1, 10))
        except Exception as image_error:
            print("⚠️ Could not add uploaded image to PDF:", image_error)

    story.append(Paragraph("Prediction Summary", heading_style))

    summary_data = [

        [
            Paragraph(
                "<b>Predicted Disease</b>",
                normal_style
            ),

            Paragraph(
                safe_value(
                    prediction
                ),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Confidence</b>",
                normal_style
            ),

            Paragraph(
                safe_value(
                    confidence
                ),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Crop</b>",
                normal_style
            ),

            Paragraph(
                safe_value(
                    info.get("Crop")
                ),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Scientific Name</b>",
                normal_style
            ),

            Paragraph(
                safe_value(
                    info.get(
                        "Scientific_Name"
                    )
                ),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Pathogen Type</b>",
                normal_style
            ),

            Paragraph(
                safe_value(
                    info.get(
                        "Pathogen_Type"
                    )
                ),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Risk Level</b>",
                normal_style
            ),

            Paragraph(
                safe_value(
                    info.get(
                        "Risk_Level"
                    )
                ),
                normal_style
            )
        ],

        [
            Paragraph(
                "<b>Severity</b>",
                normal_style
            ),

            Paragraph(
                safe_value(
                    info.get(
                        "Severity"
                    )
                ),
                normal_style
            )
        ]

    ]


    summary_table = Table(

        summary_data,

        colWidths=[
            55 * mm,
            110 * mm
        ]

    )


    summary_table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor(
                    "#eaf7ef"
                )
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor(
                    "#dddddd"
                )
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )

        ])

    )


    story.append(
        summary_table
    )


    # ==========================================
    # Disease Description
    # ==========================================

    story.append(

        Paragraph(
            "Disease Description",
            heading_style
        )

    )


    story.append(

        Paragraph(
            safe_value(
                info.get(
                    "Description"
                )
            ),
            normal_style
        )

    )


    # ==========================================
    # Disease Profile
    # ==========================================

    story.append(

        Paragraph(
            "Disease Profile",
            heading_style
        )

    )


    profile_data = [

        [
            "<b>Pathogen</b>",
            safe_value(
                info.get(
                    "Pathogen"
                )
            )
        ],

        [
            "<b>Category</b>",
            safe_value(
                info.get(
                    "Category"
                )
            )
        ],

        [
            "<b>Affected Part</b>",
            safe_value(
                info.get(
                    "Affected_Part"
                )
            )
        ],

        [
            "<b>Environment</b>",
            safe_value(
                info.get(
                    "Environment"
                )
            )
        ],

        [
            "<b>Spread</b>",
            safe_value(
                info.get(
                    "Spread"
                )
            )
        ]

    ]


    profile_table = Table(

        [

            [
                Paragraph(
                    row[0],
                    normal_style
                ),

                Paragraph(
                    row[1],
                    normal_style
                )

            ]

            for row in profile_data

        ],

        colWidths=[
            55 * mm,
            110 * mm
        ]

    )


    profile_table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor(
                    "#f5f5f5"
                )
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor(
                    "#dddddd"
                )
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])

    )


    story.append(
        profile_table
    )


    # ==========================================
    # Symptoms
    # ==========================================

    symptoms = safe_list(
        info.get(
            "Symptoms"
        )
    )


    story.append(

        Paragraph(
            "Symptoms",
            heading_style
        )

    )


    if symptoms:

        for symptom in symptoms:

            story.append(

                Paragraph(
                    "• "
                    + safe_value(
                        symptom
                    ),
                    normal_style
                )

            )

    else:

        story.append(

            Paragraph(
                "No symptom information available.",
                normal_style
            )

        )


    # ==========================================
    # Causes
    # ==========================================

    causes = safe_list(
        info.get(
            "Cause"
        )
    )


    story.append(

        Paragraph(
            "Causes",
            heading_style
        )

    )


    if causes:

        for cause in causes:

            story.append(

                Paragraph(
                    "• "
                    + safe_value(
                        cause
                    ),
                    normal_style
                )

            )

    else:

        story.append(

            Paragraph(
                "No cause information available.",
                normal_style
            )

        )


    # ==========================================
    # Treatment
    # ==========================================

    treatments = safe_list(
        info.get(
            "Treatment"
        )
    )


    story.append(

        Paragraph(
            "Treatment",
            heading_style
        )

    )


    if treatments:

        for treatment in treatments:

            story.append(

                Paragraph(
                    "• "
                    + safe_value(
                        treatment
                    ),
                    normal_style
                )

            )

    else:

        story.append(

            Paragraph(
                "No treatment information available.",
                normal_style
            )

        )


    # ==========================================
    # Organic Treatment
    # ==========================================

    organic_treatments = safe_list(
        info.get(
            "Organic_Treatment"
        )
    )


    story.append(

        Paragraph(
            "Organic Treatment",
            heading_style
        )

    )


    if organic_treatments:

        for treatment in organic_treatments:

            story.append(

                Paragraph(
                    "• "
                    + safe_value(
                        treatment
                    ),
                    normal_style
                )

            )

    else:

        story.append(

            Paragraph(
                "No organic treatment information available.",
                normal_style
            )

        )


    # ==========================================
    # Recommended Chemicals
    # ==========================================

    chemicals = safe_list(
        info.get(
            "Recommended_Chemicals"
        )
    )


    story.append(

        Paragraph(
            "Recommended Chemicals",
            heading_style
        )

    )


    if chemicals:

        for chemical in chemicals:

            story.append(

                Paragraph(
                    "• "
                    + safe_value(
                        chemical
                    ),
                    normal_style
                )

            )

    else:

        story.append(

            Paragraph(
                "No chemical recommendations available.",
                normal_style
            )

        )


    # ==========================================
    # Prevention
    # ==========================================

    prevention = safe_list(
        info.get(
            "Prevention"
        )
    )


    story.append(

        Paragraph(
            "Prevention",
            heading_style
        )

    )


    if prevention:

        for item in prevention:

            story.append(

                Paragraph(
                    "• "
                    + safe_value(
                        item
                    ),
                    normal_style
                )

            )

    else:

        story.append(

            Paragraph(
                "No prevention information available.",
                normal_style
            )

        )


    # ==========================================
    # Recommended Actions
    # ==========================================

    actions = safe_list(
        info.get(
            "Recommended_Actions"
        )
    )


    story.append(

        Paragraph(
            "Recommended Actions",
            heading_style
        )

    )


    if actions:

        for action in actions:

            story.append(

                Paragraph(
                    "• "
                    + safe_value(
                        action
                    ),
                    normal_style
                )

            )

    else:

        story.append(

            Paragraph(
                "No specific recommended actions available.",
                normal_style
            )

        )


    # ==========================================
    # Disease Progression
    # ==========================================

    age_cycle = info.get(
        "Age_Cycle",
        {}
    )


    story.append(

        Paragraph(
            "Disease Progression",
            heading_style
        )

    )


    progression_data = [

        [
            Paragraph(
                "<b>Stage</b>",
                normal_style
            ),

            Paragraph(
                "<b>Estimated Information</b>",
                normal_style
            )
        ],

        [
            Paragraph(
                "Early",
                normal_style
            ),

            Paragraph(
                safe_value(
                    age_cycle.get(
                        "Early",
                        "-"
                    ),
                    "-"
                ),
                normal_style
            )
        ],

        [
            Paragraph(
                "Moderate",
                normal_style
            ),

            Paragraph(
                safe_value(
                    age_cycle.get(
                        "Moderate",
                        "-"
                    ),
                    "-"
                ),
                normal_style
            )
        ],

        [
            Paragraph(
                "Severe",
                normal_style
            ),

            Paragraph(
                safe_value(
                    age_cycle.get(
                        "Severe",
                        "-"
                    ),
                    "-"
                ),
                normal_style
            )
        ],

        [
            Paragraph(
                "Estimated",
                normal_style
            ),

            Paragraph(
                safe_value(
                    age_cycle.get(
                        "Estimated",
                        "-"
                    ),
                    "-"
                ),
                normal_style
            )
        ]

    ]


    progression_table = Table(

        progression_data,

        colWidths=[
            45 * mm,
            120 * mm
        ]

    )


    progression_table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor(
                    "#198754"
                )
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor(
                    "#dddddd"
                )
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])

    )


    story.append(
        progression_table
    )


    # ==========================================
    # Disclaimer
    # ==========================================

    story.append(
        Spacer(1, 15)
    )


    story.append(

        Paragraph(
            "<b>Disclaimer:</b> "
            "This report provides AI-based "
            "decision-support information. "
            "Disease predictions should be "
            "verified with appropriate "
            "agricultural expertise before "
            "applying treatments or chemicals.",
            small_style
        )

    )


    # ==========================================
    # Build PDF
    # ==========================================

    document.build(
        story
    )