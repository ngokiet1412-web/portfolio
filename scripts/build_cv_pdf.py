from pathlib import Path

import reportlab
from pypdf import PdfReader
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "NgoQuangKiet_CV_FINAL.pdf"

NAVY = HexColor("#0A2342")
BLUE = HexColor("#1177E8")
TEXT = HexColor("#173A61")
SUB = HexColor("#58728E")
LINE = HexColor("#D7E5F2")
WHITE = HexColor("#FFFFFF")
FONT_DIR = Path(reportlab.__file__).resolve().parent / "fonts"
REGULAR = "Vera"
BOLD = "Vera-Bold"
pdfmetrics.registerFont(TTFont(REGULAR, str(FONT_DIR / "Vera.ttf")))
pdfmetrics.registerFont(TTFont(BOLD, str(FONT_DIR / "VeraBd.ttf")))


def wrapped_lines(text, font, size, width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and stringWidth(candidate, font, size) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_text(c, text, x, y, width, *, font=REGULAR, size=9.2, leading=12.6, color=TEXT):
    c.setFillColor(color)
    c.setFont(font, size)
    for line in wrapped_lines(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_section(c, label, x, y):
    c.setFillColor(BLUE)
    c.setFont(BOLD, 8.2)
    c.drawString(x, y, label)
    return y - 17


def draw_heading(c, text, x, y, width, size=11):
    return draw_text(c, text, x, y, width, font=BOLD, size=size, leading=size + 3, color=NAVY)


def draw_bullets(c, items, x, y, width):
    for item in items:
        lines = wrapped_lines(item, REGULAR, 8.8, width - 12)
        c.setFillColor(BLUE)
        c.setFont(BOLD, 8.8)
        c.drawString(x, y, "-")
        c.setFillColor(TEXT)
        c.setFont(REGULAR, 8.8)
        for index, line in enumerate(lines):
            c.drawString(x + 10, y, line)
            y -= 11.5
        y -= 2
    return y


def build():
    c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1, invariant=1)
    width, height = A4
    c.setTitle("Ngo Quang Kiet - CV")
    c.setAuthor("Ngo Quang Kiet")

    c.setFillColor(NAVY)
    c.rect(0, height - 100, width, 100, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(BOLD, 25)
    c.drawString(36, height - 42, "NGO QUANG KIET")
    c.setFillColor(HexColor("#CFE7FF"))
    c.setFont(BOLD, 11)
    c.drawString(36, height - 60, "AUTOMOTIVE ENGINEERING STUDENT")
    c.setFillColor(WHITE)
    c.setFont(REGULAR, 8.5)
    c.drawString(36, height - 78, "ngokiet1412@gmail.com  |  +84 909 224 702  |  Ho Chi Minh City, Vietnam")
    c.drawString(36, height - 91, "ngokiet1412-web.github.io/portfolio  |  github.com/ngokiet1412-web")
    c.linkURL("mailto:ngokiet1412@gmail.com", (36, height - 81, 160, height - 71), relative=0)
    c.linkURL("https://ngokiet1412-web.github.io/portfolio/", (36, height - 94, 220, height - 84), relative=0)
    c.linkURL("https://github.com/ngokiet1412-web", (242, height - 94, 390, height - 84), relative=0)

    left_x, left_w = 36, 337
    right_x, right_w = 399, 160
    top_y = height - 124
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.line(386, 34, 386, top_y + 8)

    y = draw_section(c, "PROFILE", left_x, top_y)
    y = draw_text(c, "Automotive Engineering student at HCMUT with hands-on exposure to field investigation, Siemens NX, ANSYS Mechanical, vehicle diagnostics and sensor-oriented R&D. I connect real evidence with modeling, engineering checks and practical validation planning.", left_x, y, left_w)
    y -= 12

    y = draw_section(c, "EXPERIENCE", left_x, y)
    y = draw_heading(c, "R&D - Vehicle Monitoring & Diagnostics", left_x, y, left_w)
    y = draw_text(c, "Thinh Kim Co., Ltd. | 2025 - Present", left_x, y - 1, left_w, font=BOLD, size=8.4, leading=11, color=SUB)
    y -= 3
    y = draw_bullets(c, [
        "Advance FuelGuard from field surveys toward a monitoring workflow for construction machinery.",
        "Support mechanical integration and analysis-oriented checks with Siemens NX and ANSYS under field constraints.",
        "Research diagnostic and sensor integration around OBD/CAN, ECU/electrical systems and controller I/O.",
    ], left_x, y, left_w)
    y -= 10

    y = draw_section(c, "SELECTED ENGINEERING WORK", left_x, y)
    y = draw_heading(c, "FuelGuard - Integrated R&D Project", left_x, y, left_w, size=10.2)
    y = draw_text(c, "Connect field evidence, CAD/CAE, prototype electronics, data handling and validation planning in one traceable workflow.", left_x, y - 1, left_w, size=8.8, leading=11.5)
    y -= 6
    y = draw_heading(c, "ROBEX & HAMM Field Investigation", left_x, y, left_w, size=10.2)
    y = draw_text(c, "Record service access, routing, dust/vibration exposure and packaging constraints on real machines, then translate observations into design requirements.", left_x, y - 1, left_w, size=8.8, leading=11.5)
    y -= 6
    y = draw_heading(c, "Versioned Engineering Workflow", left_x, y, left_w, size=10.2)
    y = draw_text(c, "Keep sources, decisions, code and reports traceable in GitHub with explicit review gates and human verification.", left_x, y - 1, left_w, size=8.8, leading=11.5)

    ry = draw_section(c, "EDUCATION", right_x, top_y)
    ry = draw_heading(c, "Ho Chi Minh City University of Technology (HCMUT)", right_x, ry, right_w, size=10.2)
    ry = draw_text(c, "Automotive Engineering program | 2023 - Present", right_x, ry - 2, right_w, font=BOLD, size=8.2, leading=11, color=SUB)
    ry = draw_text(c, "Vehicle systems, powertrain, electrical/electronic systems and diagnostics.", right_x, ry - 5, right_w, size=8.5, leading=11.2)
    ry -= 14

    ry = draw_section(c, "TECHNICAL FOCUS", right_x, ry)
    skills = [
        ("Mechanical Design", "Siemens NX; 3D modeling; assembly structure"),
        ("Engineering Simulation", "ANSYS Mechanical; structural screening; basic thermal evaluation"),
        ("Vehicle Systems", "Diagnostics; OBD/CAN research; sensors; controller I/O"),
        ("Engineering Workflow", "Field investigation; evidence traceability; GitHub; technical documentation"),
    ]
    for heading, detail in skills:
        ry = draw_heading(c, heading, right_x, ry, right_w, size=9.5)
        ry = draw_text(c, detail, right_x, ry - 1, right_w, size=8.3, leading=10.8, color=SUB)
        ry -= 7

    ry = draw_section(c, "WORKING METHOD", right_x, ry)
    ry = draw_bullets(c, ["Field-oriented", "Evidence-led decisions", "Cross-domain integration", "Human verification"], right_x, ry, right_w)

    if min(y, ry) < 38:
        raise RuntimeError(f"CV content overflow: left={y:.1f}, right={ry:.1f}")
    c.setStrokeColor(LINE)
    c.line(36, 30, width - 36, 30)
    c.setFillColor(SUB)
    c.setFont(REGULAR, 7.5)
    c.drawString(36, 18, "Portfolio CV - generated from verified repository content")
    c.save()

    reader = PdfReader(str(OUTPUT))
    box = reader.pages[0].mediabox
    text = reader.pages[0].extract_text() or ""
    required = ["NGO QUANG KIET", "Thinh Kim Co., Ltd.", "Ho Chi Minh City University", "FuelGuard"]
    if len(reader.pages) != 1 or abs(float(box.width) - float(A4[0])) > 0.5 or abs(float(box.height) - float(A4[1])) > 0.5:
        raise RuntimeError(f"Invalid CV PDF geometry: {box}")
    if any(item not in text for item in required):
        raise RuntimeError("CV PDF text validation failed")
    print(f"Created {OUTPUT.name}: one A4 page, selectable text, {len(text)} extracted characters")


if __name__ == "__main__":
    build()
