from pathlib import Path

import reportlab
from pypdf import PdfReader
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "NgoQuangKiet_CV_FINAL.pdf"
PORTRAIT = ROOT / "assets" / "portrait.webp"

NAVY = HexColor("#0A3E72")
BLUE = HexColor("#0D70C9")
INK = HexColor("#20354B")
MUTED = HexColor("#4B667E")
PALE = HexColor("#DDF1FD")
PALE2 = HexColor("#EAF7FE")
LINE = HexColor("#78A8C5")
WHITE = HexColor("#FFFFFF")
FONT_DIR = Path(reportlab.__file__).resolve().parent / "fonts"
REGULAR = "Vera"
BOLD = "Vera-Bold"
pdfmetrics.registerFont(TTFont(REGULAR, str(FONT_DIR / "Vera.ttf")))
pdfmetrics.registerFont(TTFont(BOLD, str(FONT_DIR / "VeraBd.ttf")))


def wrapped_lines(text, font, size, width):
    words = text.split()
    lines, current = [], ""
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


def draw_text(c, text, x, y, width, *, font=REGULAR, size=8, leading=10.2, color=INK):
    c.setFillColor(color)
    c.setFont(font, size)
    for line in wrapped_lines(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_section(c, title, x, y, width, *, size=11):
    c.setFillColor(NAVY)
    c.setFont(BOLD, size)
    c.drawString(x, y, title)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.65)
    c.line(x, y - 4, x + width, y - 4)
    return y - 25


def draw_bullets(c, items, x, y, width, *, size=8.35, leading=12.2):
    for bold, rest in items:
        c.setFillColor(BLUE)
        c.circle(x + 2.3, y + 2.5, 1.8, fill=0, stroke=1)
        cursor_x = x + 11
        first = True
        words = (bold + rest).split()
        current = ""
        lines = []
        for word in words:
            candidate = f"{current} {word}".strip()
            if current and stringWidth(candidate, REGULAR, size) > width - 11:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        for line in lines:
            if first and line.startswith(bold.strip()):
                c.setFont(BOLD, size)
                c.setFillColor(NAVY)
                c.drawString(cursor_x, y, bold.strip())
                bold_w = stringWidth(bold.strip(), BOLD, size)
                remainder = line[len(bold.strip()):]
                c.setFont(REGULAR, size)
                c.setFillColor(INK)
                c.drawString(cursor_x + bold_w, y, remainder)
            else:
                c.setFont(REGULAR, size)
                c.setFillColor(INK)
                c.drawString(cursor_x, y, line)
            y -= leading
            first = False
        y -= 4
    return y


def side_label(c, text, x, y, width):
    c.setFillColor(NAVY)
    c.setFont(BOLD, 9.6)
    c.drawString(x, y, text)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.55)
    c.line(x, y - 4, x + width, y - 4)
    return y - 20


def side_group(c, heading, body, x, y, width):
    c.setFillColor(NAVY)
    c.setFont(BOLD, 7.7)
    c.drawString(x, y, heading.upper())
    return draw_text(c, body, x, y - 10, width, size=7.2, leading=9.65, color=MUTED) - 6


