from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,HRFlowable
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from datetime import datetime

def create_notes_pdf(content):

    pdf_path="Focused_Notes.pdf"
    doc=SimpleDocTemplate(pdf_path,rightMargin=40,leftMargin=40,topMargin=40,bottomMargin=40)

    styles=getSampleStyleSheet()

    title_style=ParagraphStyle("Title",parent=styles["Title"],fontSize=22,leading=28,alignment=TA_CENTER)
    heading_style=ParagraphStyle("Heading",parent=styles["Heading1"],fontSize=14,leading=18,alignment=TA_CENTER,spaceBefore=5,spaceAfter=5)
    section_style=ParagraphStyle("Section",parent=styles["Heading2"],fontSize=12,leading=14,spaceBefore=4,spaceAfter=4)
    body_style=ParagraphStyle("Body",parent=styles["BodyText"],fontSize=10,leading=14,spaceBefore=1,spaceAfter=1)

    elements=[]

    elements.append(Paragraph("Exam Prep AI - Focused Notes",title_style))
    elements.append(Spacer(1,15))
    elements.append(Paragraph(datetime.now().strftime("Generated on %d %B %Y"),body_style))
    elements.append(Spacer(1,20))

    for line in content.split("\n"):

        line=line.strip()

        if not line:
            continue

        line=line.replace("**","").replace("###","")

        if line.startswith("* "):
            line="• "+line[2:]

        major_sections=["IMPORTANT TOPICS","MISSING IMPORTANT TOPICS","PARTIALLY COVERED TOPICS"]

        sub_sections=["Definition:","Key Points:","Important Features:",
                      "Advantages:","Disadvantages:","Advantages and Disadvantages:",
                      "Common Exam Questions:","5-Mark Answer:","10-Mark Answer:"]

        if line.upper() in major_sections:

            elements.append(Spacer(1,12))
            elements.append(HRFlowable(width="100%"))
            elements.append(Paragraph(f"<b>{line.upper()}</b>",heading_style))
            elements.append(HRFlowable(width="100%"))
            elements.append(Spacer(1,8))

        elif line in sub_sections:

            elements.append(Spacer(1,5))
            elements.append(Paragraph(f"<b>{line}</b>",section_style))
            elements.append(HRFlowable(width="100%"))
            elements.append(Spacer(1,3))

        elif len(line)<50 and ":" not in line and not line.startswith("•") and not line[0].isdigit():

            elements.append(Spacer(1,8))
            elements.append(HRFlowable(width="100%"))
            elements.append(Paragraph(f"<b>{line.upper()}</b>",heading_style))
            elements.append(HRFlowable(width="100%"))
            elements.append(Spacer(1,5))

        else:

            elements.append(Paragraph(line,body_style))

    doc.build(elements)

    return pdf_path


def create_revision_pdf(content):

    pdf_path="Revision_Plan.pdf"
    doc=SimpleDocTemplate(pdf_path,rightMargin=40,leftMargin=40,topMargin=40,bottomMargin=40)

    styles=getSampleStyleSheet()

    title_style=ParagraphStyle("Title",parent=styles["Title"],fontSize=22,leading=28,alignment=TA_CENTER)
    heading_style=ParagraphStyle("Heading",parent=styles["Heading1"],fontSize=14,leading=18,alignment=TA_CENTER,spaceBefore=5,spaceAfter=5)
    body_style=ParagraphStyle("Body",parent=styles["BodyText"],fontSize=10,leading=14)

    elements=[]

    elements.append(Paragraph("Exam Prep AI - Revision Plan",title_style))
    elements.append(Spacer(1,15))
    elements.append(Paragraph(datetime.now().strftime("Generated on %d %B %Y"),body_style))
    elements.append(Spacer(1,20))

    for line in content.split("\n"):

        line=line.strip()

        if not line:
            continue

        if line.upper().startswith("DAY ") or line.upper().startswith("WEEK ") or "REVISION PLAN" in line.upper():

            elements.append(Spacer(1,8))
            elements.append(HRFlowable(width="100%"))
            elements.append(Paragraph(f"<b>{line}</b>",heading_style))
            elements.append(HRFlowable(width="100%"))
            elements.append(Spacer(1,5))

        else:

            elements.append(Paragraph(line,body_style))

    doc.build(elements)

    return pdf_path


def create_mock_pdf(content):

    pdf_path="Mock_Test_Paper.pdf"
    doc=SimpleDocTemplate(pdf_path,rightMargin=40,leftMargin=40,topMargin=40,bottomMargin=40)

    styles=getSampleStyleSheet()

    title_style=ParagraphStyle("Title",parent=styles["Title"],fontSize=18,leading=24,alignment=TA_CENTER)
    section_style=ParagraphStyle("Section",parent=styles["Heading2"],fontSize=12,leading=16,spaceBefore=5,spaceAfter=5)
    body_style=ParagraphStyle("Body",parent=styles["BodyText"],fontSize=10,leading=14)

    elements=[]

    elements.append(Paragraph("Exam Prep AI - Mock Question Paper",title_style))
    elements.append(Spacer(1,15))
    elements.append(Paragraph(datetime.now().strftime("Generated on %d %B %Y"),body_style))
    elements.append(Spacer(1,20))

    for line in content.split("\n"):

        line=line.strip()

        if not line:
            elements.append(Spacer(1,4))
            continue

        if "UNIVERSITY" in line.upper() or "EXAMINATION" in line.upper() or "QUESTION PAPER" in line.upper():

            elements.append(Paragraph(f"<b>{line}</b>",title_style))

        elif line.upper().startswith("PART ") or line.upper().startswith("SECTION "):

            elements.append(Spacer(1,8))
            elements.append(HRFlowable(width="100%"))
            elements.append(Paragraph(f"<b>{line}</b>",section_style))
            elements.append(HRFlowable(width="100%"))
            elements.append(Spacer(1,4))

        else:

            elements.append(Paragraph(line,body_style))

    doc.build(elements)

    return pdf_path