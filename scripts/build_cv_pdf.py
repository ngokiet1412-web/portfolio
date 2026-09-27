from __future__ import annotations

import hashlib
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "cv-approved-source.jpg"
OUTPUT = ROOT / "NgoQuangKiet_CV_FINAL.pdf"
APPROVED_SHA256 = "716ff6b78460d4582727fe385678a1d65338b80d7e12a36c49ba9c8280fafb5a"


def build() -> None:
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if source_hash != APPROVED_SHA256:
        raise RuntimeError(
            "CV source hash does not match the approved D:/cv.jpg source: "
            f"expected {APPROVED_SHA256}, got {source_hash}"
        )

    page_width, page_height = A4
    image = ImageReader(str(SOURCE))
    image_width, image_height = image.getSize()
    scale = min(page_width / image_width, page_height / image_height)
    draw_width = image_width * scale
    draw_height = image_height * scale
    x = (page_width - draw_width) / 2
    y = (page_height - draw_height) / 2

    pdf = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1, invariant=1)
    pdf.setTitle("Ngo Quang Kiet - CV")
    pdf.setAuthor("Ngo Quang Kiet")
    pdf.drawImage(
        image,
        x,
        y,
        width=draw_width,
        height=draw_height,
        preserveAspectRatio=True,
        anchor="c",
    )
    pdf.showPage()
    pdf.save()

    reader = PdfReader(str(OUTPUT))
    if len(reader.pages) != 1:
        raise RuntimeError(f"Expected one page, found {len(reader.pages)}")
    box = reader.pages[0].mediabox
    if abs(float(box.width) - page_width) > 0.5 or abs(float(box.height) - page_height) > 0.5:
        raise RuntimeError(f"Invalid A4 page geometry: {box}")
    resources = reader.pages[0].get("/Resources", {})
    if not resources.get("/XObject"):
        raise RuntimeError("CV image is missing from the generated PDF")

    print(
        f"Created {OUTPUT.name}: one A4 page, approved source {image_width}x{image_height}, "
        f"SHA256 {source_hash}"
    )


if __name__ == "__main__":
    build()
