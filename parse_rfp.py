import os
from google import genai

# Initialize Gemini Client
client = genai.Client()

def analyze_rfp(rfp_text):
    prompt = f"""
    You are an expert Enterprise RFP & Tender Bid Strategist.
    Analyze the following Request for Proposal (RFP) text and extract:
    1. Executive Summary & Core Requirements
    2. Mandatory Eligibility & Technical Criteria
    3. Key Risks & Disqualification Factors
    4. Strategic Recommendations for Winning the Bid

    RFP TEXT:
    {rfp_text}
    """

    print("Analyzing RFP document with Gemini...")
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    return response.text

# Sample RFP text for testing
sample_rfp = """
Project: Autonomous AI Procurement System for Enterprise Logistics
Objective: Build a multi-agent system to automate supplier outreach and bid selection.
Key Requirements:
- Integration with REST APIs and SQL databases.
- Sub-second response time for bid ranking.
- Strict compliance with SOC2 Type II security guidelines.
- Budget cap: $150,000. Timeline: 8 weeks.
"""

if __name__ == "__main__":
    analysis = analyze_rfp(sample_rfp)
    print("\n================ BID STRATEGY ANALYSIS ================")
    print(analysis)