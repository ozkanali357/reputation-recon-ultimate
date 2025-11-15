from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime

class Evidence(BaseModel):
    claim_id: str
    url: str
    source_type: str
    excerpt: str
    retrieved_at: datetime
    parser_id: str

class Claim(BaseModel):
    id: str
    product_id: str
    category: str
    text: str
    score_contrib: float
    confidence: float

class Summary(BaseModel):
    claims: List[Claim]
    evidences: List[Evidence]

def generate_summary(claims: List[Claim], evidences: List[Evidence]) -> Summary:
    return Summary(claims=claims, evidences=evidences)

def format_summary(summary: Summary) -> str:
    formatted = "Summary Report\n\n"
    for claim in summary.claims:
        formatted += f"Claim ID: {claim.id}\n"
        formatted += f"Product ID: {claim.product_id}\n"
        formatted += f"Category: {claim.category}\n"
        formatted += f"Text: {claim.text}\n"
        formatted += f"Score Contribution: {claim.score_contrib}\n"
        formatted += f"Confidence: {claim.confidence}\n\n"
    
    formatted += "Evidences:\n"
    for evidence in summary.evidences:
        formatted += f"Claim ID: {evidence.claim_id}\n"
        formatted += f"URL: {evidence.url}\n"
        formatted += f"Source Type: {evidence.source_type}\n"
        formatted += f"Excerpt: {evidence.excerpt}\n"
        formatted += f"Retrieved At: {evidence.retrieved_at}\n"
        formatted += f"Parser ID: {evidence.parser_id}\n\n"
    
    return formatted.strip()