# Ngo Quang Kiet - Automotive Engineering Portfolio

Static portfolio deployed from `main`.

## CV source custody

- Approved visual source: `D:\cv.jpg`
- Repository copy: `assets/cv-approved-source.jpg`
- Locked SHA-256: `716ff6b78460d4582727fe385678a1d65338b80d7e12a36c49ba9c8280fafb5a`
- Output: one-page A4 `NgoQuangKiet_CV_FINAL.pdf`

Rebuild with:

```powershell
python scripts/build_cv_pdf.py
```

The builder stops if the repository source image no longer matches the approved hash.
