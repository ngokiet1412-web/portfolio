"""Validate the exact approved CV PDF without rebuilding or modifying it."""

from __future__ import annotations

import hashlib
from pathlib import Path

from pypdf import PdfReader


PDF_PATH = Path(__file__).resolve().parents[1] / "NgoQuangKiet_CV_FINAL.pdf"
APPROVED_SHA256 = "cb012a7985054a0a806418eeb261abd9d093d7de093c849ae39236050064161c"
REQUIRED_TEXT = (
    "NGO QUANG KIET",
    "HCMUT",
    "FuelGuard",
    "EXPERIENCE",
    "EDUCATION",
)


def main() -> None:
    data = PDF_PATH.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != APPROVED_SHA256:
        raise SystemExit(f"CV hash mismatch: expected {APPROVED_SHA256}, got {digest}")

    reader = PdfReader(PDF_PATH)
    if reader.is_encrypted:
        raise SystemExit("CV must not be encrypted")
    if len(reader.pages) != 1:
        raise SystemExit(f"CV must have one page, got {len(reader.pages)}")

    page = reader.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    if abs(width - 595.276) > 1 or abs(height - 841.89) > 1:
        raise SystemExit(f"CV must be A4, got {width:.2f} x {height:.2f} pt")

    text = page.extract_text() or ""
    if len(text) < 2_000:
        raise SystemExit(f"CV text extraction is unexpectedly short: {len(text)} characters")
    missing = [phrase for phrase in REQUIRED_TEXT if phrase not in text]
    if missing:
        raise SystemExit(f"CV is missing required text: {', '.join(missing)}")

    print(f"Validated approved CV: SHA-256 {digest}, 1 A4 page, {len(text)} text characters")


if __name__ == "__main__":
    main()
