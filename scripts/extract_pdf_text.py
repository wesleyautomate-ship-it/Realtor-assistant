#!/usr/bin/env python3
"""
Extract text from a PDF and write a .txt file alongside it.

Usage:
  python scripts/extract_pdf_text.py path/to/file.pdf [--out path/to/output.txt]

Dependencies:
  pip install pdfminer.six

Notes:
- The script writes UTF-8 text and attempts to preserve simple layout.
- Large PDFs may take time; run from project root for relative paths.
"""
import argparse
import sys
from pathlib import Path

try:
    from pdfminer.high_level import extract_text
except Exception as e:
    print("Error: pdfminer.six is not installed. Install with: pip install pdfminer.six", file=sys.stderr)
    raise

def main():
    parser = argparse.ArgumentParser(description="Extract text from a PDF to a .txt file")
    parser.add_argument("pdf", type=str, help="Path to the PDF file")
    parser.add_argument("--out", type=str, default=None, help="Optional output .txt path")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.out) if args.out else pdf_path.with_suffix(".txt")

    print(f"Reading: {pdf_path}")
    text = extract_text(str(pdf_path))

    # Basic normalization
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    out_path.write_text(text, encoding="utf-8")
    print(f"Wrote: {out_path} ({len(text)} chars)")

if __name__ == "__main__":
    main()
