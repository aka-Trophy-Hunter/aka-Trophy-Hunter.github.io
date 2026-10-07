# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)

ACCENT = colors.HexColor("#1d4ed8")
TEXT = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#5a5a5a")

name_style = ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=24, textColor=TEXT, leading=28)
contact_style = ParagraphStyle("contact", fontName="Helvetica", fontSize=9.5, textColor=MUTED, alignment=TA_RIGHT, leading=14)
section_style = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11.5, textColor=ACCENT, spaceBefore=6, spaceAfter=2)
body_style = ParagraphStyle("body", fontName="Helvetica", fontSize=9.3, textColor=TEXT, leading=12.5)
date_style = ParagraphStyle("date", fontName="Helvetica", fontSize=8.7, textColor=MUTED, leading=12)
role_style = ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=9.6, textColor=TEXT, leading=12.3)
sub_style = ParagraphStyle("sub", fontName="Helvetica-Oblique", fontSize=8.9, textColor=MUTED, leading=12)
bullet_style = ParagraphStyle("bullet", fontName="Helvetica", fontSize=8.9, textColor=TEXT, leading=12, leftIndent=10, bulletIndent=0, spaceAfter=1)
label_style = ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=9.3, textColor=TEXT, leading=12.5)

DATE_COL = 1.15 * inch
CONTENT_COL = 6.1 * inch

def section(title):
    return [Paragraph(title.upper(), section_style), HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=6)]

def section_with(title, first_flowables):
    """Section header glued to its first content block so the header never
    ends up alone at the bottom of a page. first_flowables may be a single
    flowable or a list; never nest this inside another KeepTogether."""
    if not isinstance(first_flowables, list):
        first_flowables = [first_flowables]
    return KeepTogether(section(title) + first_flowables)

def row(date_text, content_flowables, left_style=date_style):
    left = date_text if hasattr(date_text, "wrap") else Paragraph(date_text, left_style)
    t = Table([[left, content_flowables]], colWidths=[DATE_COL, CONTENT_COL])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t

def bullets(items):
    return [Paragraph("&bull;&nbsp;&nbsp;" + i, bullet_style) for i in items]

story = []

# ---------------- Header ----------------
header_tbl = Table([[
    Paragraph("Moneeba Abrar", name_style),
    Paragraph(
        "Haripur, KP, Pakistan<br/>"
        "moneebaabrar88@gmail.com &nbsp;|&nbsp; +92 311 7864822<br/>"
        '<link href="https://github.com/aka-Trophy-Hunter" color="#1d4ed8">github.com/aka-Trophy-Hunter</link>',
        contact_style,
    ),
]], colWidths=[3.6 * inch, 3.65 * inch])
header_tbl.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
]))
story.append(header_tbl)
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=1.4, color=TEXT, spaceAfter=7))

# ---------------- Objective ----------------
story.append(section_with("Objective", Paragraph(
    "Software Engineering graduate with research experience in computer vision and deep learning. "
    "Interested in efficient deep learning &mdash; especially making vision transformers faster and lighter "
    "through token compression, knowledge distillation, and efficient architecture design, while keeping "
    "them accurate. Eager to contribute to research that makes large vision models practical for "
    "real-world and resource-limited settings.",
    body_style,
)))

# ---------------- Education ----------------
story.append(section_with("Education", row("Fall 2022 &ndash;<br/>Spring 2026", [
    Paragraph("B.S. Software Engineering &mdash; <b>Gold Medalist</b>, CGPA 3.92/4.00", role_style),
    Paragraph("University of Haripur, KP, Pakistan", sub_style),
])))

# ---------------- Research Interests ----------------
story.append(section_with("Research Interests", Paragraph(
    "Efficient Deep Learning &middot; Self-Supervised Representation Learning &middot; "
    "Foundation Models &middot; Image Recognition &amp; Object Detection &middot; "
    "Knowledge Distillation &middot; Vision-Language Models",
    body_style,
)))

