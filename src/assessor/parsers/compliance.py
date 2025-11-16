from typing import Dict
import re


def parse_compliance_from_text(text: str) -> Dict[str, bool]:
    """
    Extract compliance attestations from vendor documentation.
    
    Returns dict with boolean flags for common compliance standards:
    - soc2_type2: SOC 2 Type II certification
    - iso_27001: ISO 27001 certification
    - gdpr_dpa: GDPR Data Processing Agreement
    - hipaa: HIPAA compliance
    - fedramp: FedRAMP authorization
    """
    text_lower = text.lower()
    
    compliance = {
        "soc2_type2": False,
        "iso_27001": False,
        "gdpr_dpa": False,
        "hipaa": False,
        "fedramp": False
    }
    
    # SOC 2 Type II detection
    soc2_patterns = [
        r"soc 2 type ii", r"soc2 type 2", r"soc 2®", r"service organization control"
    ]
    if any(re.search(p, text_lower) for p in soc2_patterns):
        compliance["soc2_type2"] = True
    
    # ISO 27001 detection
    iso_patterns = [
        r"iso 27001", r"iso/iec 27001", r"iso27001"
    ]
    if any(re.search(p, text_lower) for p in iso_patterns):
        compliance["iso_27001"] = True
    
    # GDPR DPA detection
    gdpr_patterns = [
        r"\bgdpr\b", r"data processing agreement", r"dpa", r"general data protection"
    ]
    if any(re.search(p, text_lower) for p in gdpr_patterns):
        compliance["gdpr_dpa"] = True
    
    # HIPAA detection
    hipaa_patterns = [
        r"\bhipaa\b", r"health insurance portability", r"phi protection"
    ]
    if any(re.search(p, text_lower) for p in hipaa_patterns):
        compliance["hipaa"] = True
    
    # FedRAMP detection
    fedramp_patterns = [
        r"fedramp", r"federal risk and authorization"
    ]
    if any(re.search(p, text_lower) for p in fedramp_patterns):
        compliance["fedramp"] = True
    
    return compliance