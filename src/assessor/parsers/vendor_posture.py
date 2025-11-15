from typing import Dict, Any
import requests
from pydantic import BaseModel, HttpUrl

class VendorPosture(BaseModel):
    vendor: str
    product: str
    security_page_url: HttpUrl
    psirt_url: HttpUrl
    bug_bounty: bool
    sla: str
    encryption_posture: str
    compliance_certifications: Dict[str, bool]

def parse_vendor_posture(vendor_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Input:
      {"vendor": "...", "security_posture": {"bug_bounty": bool, "psirt": bool}}
    Output:
      {"vendor": "...", "bug_bounty": bool, "psirt": bool}
    """
    sp = vendor_data.get("security_posture", {}) or {}
    return {
        "vendor": vendor_data.get("vendor"),
        "bug_bounty": bool(sp.get("bug_bounty")),
        "psirt": bool(sp.get("psirt")),
    }

def fetch_vendor_posture(vendor: str) -> VendorPosture:
    response = requests.get(f"https://api.example.com/vendor/{vendor}/posture")
    response.raise_for_status()
    vendor_data = response.json()
    return parse_vendor_posture(vendor_data)