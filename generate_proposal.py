import os
from google import genai

client = genai.Client()

def synthesize_proposal(rfp_filename, company_profile):
    # 1. Read the RFP analysis file
    if not os.path.exists(rfp_filename):
        print(f"Error: Could not find '{rfp_filename}'. Run your parser module first.")
        return

    with open(rfp_filename, 'r', encoding='utf-8') as f:
        rfp_content = f.read()

    # 2. Construct the prompt for Section Generation
    prompt = f"""
    You are an expert Enterprise Bid Writer and Proposal Synthesizer.
    Using the RFP requirements analysis below and our company profile, draft a professional, compelling, and compliant business proposal.

    Generate the following 4 core proposal sections:
    1. Executive Summary & Value Proposition
    2. Proposed Technical Architecture & Solution Design
    3. Project Milestone Breakdown & Timeline
    4. Cost Proposal & Value-Engineered Pricing

    RFP ANALYSIS CONTEXT:
    {rfp_content}

    OUR COMPANY PROFILE:
    {company_profile}
    """

    print("Generating comprehensive proposal sections with Gemini...")
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    # 3. Save the output to a new proposal text file
    output_filename = "generated_proposal.txt"
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        out_file.write(response.text)

    print(f"\n================ SUCCESS! ================")
    print(f"Proposal successfully drafted and saved to: {output_filename}")
    print(response.text[:1500] + "\n\n[...truncated for preview...]")

if __name__ == "__main__":
    # Target the analysis file generated in Module 1
    analysis_file = "sample_tender.txt" # Or read your parsed output text
    
    # Define your team/company background
    my_company = """
    Company Name: TechVanguard Enterprise Solutions
    Core Competencies: Cloud infrastructure migration, multi-agent AI orchestration, SOC2 compliant security frameworks, and rapid 12-week enterprise deployment pipelines.
    """
    
    synthesize_proposal("sample_tender.txt", my_company)