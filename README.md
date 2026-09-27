# Ngo Quang Kiet - Automotive Engineering Portfolio

Static portfolio deployed from `main`.

## CV source custody

- Approved source: `D:\NgoQuangKiet_CV.pdf`
- Repository copy: `NgoQuangKiet_CV_FINAL.pdf`
- Locked SHA-256: `cb012a7985054a0a806418eeb261abd9d093d7de093c849ae39236050064161c`
- Format: one-page A4 PDF with selectable text

Validate with:

```powershell
python scripts/validate_cv_pdf.py
```

The validator stops if the PDF changes, loses its A4 page geometry, or no longer contains the expected selectable text. It never rebuilds or overwrites the approved file.
