from typing import Any, Dict

def generate_brief(entity: Dict[str, Any], signals: Dict[str, Any], score: Dict[str, Any]) -> str:
    """Generate a concise CISO-ready brief."""
    vendor = entity.get("vendor", "Unknown")
    product = entity.get("product", "Unknown")
    category = entity.get("category", "Unknown")
    homepage = entity.get("homepage", "N/A")
    
    cve_stats = signals.get("nvd_cves", [])
    kev_count = sum(1 for cve in cve_stats if cve.get("in_kev"))
    critical_count = sum(1 for cve in cve_stats if cve.get("severity") == "CRITICAL")
    
    brief = f"""
# Security Assessment: {product}

**Vendor:** {vendor}  
**Category:** {category}  
**Homepage:** {homepage}  
**Trust Score:** {score["total_score"]}/100 (Confidence: {score["confidence"]:.1%})

## Summary
{product} is a {category} tool by {vendor}. Based on available evidence:
- **CVE Exposure:** {len(cve_stats)} total CVEs, {critical_count} critical, {kev_count} in CISA KEV.
- **Controls:** {score["components"]["controls"]["rationale"]}
- **Vendor Posture:** {score["components"]["vendor"]["rationale"]}
- **Compliance:** {score["components"]["compliance"]["rationale"]}

## Risk Assessment
{score["components"]["exposure"]["rationale"]}

## Recommendation
{"⚠️ High-risk due to KEV presence. Consider alternatives." if kev_count > 0 else "✅ Moderate risk. Review controls before deployment."}

---
*Generated with deterministic evidence. See citations for sources.*
"""
    return brief.strip()