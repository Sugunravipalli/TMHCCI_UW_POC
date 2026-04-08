"""
Convert all .txt files in folders 03, 04, 09, 10 to PDF format
for Snowflake PARSE_DOCUMENT compatibility.
"""

from fpdf import FPDF
from pathlib import Path


BASE = Path(r"C:\Users\bharg\Downloads\OneDrive_2026-04-07\Tokio Marine\Tokio Marine POC - London\synthetic_data")


class UWDocPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "TOKIO MARINE HCC INTERNATIONAL - CONFIDENTIAL", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def txt_to_pdf(txt_path: Path, pdf_path: Path):
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    pdf = UWDocPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    for line in content.split("\n"):
        stripped = line.rstrip()

        # Separator lines (=== or ---)
        if stripped.strip() and all(c in "=" for c in stripped.strip()) and len(stripped.strip()) > 10:
            pdf.set_draw_color(0, 51, 102)
            pdf.set_line_width(0.5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(2)
            continue

        if stripped.strip() and all(c in "-" for c in stripped.strip()) and len(stripped.strip()) > 10:
            pdf.set_draw_color(180, 180, 180)
            pdf.set_line_width(0.3)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(2)
            continue

        # All-caps title lines
        s = stripped.strip()
        if s and s.isupper() and len(s) > 10 and "|" not in s and "[" not in s:
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(0, 51, 102)
            pdf.multi_cell(0, 5, s, align="C")
            pdf.ln(1)
            continue

        # Empty lines
        if not s:
            pdf.ln(2)
            continue

        # Everything else: monospace body text
        pdf.set_font("Courier", "", 8)
        pdf.set_text_color(0, 0, 0)
        # Truncate very long lines to fit page
        display = stripped[:130] if len(stripped) > 130 else stripped
        pdf.cell(0, 3.5, display, new_x="LMARGIN", new_y="NEXT")

    pdf.output(str(pdf_path))


def convert_folder(folder_name: str):
    folder = BASE / folder_name
    txt_files = sorted(folder.glob("*.txt"))
    if not txt_files:
        print(f"  {folder_name}: no .txt files found")
        return 0

    count = 0
    for txt_file in txt_files:
        pdf_name = txt_file.stem + ".pdf"
        pdf_path = folder / pdf_name
        try:
            txt_to_pdf(txt_file, pdf_path)
            count += 1
            print(f"  Created: {pdf_name}")
        except Exception as e:
            print(f"  ERROR on {txt_file.name}: {e}")

    return count


if __name__ == "__main__":
    print("=" * 60)
    print("  Converting .txt to PDF for Snowflake PARSE_DOCUMENT")
    print("=" * 60)

    total = 0
    for folder in ["03_applications", "04_loss_runs", "09_uw_guidelines", "10_authority_letters"]:
        print(f"\n{folder}/")
        total += convert_folder(folder)

    print(f"\n{'=' * 60}")
    print(f"  Done. {total} PDFs created.")
    print(f"{'=' * 60}")
