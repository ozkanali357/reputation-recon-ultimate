from typing import Dict
import re


def parse_controls_from_text(text: str) -> Dict[str, bool]:
    """
    Extract security controls from vendor documentation/ToS text.
    
    Returns dict with boolean flags for common enterprise controls:
    - sso_saml: SSO/SAML support
    - mfa: Multi-factor authentication
    - rbac: Role-based access control
    - audit_logs: Audit logging
    - encryption_at_rest: Data encryption at rest
    """
    text_lower = text.lower()
    
    controls = {
        "sso_saml": False,
        "mfa": False,
        "rbac": False,
        "audit_logs": False,
        "encryption_at_rest": False
    }
    
    # SSO/SAML detection
    sso_patterns = [
        r"\bsso\b", r"\bsaml\b", r"single sign-on", r"okta", r"azure ad", r"google workspace"
    ]
    if any(re.search(p, text_lower) for p in sso_patterns):
        controls["sso_saml"] = True
    
    # MFA detection
    mfa_patterns = [
        r"\bmfa\b", r"\b2fa\b", r"two-factor", r"multi-factor", r"authenticator app"
    ]
    if any(re.search(p, text_lower) for p in mfa_patterns):
        controls["mfa"] = True
    
    # RBAC detection
    rbac_patterns = [
        r"\brbac\b", r"role-based access", r"permission", r"user roles", r"access control"
    ]
    if any(re.search(p, text_lower) for p in rbac_patterns):
        controls["rbac"] = True
    
    # Audit logs detection
    audit_patterns = [
        r"audit log", r"activity log", r"event log", r"compliance log"
    ]
    if any(re.search(p, text_lower) for p in audit_patterns):
        controls["audit_logs"] = True
    
    # Encryption detection
    encryption_patterns = [
        r"encryption at rest", r"aes-256", r"encrypted storage", r"data encryption"
    ]
    if any(re.search(p, text_lower) for p in encryption_patterns):
        controls["encryption_at_rest"] = True
    
    return controls