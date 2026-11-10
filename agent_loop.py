import os
from google import genai
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

client = genai.Client()

def run_bid_agent():
    print("==================================================")
    print(" BIDAGENT: AUTONOMOUS RFP STRATEGIST ")
    print("==================================================")
    
    # 1. Ingest RFP
    rfp_file = "sample_tender.txt"
    if not os.path.exists(rfp_file):
        print(f"Error: {rfp_file} not found.")
        return
    
    with open(rfp_file, 'r', encoding='utf-8') as f:
        rfp_text = f.read()

    print("\n[1/3] Analyzing RFP requirements and formulating win strategy...")
    analysis_prompt = f"""
    You are an expert Enterprise Bid Strategist. Analyze this RFP:
    {rfp_text}
    Provide Executive Summary, Technical Criteria, Disqualification Risks, and Win Strategy.
    """
    analysis_res = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=analysis_prompt
    )
    analysis = analysis_res.text
    print(">>> RFP analysis complete.")

    # 2. Initial Draft Generation
    print("\n[2/3] Synthesizing initial multi-section proposal draft...")
    draft_prompt = f"""
    Using this RFP Analysis:
    {analysis}
    Draft a comprehensive, professional enterprise bid proposal with 4 core sections:
    1. Executive Summary & Value Proposition
    2. Proposed Technical Architecture & Solution Design
    3. Project Milestone Breakdown & Timeline
    4. Cost Proposal & Value-Engineered Pricing
    """
    draft_res = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=draft_prompt
    )
    proposal_text = draft_res.text
    print(">>> Initial proposal drafted successfully.")

    # 3. Interactive Agentic Refinement Loop
    print("\n[3/3] Entering Interactive Refinement Phase...")
    while True:
        print("\n--------------------------------------------------")
        print("OPTIONS:")
        print(" - Type your feedback/critique to refine the proposal (e.g., 'Make the pricing section more competitive')")
        print(" - Type 'export' to generate the final Word document")
        print(" - Type 'exit' to quit")
        print("--------------------------------------------------")
        
        user_input = input("Executor Command > ").strip()
        
        if user_input.lower() == 'exit':
            print("Exiting BidAgent session.")
            break
        elif user_input.lower() == 'export':
            export_to_word(proposal_text, "Final_Bid_Proposal.docx")
            break
        elif user_input:
            print("\nRefining proposal based on your feedback...")
            refine_prompt = f"""
            You are an expert Enterprise Bid Writer. 
            Here is the current proposal:
            {proposal_text}
            
            User Feedback / Requested Modification:
            {user_input}
            
            Rewrite or update the proposal to fully incorporate this feedback while maintaining professional tone and structure. Output the updated full proposal.
            """
            refine_res = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=refine_prompt
            )
            proposal_text = refine_res.text
            print(">>> Proposal updated successfully! Review preview or export.")
            print(proposal_text[:600] + "\n...[truncated for preview]...\n")

def export_to_word(text, docx_filename):
    print(f"\nExporting polished proposal to {docx_filename}...")
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(51, 51, 51)

    for line in text.split('\n'):
        cleaned = line.strip()
        if not cleaned:
            continue
        if cleaned.startswith("## ") or cleaned.startswith("### "):
            heading = doc.add_heading(cleaned.replace("## ", "").replace("### ", "").strip(), level=2)
            heading.paragraph_format.space_before = Pt(14)
            heading.paragraph_format.space_after = Pt(6)
            for run in heading.runs:
                run.font.name = 'Calibri'
                run.font.color.rgb = RGBColor(16, 44, 87)
                run.font.bold = True
        elif cleaned.startswith("# "):
            title = doc.add_heading(cleaned.replace("# ", "").strip(), level=1)
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            title.paragraph_format.space_after = Pt(12)
            for run in title.runs:
                run.font.name = 'Calibri'
                run.font.color.rgb = RGBColor(16, 44, 87)
                run.font.bold = True
        elif cleaned.startswith("* ") or cleaned.startswith("- "):
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(3)
            p.add_run(cleaned[2:].strip())
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
            p.add_run(cleaned)

    doc.save(docx_filename)
    print(f"================ SUCCESS! ================")
    print(f"Saved: {docx_filename}")

if __name__ == "__main__":
    run_bid_agent()