def pill(c, text, x, y):
    size = 6.2
    width = stringWidth(text, REGULAR, size) + 12
    c.setFillColor(HexColor("#C7E7F8"))
    c.roundRect(x, y - 8, width, 12, 6, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont(REGULAR, size)
    c.drawString(x + 6, y - 4.2, text)
    return width


def build():
    c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1, invariant=1)
    width, height = A4
    sidebar_w = 184
    c.setTitle("Ngo Quang Kiet - CV")
    c.setAuthor("Ngo Quang Kiet")

    c.setFillColor(PALE)
    c.rect(0, 0, sidebar_w, height, fill=1, stroke=0)

    # Portrait: a circular clip plus an inward zoom hides the dark square background.
    cx, cy, radius = sidebar_w / 2, height - 67, 48
    path = c.beginPath()
    path.circle(cx, cy, radius)
    c.saveState()
    c.clipPath(path, stroke=0, fill=0)
    image = ImageReader(str(PORTRAIT))
    c.drawImage(image, cx - 60, cy - 63, 120, 126, mask="auto", preserveAspectRatio=False)
    c.restoreState()
    c.setStrokeColor(WHITE)
    c.setLineWidth(6)
    c.circle(cx, cy, radius + 1, fill=0, stroke=1)

    sx, sw = 22, sidebar_w - 44
    sy = height - 132
    sy = side_label(c, "SKILLS", sx, sy, sw)
    sy = side_group(c, "Engineering Software", "Siemens NX", sx, sy, sw)
    sy = draw_text(c, "3D Modeling · Assembly & Constraints · Drafting · Mechanical Component Design · CAD File Exchange", sx, sy + 3, sw, size=7.1, leading=9.55, color=MUTED) - 6
    sy = side_group(c, "ANSYS Mechanical", "Static Structural · Stress & Deformation Evaluation · Safety Factor Assessment · Basic Thermal Analysis", sx, sy + 3, sw)
    sy = side_label(c, "AUTOMOTIVE ENGINEERING", sx, sy - 2, sw)
    sy = draw_text(c, "OBD-II · CAN Fundamentals · Sensor Integration · DSP Concepts · MATLAB/Simulink", sx, sy, sw, size=7.15, leading=9.6, color=MUTED) - 7
    sy = side_label(c, "PROGRAMMING", sx, sy, sw)
    sy = draw_text(c, "Python / C++", sx, sy, sw, font=BOLD, size=7.65, leading=9.2, color=NAVY)
    sy = draw_text(c, "Basic engineering-use level for data processing, signal filtering and task automation.", sx, sy, sw, size=7.15, leading=9.6, color=MUTED) - 7
    sy = side_label(c, "AI-ASSISTED ENGINEERING", sx, sy, sw)
    sy = draw_text(c, "Uses AI tools to learn unfamiliar software, troubleshoot CAD/CAE workflows, support coding and technical research; outputs are manually reviewed and verified.", sx, sy, sw, size=7.1, leading=9.45, color=MUTED) - 7
    sy = side_label(c, "WORKING STYLE", sx, sy, sw)
    styles = [
        ("Adaptable & proactive", "Comfortable learning unfamiliar engineering software and workflows."),
        ("Hands-on & field-oriented", "Comfortable investigating real equipment on site."),
        ("Enthusiastic & collaborative", "Responsive, responsible and willing to support team work."),
        ("Careful with outputs", "Verifies engineering and AI-assisted results before use."),
    ]
    for heading, body in styles:
        sy = draw_text(c, heading, sx, sy, sw, font=BOLD, size=7.25, leading=9.0, color=NAVY)
        sy = draw_text(c, body, sx, sy, sw, size=6.9, leading=9.2, color=MUTED) - 5
    sy = side_label(c, "LANGUAGE", sx, sy - 1, sw)
    draw_text(c, "English — IELTS 6.5", sx, sy, sw, size=7.25, leading=9.1, color=MUTED)

    mx, mw = sidebar_w + 24, width - sidebar_w - 47
    y = height - 48
    c.setFillColor(NAVY)
    c.setFont(BOLD, 24)
    c.drawString(mx, y, "NGO QUANG KIET")
    y -= 19
    c.setFillColor(INK)
    c.setFont(REGULAR, 8.5)
    c.drawString(mx, y, "Automotive Engineering · R&D · Mechanical Design · Vehicle Diagnostics")
    y -= 18
    c.setFont(REGULAR, 7.2)
    c.drawString(mx, y, "Ho Chi Minh City, Vietnam   |   +84 909 224 702   |   ngokiet1412@gmail.com")
    c.setStrokeColor(LINE)
    c.line(mx, y - 8, mx + mw, y - 8)
    c.linkURL("mailto:ngokiet1412@gmail.com", (mx + 235, y - 3, mx + mw, y + 8), relative=0)
    y -= 29

    y = draw_section(c, "PROFESSIONAL SUMMARY", mx, y, mw)
    y = draw_text(c, "Hands-on Automotive Engineering profile combining vehicle systems, CAD/CAE, field investigation, diagnostics and AI-assisted technical workflows with manual review and verification.", mx, y, mw, size=8.95, leading=13)
    y -= 16
    y = draw_section(c, "PROFILE", mx, y, mw)
    y = draw_text(c, "Automotive Engineering student at Ho Chi Minh City University of Technology (HCMUT) with fundamentals in vehicle systems, powertrain, vehicle electrical/electronic systems and diagnostics. Focused on R&D for construction equipment and vehicle monitoring, using Siemens NX/ANSYS for mechanical design and analysis, with basic Python/C++ and OBD/CAN.", mx, y, mw, size=8.7, leading=12.8)
    y -= 16

    project_top = y + 5
    project_h = 116
    c.setFillColor(PALE2)
    c.roundRect(mx - 5, project_top - project_h, mw + 10, project_h, 9, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.setFont(BOLD, 9.3)
    c.drawString(mx + 7, project_top - 17, "CURRENT R&D PROJECT")
    c.setFillColor(NAVY)
    c.setFont(BOLD, 19)
    c.drawString(mx + 7, project_top - 41, "FuelGuard")
    draw_text(c, "Fuel monitoring and equipment-health system for construction machinery, combining sensor data, vehicle diagnostics, mechanical integration and field validation under vibration, dust and uneven-terrain constraints.", mx + 7, project_top - 56, mw - 14, size=7.8, leading=9.7)
    px = mx + 7
    for label in ["Fuel Monitoring", "Vehicle Diagnostics", "Sensor Integration", "CAD/CAE", "Field Validation"]:
        pw = pill(c, label, px, project_top - 91)
        px += pw + 4
    y = project_top - project_h - 20

    y = draw_section(c, "EXPERIENCE", mx, y, mw)
    c.setFillColor(NAVY)
    c.setFont(BOLD, 10.4)
    c.drawString(mx, y, "R&D – Vehicle Monitoring & Diagnostics")
    c.setFont(BOLD, 7.2)
    c.drawRightString(mx + mw, y, "2025 – Present")
    y -= 11
    c.setFillColor(INK)
    c.setFont(REGULAR, 7.3)
    c.drawString(mx, y, "Thinh Kim Co., Ltd.")
    y -= 18
    y = draw_bullets(c, [
        ("FuelGuard system development", " for construction machinery, from field survey to monitoring workflow."),
        ("Siemens NX", " mechanical component and sensor-mount design for vibration, dust and installation constraints."),
        ("ANSYS-based", " structural checks for stress, deformation, material strength and vibration-related evaluation."),
        ("Basic Python/C++", " and signal-processing support for fuel-level filtering and analysis."),
        ("OBD/CAN", ", ECU, electrical-system and sensor investigation for integration."),
        ("On-site equipment surveys", " to identify diagnostic ports, electrical components and feasible installation points."),
    ], mx, y, mw)
    y -= 15

    y = draw_section(c, "EDUCATION", mx, y, mw)
    c.setFillColor(NAVY)
    c.setFont(BOLD, 9.2)
    c.drawString(mx, y, "Ho Chi Minh City University of Technology (HCMUT)")
    c.setFont(BOLD, 7.2)
    c.drawRightString(mx + mw, y, "2023 – Present")
    c.setFillColor(INK)
    c.setFont(REGULAR, 7.5)
    c.drawString(mx, y - 12, "Automotive Engineering Program")

    if min(y - 12, sy) < 31:
        raise RuntimeError(f"CV content overflow: main={y:.1f}, sidebar={sy:.1f}")
    c.setStrokeColor(LINE)
    c.line(mx, 27, width - 23, 27)
    c.setFillColor(MUTED)
    c.setFont(REGULAR, 6.7)
    c.drawRightString(width - 23, 16, "Portfolio: FuelGuard Engineering Portfolio")
    c.linkURL("https://ngokiet1412-web.github.io/portfolio/", (width - 190, 10, width - 23, 25), relative=0)
    c.save()

    reader = PdfReader(str(OUTPUT))
    box = reader.pages[0].mediabox
    text = reader.pages[0].extract_text() or ""
    required = ["NGO QUANG KIET", "PROFESSIONAL SUMMARY", "FuelGuard", "Thinh Kim Co., Ltd.", "IELTS 6.5", "2023"]
    if len(reader.pages) != 1 or abs(float(box.width) - float(A4[0])) > 0.5 or abs(float(box.height) - float(A4[1])) > 0.5:
        raise RuntimeError(f"Invalid CV PDF geometry: {box}")
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError(f"CV PDF text validation failed: {missing}")
    print(f"Created {OUTPUT.name}: one A4 page, selectable text, {len(text)} extracted characters")


if __name__ == "__main__":
    build()
