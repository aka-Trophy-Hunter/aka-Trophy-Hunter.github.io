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

LINK = "color='#1d4ed8'"

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

def link(text, url):
    return f"<link href='{url}' {LINK}>{text}</link>"

story = []

# ---------------- Header ----------------
header_tbl = Table([[
    Paragraph("Moneeba Abrar", name_style),
    Paragraph(
        "Haripur, KP, Pakistan<br/>"
        "moneebaabrar88@gmail.com<br/>"
        f'{link("github.com/aka-Trophy-Hunter", "https://github.com/aka-Trophy-Hunter")} &nbsp;|&nbsp; '
        f'{link("linkedin.com/in/moneeba-a-", "https://www.linkedin.com/in/moneeba-a-/")}',
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
    "Gold-medalist Software Engineering graduate with hands-on research in computer vision, "
    "vision-language models, and medical imaging. I aim to make large vision models faster, "
    "lighter, and more trustworthy &mdash; through token compression, knowledge distillation, "
    "and interpretable deep learning &mdash; so they can run reliably in real-world and "
    "resource-limited settings.",
    body_style,
)))

# ---------------- Education ----------------
story.append(section_with("Education", row("Oct 2022 &ndash;<br/>Jun 2026", [
    Paragraph(f"B.S. Software Engineering &mdash; <b>Gold Medalist</b>, CGPA 3.92/4.00", role_style),
    Paragraph(f'{link("University of Haripur", "https://www.uoh.edu.pk/#gsc.tab=0")}, KP, Pakistan', sub_style),
    Paragraph("Thesis: Augmented Reality &amp; Deep Learning Assisted Enhanced Museum Experience", sub_style),
])))

# ---------------- Research Interests ----------------
story.append(section_with("Research Interests", Paragraph(
    "Efficient Deep Learning &middot; Interpretable AI for Medical Imaging &middot; "
    "Computer Vision &middot; Self-Supervised Representation Learning &middot; "
    "Image Recognition &amp; Object Detection &middot; Vision-Language Models",
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
def project(title, stack, desc, links_=None):
    flowables = [
        Paragraph(f"{title} <font color='#5a5a5a' size='8.5'>&mdash; {stack}</font>", role_style),
    ] + bullets([desc])
    if links_:
        linktext = " &nbsp;&middot;&nbsp; ".join(link(t, u) for t, u in links_)
        flowables.append(Paragraph(linktext, ParagraphStyle(
            "projlink", fontName="Helvetica", fontSize=8.3, textColor=ACCENT, leading=11, leftIndent=10, spaceBefore=1)))
    return flowables

proj_items = [
    ("Explainable AI for Knee Osteoarthritis Detection &amp; Severity Grading",
     "Python, TensorFlow, DenseNet-121",
     "DenseNet-121 ensemble that grades knee osteoarthritis into 5 severity levels from X-rays, "
     "reaching 98.75% accuracy, with Grad-CAM heatmaps showing which regions drive each prediction.",
     None),
    ("PulmoVision: Automated Pneumonia Diagnosis Using Deep Learning",
     "Python, TensorFlow, ResNet",
     "ResNet transfer learning pipeline for pneumonia classification from chest X-rays, deployed as "
     "a public web app on Streamlit Community Cloud.",
     [("Live App", "https://pulmovision-.streamlit.app/"), ("Code", "https://github.com/aka-Trophy-Hunter/PulmoVision")]),
    ("Performance Benchmarking of Machine Learning Algorithms",
     "Python, scikit-learn, Pandas",
     "Benchmarking multiple machine learning algorithms across datasets and problem instances, "
     "analyzing performance variations to identify relationships between dataset characteristics "
     "and algorithm effectiveness.",
     None),
    ("NailScan: AI-Powered Nail Condition Analyzer",
     "Python, PyTorch, YOLOv5, OpenCV",
     "Built and deployed a nail health screening app: a YOLOv5 segmentation model locates the nail, "
     "then a ResNet-152 classifier grades it into one of 6 conditions.",
     [("Live App", "https://nailscan.streamlit.app/"), ("Code", "https://github.com/aka-Trophy-Hunter/NailScan")]),
    ("Encoder-Aware Visual Token Compression for Efficient VLMs",
     "Python, PyTorch, ViT",
     "Implementing adaptive, encoder-dependent visual token compression for vision-language models, "
     "benchmarking a random baseline and Top-K pruning against an adaptive compression method on ViT.",
     [("Code", "https://github.com/aka-Trophy-Hunter/encoder-aware-visual-token-compression")]),
    ("Data Structures &amp; Algorithms Visualization Suite",
     "C++",
     "Desktop application with graphical visualization of sorting, tree traversals, and graph "
     "pathfinding algorithms.",
     None),
]
story.append(section_with("Academic Projects", project(*proj_items[0])))
for i, (t, s, d, l) in enumerate(proj_items[1:], start=1):
    story.append(Spacer(1, 3))
    story.append(KeepTogether(project(t, s, d, l)))

# ---------------- Technical Skills ----------------
skills_rows = [
    ("Languages", "Python, JavaScript, C++"),
    ("Frameworks", "PyTorch, TensorFlow, Keras, Hugging Face Transformers, OpenCV, Scikit-learn, FastAPI, Pandas, Seaborn, Plotly, Streamlit"),
    ("Dev Tools", "Git/GitHub, MySQL, SQL, Linux/Bash, REST APIs, OOP, Web Development"),
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
    "<b>Gold Medal</b>, BS Software Engineering (CGPA 3.92/4.00), University of Haripur &mdash; Jun 2026", bullet_style)))
story.append(Paragraph(
    "<b>Top Project</b>, Final Year Project Exhibition, University of Haripur &mdash; Jul 2026", bullet_style))
story.append(Paragraph(
    "<b>Laptop Recipient</b>, PM Youth Program (Academic Excellence) &mdash; Nov 2023", bullet_style))
story.append(Paragraph(
    "<b>Top Performer</b>, Python Frenzy Competition, IT Club &mdash; Sep 2024", bullet_style))
story.append(Paragraph(
    "A1 grades in SSC &amp; FSc (2019&ndash;2021); Top 10, Abbottabad Board (FSc); 93rd percentile, "
    "Engineering/IT entry test", bullet_style))

# ---------------- Conferences & Seminars ----------------
story.append(section_with("Conferences &amp; Seminars", Paragraph(
    "AI in Healthcare Webinar &mdash; Abu Dhabi, UAE", bullet_style)))
story.append(Paragraph(
    "1st International Conference on Computational Sciences and Innovations (ICCSI) &mdash; Haripur, Pakistan", bullet_style))
story.append(Paragraph(
    "CyberFest &mdash; Peshawar, Pakistan", bullet_style))

# ---------------- Certifications ----------------
cert_list = [
    ("AI in Healthcare Specialization", "Stanford University", "https://www.coursera.org/account/accomplishments/specialization/certificate/10YKG46I1FAG"),
    ("Deep Learning for Computer Vision: Techniques and Applications", "Khalifa University", "https://www.coursera.org/account/accomplishments/certificate/6F8Q5X2V27ST"),
    ("Computer Vision Specialization", "University of Colorado Boulder", "https://www.coursera.org/account/accomplishments/specialization/certificate/IO9OI0Y13UO8"),
    ("Modern AI Models for Vision and Multimodal Understanding", "University of Colorado Boulder", None),
    ("Multimodal Intelligence: Vision, Audio and Language in Action", "Coursera", "https://www.coursera.org/account/accomplishments/specialization/certificate/TMOV49NU5JOV"),
    ("Unsupervised Learning, Recommenders, Reinforcement Learning", "DeepLearning.AI", "https://coursera.org/share/460741ea7097f9bf0a053a9bf4b9c18d"),
    ("Fundamentals of Building AI Agents", "IBM", "https://coursera.org/share/c2cd272d9767f2998544eb857056461c"),
    ("Explainable AI: Scene Classification and Grad-CAM Visualization", "Coursera", "https://www.coursera.org/account/accomplishments/certificate/LEA9PSTX5YKD"),
    ("Interpretable Machine Learning", "Duke University", "https://coursera.org/share/91443daedc7e44a0a40a825eadcb519a"),
    ("Build Multimodal Generative AI Applications", "IBM", "https://coursera.org/share/d3b58555608014544846893553609420"),
    ("AI in Healthcare Webinar", "UAEU", None),
    ("Crash Course on Python", "Google", None),
]
def cert_line(title, org, url):
    t = link(title, url) if url else title
    return "&bull;&nbsp;&nbsp;" + t + f" &mdash; {org}"

story.append(section_with("Certifications", Paragraph(cert_line(*cert_list[0]), bullet_style)))
for c in cert_list[1:]:
    story.append(Paragraph(cert_line(*c), bullet_style))

# ---------------- Leadership & Service ----------------
story.append(section_with("Leadership &amp; Service",
    row("Jun 2025 &ndash;<br/>Present", [Paragraph("Vice President, IT Computing Society, University of Haripur", bullet_style)])))
story.append(row("Dec 2025", [Paragraph(f'Career Expo 2025 Organizer, University of Haripur &nbsp; {link("[Certificate]", "https://drive.google.com/file/d/1VxpkeLeTrgCH6usfg-NGEULqEfLrT_Cx/view?usp=drive_link")}', bullet_style)]))
story.append(row("Apr 2025", [Paragraph(f'Event Manager, 4th Convocation, University of Haripur &nbsp; {link("[Certificate]", "https://drive.google.com/file/d/11WehmAHuvVMmYt0XrU5tWbrvFdyDDCT3/view?usp=drive_link")}', bullet_style)]))
story.append(row("Jan 2024", [Paragraph(f'Team Lead, Social Work Visit &mdash; Aghosh Al-Khidmat, Haripur &nbsp; {link("[Photos]", "https://drive.google.com/drive/folders/1u6vhqeTaLEJUNfOt--eZunaILs_GSkna?usp=drive_link")}', bullet_style)]))

# ---------------- Language Skills ----------------
story.append(section_with("Language Skills", Paragraph(
    "<b>Urdu</b> &mdash; Mother tongue &nbsp;&nbsp;|&nbsp;&nbsp; <b>English</b> &mdash; Fluent", body_style)))

# ---------------- References ----------------
story.append(section_with("References", row(
    "", [
        Paragraph("Dr. Dawar Khan", role_style),
        Paragraph("Assistant Professor, Course Instructor &mdash; University of Haripur", sub_style),
        Paragraph(f'dawar.khan@uoh.edu.pk &nbsp;|&nbsp; {link("dawarkhanuom.github.io", "https://dawarkhanuom.github.io/")}', body_style),
    ]
)))
story.append(row(
    "", [
        Paragraph("Dr. Mudassar Ali Khan", role_style),
        Paragraph("Assistant Professor, Research Supervisor &mdash; University of Haripur", sub_style),
        Paragraph(f'mudaser@uoh.edu.pk &nbsp;|&nbsp; {link("Google Scholar", "https://scholar.google.com/citations?hl=en&amp;user=P06LmbsAAAAJ")}', body_style),
    ]
))

doc = SimpleDocTemplate(
    "Moneeba_Abrar_CV.pdf",
    pagesize=letter,
    leftMargin=0.6 * inch, rightMargin=0.6 * inch,
    topMargin=0.4 * inch, bottomMargin=0.3 * inch,
    title="Moneeba Abrar - CV",
)
doc.build(story)
print("done")
