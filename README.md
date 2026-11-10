# BidAgent: Autonomous Enterprise RFP & Tender Bid Strategist

## Overview
BidAgent is an end-to-end multi-module AI agent designed to ingest enterprise Requests for Proposals (RFPs), analyze critical requirements and disqualification risks, synthesize structured multi-section business proposals, allow interactive human-in-the-loop refinement, and automatically format and export final submissions to Microsoft Word (`.docx`).

## Key Features
- **Automated RFP Ingestion & Strategic Parsing**: Uses Gemini to analyze complex tender documents, extracting core technical criteria, constraints, and win strategies.
- **Dynamic Proposal Synthesis**: Automatically drafts executive summaries, technical architecture designs, milestone timelines, and value-engineered cost proposals.
- **Interactive Refinement Loop**: Empowers users to chat with the agent in real time, critique sections, and apply precise modifications before final locking.
- **Executive Document Formatting**: Leverages `python-docx` to output professionally styled Microsoft Word proposals complete with custom margins, typography, and hierarchy.

## Tech Stack
- **Language**: Python 3.x
- **AI Engine**: Google GenAI SDK (`gemini-3.5-flash-lite`)
- **Document Automation**: `python-docx`, `lxml`