# ---------------- Major Research Project ----------------
story.append(section_with("Major Research Project", row("2025 &ndash; 2026", [
    Paragraph("Augmented Reality &amp; Deep Learning Assisted Enhanced Museum Experience", role_style),
    Paragraph("Final Year Research Project (Thesis) &mdash; University of Haripur", sub_style),
    Spacer(1, 3),
] + bullets([
    "Built a multimodal AI system integrating computer vision, deep learning, speech interaction, and "
    "multilingual assistance for real-world cultural heritage recognition (case study: Taxila Museum).",
    "Curated a custom dataset of Taxila Museum artifacts; performed end-to-end data collection, "
    "preprocessing, and augmentation pipelines; developed vision-language recognition pipelines for "
    "low-resource artifact categories.",
    "Research paper on hybrid vision-language recognition for cultural heritage systems under "
    "preparation for publication.",
    "Nominated by the Directorate General of Science &amp; Technology (DoST), KP for research funding, "
    "recognizing scientific merit and societal impact.",
    "Awarded Top Project at the Final Year Project Exhibition, University of Haripur.",
]))))

# ---------------- Academic Projects ----------------
def project(title, stack, desc):
    return [
        Paragraph(f"{title} <font color='#5a5a5a' size='8.5'>&mdash; {stack}</font>", role_style),
    ] + bullets([desc])

proj_items = [
    ("Explainable AI for Knee Osteoarthritis Detection &amp; Severity Grading",
     "Python, TensorFlow, DenseNet-121",
     "DenseNet-121 ensemble for 5-grade knee osteoarthritis severity classification with Grad-CAM "
     "interpretability heatmaps."),
    ("PulmoVision: Automated Pneumonia Diagnosis Using Deep Learning",
     "Python, TensorFlow, ResNet",
     "Developed a ResNet-based transfer learning pipeline for automated pneumonia detection and "
     "classification from chest X-ray images."),
    ("Performance Benchmarking of Machine Learning Algorithms",
     "Python, scikit-learn, Pandas",
     "Benchmarked multiple machine learning algorithms across datasets and problem instances, analyzing "
     "performance variations to identify relationships between dataset characteristics and algorithm "
     "effectiveness."),
    ("AI-Powered Nail Condition Analyzer",
     "Python, TensorFlow, OpenCV",
     "CNN-based diagnostic assistant for medical image classification of nail conditions with "
     "preprocessing pipelines."),
    ("Encoder-Aware Visual Token Compression for Efficient VLMs",
     "Python, PyTorch, ViT",
     "Implementing adaptive, encoder-dependent visual token compression for vision-language models, "
     "benchmarking a random baseline and Top-K pruning against an adaptive compression method on ViT."),
    ("Data Structures &amp; Algorithms Visualization Suite",
     "C++",
     "Desktop application with graphical visualization of sorting, tree traversals, and graph "
     "pathfinding algorithms."),
]
story.append(section_with("Academic Projects", project(*proj_items[0])))
for i, (t, s, d) in enumerate(proj_items[1:], start=1):
    story.append(Spacer(1, 3))
    story.append(KeepTogether(project(t, s, d)))

# ---------------- Technical Skills ----------------
skills_rows = [
    ("Languages", "Python, JavaScript, C++, C#"),
    ("Frameworks", "Hugging Face Transformers, PyTorch, TensorFlow, OpenCV, Scikit-learn, Streamlit"),
    ("Dev Tools", "Git/GitHub, Linux/Bash, REST APIs, Flask, Streamlit"),
]
skills_flowables = [row(label, [Paragraph(val, body_style)], left_style=label_style) for label, val in skills_rows]
story.append(KeepTogether(section("Technical Skills") + skills_flowables))

# ---------------- Experience ----------------
story += section("Experience")
story.append(row("Jul 2026 &ndash;<br/>Present", [
    Paragraph("AI Intern", role_style),
    Paragraph("UAVs Lab, National Radio and Telecommunication Corporation (NRTC) &mdash; Haripur, Pakistan", sub_style),
    Spacer(1, 3),
] + bullets([
    "Working on an object detection and pattern recognition module for a UAV-based mission: comparing "
    "before/after aerial imagery from a drone's outbound and return flight path to identify and flag "
    "missing objects.",
    "Collaborating within a larger multi-module team project, owning the detection and comparison "
    "component end-to-end.",
])))
story.append(row("Jul 2025 &ndash;<br/>Aug 2025", [
    Paragraph("IT Directorate Intern", role_style),
    Paragraph("Senate of Pakistan &mdash; Islamabad, Pakistan", sub_style),
    Spacer(1, 3),
] + bullets([
    "Contributed to software development and web-based systems within the IT Directorate.",
    "Assisted in maintaining and troubleshooting internal web applications used across departments.",
    "Collaborated with senior IT staff on requirement gathering and testing for ongoing system upgrades.",
])))
story.append(row("Jul 2024 &ndash;<br/>Aug 2024", [
    Paragraph("Game Development Intern", role_style),
    Paragraph("Codematics Inc. &mdash; Abbottabad, Pakistan", sub_style),
    Spacer(1, 3),
] + bullets([
    "Developed 2D/3D Unity projects, including animations and shader graphs.",
    "Explored AI-driven gameplay elements and prototyped interactive mechanics.",
    "Collaborated with a small team on game design iteration and playtesting feedback.",
])))

