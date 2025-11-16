from typing import Any, Dict, List

def _aggregate_cve_stats(cve_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate CVE list into stats dict."""
    kev_hits = sum(1 for cve in cve_list if cve.get("in_kev"))
    critical_count = sum(1 for cve in cve_list if cve.get("severity") == "CRITICAL")
    # Placeholder: count CVEs from last 12 months (requires date parsing)
    last_12m_count = 0  # TODO: parse published dates
    
    return {
        "kev_hits": kev_hits,
        "critical_count": critical_count,
        "last_12m_count": last_12m_count,
        "total_count": len(cve_list),
    }

def score_exposure(cve_stats: Dict[str, Any]) -> Dict[str, Any]:
    """Score based on CVE/KEV data (0-30 points)."""
    kev_count = cve_stats.get("kev_hits", 0)
    critical_count = cve_stats.get("critical_count", 0)
    recent_velocity = cve_stats.get("last_12m_count", 0)
    
    score = 30
    if kev_count > 0:
        score -= 15  # KEV presence is severe
    if critical_count > 5:
        score -= 10
    elif critical_count > 0:
        score -= 5
    if recent_velocity > 10:
        score -= 5
    
    return {
        "score": max(0, score),
        "max": 30,
        "rationale": f"KEV hits: {kev_count}, Critical CVEs: {critical_count}, Recent velocity: {recent_velocity}",
    }


def score_controls(controls: Dict[str, Any]) -> Dict[str, Any]:
    """Score based on admin/deployment controls (0-20 points)."""
    score = 0
    checks = []
    
    if controls.get("sso_saml"):
        score += 6
        checks.append("SSO/SAML")
    if controls.get("mfa"):
        score += 5
        checks.append("MFA")
    if controls.get("rbac"):
        score += 4
        checks.append("RBAC")
    if controls.get("audit_logs"):
        score += 3
        checks.append("Audit logs")
    if controls.get("encryption_at_rest"):
        score += 2
        checks.append("Encryption at rest")
    
    return {
        "score": score,
        "max": 20,
        "rationale": f"Controls present: {', '.join(checks) or 'None detected'}",
    }


def score_vendor(vendor_posture: Dict[str, Any]) -> Dict[str, Any]:
    """Score vendor security posture (0-15 points)."""
    score = 0
    signals = []
    
    if vendor_posture.get("psirt_page"):
        score += 5
        signals.append("PSIRT page")
    if vendor_posture.get("bug_bounty"):
        score += 4
        signals.append("Bug bounty")
    if vendor_posture.get("security_advisories"):
        score += 3
        signals.append("Security advisories")
    if vendor_posture.get("transparency_report"):
        score += 3
        signals.append("Transparency report")
    
    return {
        "score": score,
        "max": 15,
        "rationale": f"Vendor signals: {', '.join(signals) or 'None detected'}",
    }


def score_compliance(compliance: Dict[str, Any]) -> Dict[str, Any]:
    """Score compliance attestations (0-15 points)."""
    score = 0
    certs = []
    
    if compliance.get("soc2_type2"):
        score += 7
        certs.append("SOC 2 Type II")
    if compliance.get("iso_27001"):
        score += 5
        certs.append("ISO 27001")
    if compliance.get("gdpr_dpa"):
        score += 3
        certs.append("GDPR/DPA")
    
    return {
        "score": score,
        "max": 15,
        "rationale": f"Compliance: {', '.join(certs) or 'None detected'}",
    }


def calculate_trust_score(brief, cve_stats, cisa_kev, entity):
    """Enhanced scoring with 6-component breakdown"""
    
    weights = load_weights()  # From weights.yaml
    
    scores = {
        'vulnerability_exposure': score_vulnerability_exposure(cve_stats, cisa_kev),
        'vendor_maturity': score_vendor_maturity(brief.get('vendor_reputation', {})),
        'compliance_coverage': score_compliance(brief.get('data_handling', {})),
        'incident_history': score_incidents(brief.get('incidents', {})),
        'controls_capability': score_controls(brief.get('controls', {})),
        'data_handling': score_data_security(brief.get('data_handling', {}))
    }
    
    total = sum(scores[k] * weights[k] for k in scores)
    
    # Determine confidence
    data_points = sum([
        1 if cve_stats['total'] > 0 else 0,
        1 if brief.get('vendor_reputation', {}).get('psirt_maturity') else 0,
        1 if len(brief.get('data_handling', {}).get('compliance', [])) > 0 else 0,
        1 if cisa_kev else 0
    ])
    
    confidence = 'high' if data_points >= 3 else 'medium' if data_points >= 2 else 'low'
    
    # Generate rationale (reputation-recon style)
    rationale = f"Score based on {cve_stats['total']} CVEs analyzed ({cve_stats['critical']} critical, {cve_stats['high']} high), "
    rationale += f"{len(cisa_kev)} CISA KEV entries, "
    rationale += f"{brief.get('vendor_reputation', {}).get('psirt_maturity', 'unknown')} PSIRT maturity, "
    rationale += f"and {len(brief.get('data_handling', {}).get('compliance', []))} compliance attestations."
    
    if confidence == 'low':
        rationale += " Limited public data - recommend direct vendor assessment."
    
    return {
        'value': round(total),
        'confidence': confidence,
        'rationale': rationale,
        'breakdown': [
            {
                'component': k.replace('_', ' ').title(),
                'score': scores[k],
                'weight': weights[k]
            }
            for k in scores
        ]
    }