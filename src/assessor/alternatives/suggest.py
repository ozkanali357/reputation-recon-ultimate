from typing import List, Dict, Any, Optional
import yaml
from pathlib import Path

TAXONOMY_FILE = Path(__file__).parent / "taxonomy.yaml"


def load_taxonomy() -> Dict[str, List[Dict[str, str]]]:
    """Load category → alternatives mapping from taxonomy.yaml"""
    with open(TAXONOMY_FILE, "r") as f:
        return yaml.safe_load(f)


def suggest_alternatives(
    category: str,
    current_product: str,
    current_score: int,
    count: int = 2
) -> List[Dict[str, Any]]:
    """
    Suggest safer alternatives based on category and score.
    
    Args:
        category: Product category (e.g., "File archiver")
        current_product: Current product name
        current_score: Current product's trust score (0-100)
        count: Number of alternatives to suggest (default: 2)
    
    Returns:
        List of alternative products with rationale
    """
    taxonomy = load_taxonomy()
    
    # Get alternatives for this category
    category_alternatives = taxonomy.get(category, [])
    
    # Filter out the current product and sort by preference
    candidates = [
        alt for alt in category_alternatives 
        if alt["product"].lower() != current_product.lower()
    ]
    
    # If we have pre-scored alternatives, prefer higher-scored ones
    # Otherwise, use the curated order from taxonomy.yaml
    alternatives = []
    for candidate in candidates[:count]:
        rationale_parts = []
        
        # Add rationale based on known attributes
        if candidate.get("open_source"):
            rationale_parts.append("Open-source with community audits")
        
        if candidate.get("enterprise_support"):
            rationale_parts.append("Enterprise support available")
        
        if candidate.get("compliance"):
            rationale_parts.append(f"Compliance: {candidate['compliance']}")
        
        if candidate.get("fewer_cves"):
            rationale_parts.append("Lower CVE count historically")
        
        if candidate.get("active_psirt"):
            rationale_parts.append("Active PSIRT/security team")
        
        # Default rationale if no specific reasons
        if not rationale_parts:
            rationale_parts.append("Widely adopted alternative with good security track record")
        
        alternatives.append({
            "product": candidate["product"],
            "vendor": candidate.get("vendor", "Unknown"),
            "homepage": candidate.get("homepage", ""),
            "rationale": "; ".join(rationale_parts),
            "category": category
        })
    
    return alternatives


def generate_alternatives_brief(alternatives: List[Dict[str, Any]]) -> str:
    """Generate a human-readable alternatives section"""
    if not alternatives:
        return "## Safer Alternatives\n\nNo alternatives available for this category.\n"
    
    brief = "## Safer Alternatives\n\n"
    for idx, alt in enumerate(alternatives, 1):
        brief += f"### {idx}. {alt['product']}\n"
        brief += f"- **Vendor**: {alt['vendor']}\n"
        brief += f"- **Rationale**: {alt['rationale']}\n"
        if alt.get('homepage'):
            brief += f"- **Homepage**: {alt['homepage']}\n"
        brief += "\n"
    
    return brief