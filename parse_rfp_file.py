import os
from google import genai

client = genai.Client()

def analyze_rfp_file(filename):
    # Check if the file exists in the folder
    if not os.path.exists(filename):
        print(f"Error: Could not find '{filename}' in the bid_agent folder.")
        print("Please save your RFP text file into C:\\Users\\user\\Desktop\\bid_agent\\")
        return

    # Read the file contents
    with open(filename, 'r', encoding='utf-8') as f:
        rfp_text = f.read()

    prompt = f"""
    You are an expert Enterprise RFP & Tender Bid Strategist.
    Analyze the following Request for Proposal (RFP) document and provide:
    1. Executive Summary & Core Requirements
    2. Mandatory Eligibility & Technical Criteria
    3. Key Risks & Disqualification Factors
    4. Strategic Recommendations for Winning the Bid

    RFP DOCUMENT TEXT:
    {rfp_text}
    """

    print(f"Analyzing '{filename}' with Gemini...")
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    
    print("\n================ BID STRATEGY ANALYSIS ================")
    print(response.text)

if __name__ == "__main__":
    # You can name your uploaded/created text file whatever you like
    target_file = "sample_tender.txt"
    analyze_rfp_file(target_file)