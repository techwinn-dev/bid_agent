import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def convert_txt_to_docx(txt_filename, docx_filename):
    if not os.path.exists(txt_filename):
        print(f"Error: Could not find '{txt_filename}'. Generate the proposal first.")
        return

    print(f"Reading '{txt_filename}' and formatting into Word document...")

    doc = Document()

    # Set page margins (1 inch on all sides)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Base Font Setup
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(51, 51, 51) # Charcoal black

    with open(txt_filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        cleaned_line = line.strip()

        if not cleaned_line:
            continue

        # Header detection and formatting
        if cleaned_line.startswith("## ") or cleaned_line.startswith("### "):
            heading_text = cleaned_line.replace("## ", "").replace("### ", "").strip()
            heading = doc.add_heading(heading_text, level=2)
            heading.paragraph_format.space_before = Pt(14)
            heading.paragraph_format.space_after = Pt(6)
            for run in heading.runs:
                run.font.name = 'Calibri'
                run.font.color.rgb = RGBColor(16, 44, 87) # Executive Dark Navy
                run.font.bold = True

        elif cleaned_line.startswith("# "):
            heading_text = cleaned_line.replace("# ", "").strip()
            title = doc.add_heading(heading_text, level=1)
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            title.paragraph_format.space_after = Pt(12)
            for run in title.runs:
                run.font.name = 'Calibri'
                run.font.color.rgb = RGBColor(16, 44, 87)
                run.font.bold = True

        elif cleaned_line.startswith("* ") or cleaned_line.startswith("- "):
            bullet_text = cleaned_line[2:].strip()
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(3)
            parse_bold_runs(p, bullet_text)

        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
            parse_bold_runs(p, cleaned_line)

    doc.save(docx_filename)
    print(f"\n================ SUCCESS! ================")
    print(f"Formatted Word proposal saved cleanly to: {docx_filename}")

def parse_bold_runs(paragraph, text):
    """Parses markdown bolding (**text**) into actual Word bold runs."""
    parts = text.split("**")
    for i, part in enumerate(parts):
        if not part:
            continue
        run = paragraph.add_run(part)
        if i % 2 == 1: # Odd index means it was inside ** **
            run.bold = True

if __name__ == "__main__":
    convert_txt_to_docx("generated_proposal.txt", "Final_Bid_Proposal.docx")