# ---------------- Awards & Achievements ----------------
story.append(section_with("Awards &amp; Achievements", Paragraph(
    "<b>Gold Medal</b>, BS Software Engineering (CGPA 3.92/4.00), University of Haripur", bullet_style)))
story.append(Paragraph(
    "<b>Top Project</b>, Final Year Project Exhibition, University of Haripur", bullet_style))
story.append(Paragraph(
    "<b>PM Youth Laptop Scheme</b> &mdash; awarded for academic excellence", bullet_style))
story.append(Paragraph(
    "A1 grades in SSC &amp; FSc (2019&ndash;2021); Top 10, Abbottabad Board (FSc); 93rd percentile, "
    "Engineering/IT entry test", bullet_style))
story.append(Paragraph(
    "Top Performer, Python Frenzy Competition, IT Club", bullet_style))
story.append(Paragraph(
    "Award for Organizing UoH 4th Convocation (2025)", bullet_style))
story.append(Paragraph(
    "Participant, 1st International Conference on Computational Sciences", bullet_style))

# ---------------- Certifications ----------------
cert_list = [
    "AI in Healthcare Specialization &mdash; Stanford University",
    "Deep Learning for Computer Vision: Techniques and Applications &mdash; Khalifa University",
    "Computer Vision Specialization &mdash; University of Colorado Boulder",
    "Modern AI Models for Vision and Multimodal Understanding &mdash; University of Colorado Boulder",
    "Multimodal Intelligence: Vision, Audio and Language in Action &mdash; Coursera",
    "Build Multimodal Generative AI Applications &mdash; IBM",
    "Fundamentals of Building AI Agents &mdash; IBM",
    "Explainable AI: Scene Classification and Grad-CAM Visualization &mdash; Coursera",
    "Interpretable Machine Learning &mdash; Duke University",
    "Unsupervised Learning, Recommenders, Reinforcement Learning &mdash; DeepLearning.AI",
    "AI in Healthcare Webinar &mdash; UAEU",
    "Crash Course on Python &mdash; Google",
]
story.append(section_with("Certifications", Paragraph("&bull;&nbsp;&nbsp;" + cert_list[0], bullet_style)))
for c in cert_list[1:]:
    story.append(Paragraph("&bull;&nbsp;&nbsp;" + c, bullet_style))

# ---------------- Leadership & Service ----------------
story.append(section_with("Leadership &amp; Service",
    row("Jul 2025 &ndash;<br/>Present", [Paragraph("Vice President, IT Computing Society, University of Haripur", bullet_style)])))
story.append(row("Dec 2025", [Paragraph("Career Expo 2025 Organizer, University of Haripur", bullet_style)]))
story.append(row("May 2025", [Paragraph("Event Manager, IT Department Orientation, University of Haripur", bullet_style)]))
story.append(row("Jan 2024", [Paragraph("Team Lead, Social Work Visit &mdash; Aghosh Al-Khidmat, Haripur", bullet_style)]))

# ---------------- References ----------------
story.append(section_with("References", Paragraph("Available upon request.", body_style)))

doc = SimpleDocTemplate(
    "Moneeba_Abrar_CV.pdf",
    pagesize=letter,
    leftMargin=0.6 * inch, rightMargin=0.6 * inch,
    topMargin=0.4 * inch, bottomMargin=0.3 * inch,
    title="Moneeba Abrar - CV",
)
doc.build(story)
print("done")
