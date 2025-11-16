import re
from typing import Dict, Optional
import httpx
from bs4 import BeautifulSoup


def fetch_vendor_posture(homepage: str, vendor: str, timeout: int = 10) -> Dict[str, bool]:
    """
    Fetch vendor security posture signals from homepage and common paths.
    
    Returns dict with boolean flags:
    - psirt_page: Has dedicated security/PSIRT page
    - bug_bounty: Has bug bounty program
    - security_advisories: Publishes security advisories
    - transparency_report: Has transparency report
    """
    signals = {
        "psirt_page": False,
        "bug_bounty": False,
        "security_advisories": False,
        "transparency_report": False
    }
    
    # Common security page paths
    security_paths = [
        "/security",
        "/trust",
        "/psirt",
        "/responsible-disclosure",
        "/bug-bounty",
        "/security-advisories"
    ]
    
    try:
        # Fetch homepage
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            response = client.get(homepage)
            if response.status_code != 200:
                return signals
            
            soup = BeautifulSoup(response.text, "html.parser")
            text_content = soup.get_text().lower()
            
            # Check for security keywords
            if any(kw in text_content for kw in ["security", "psirt", "vulnerability", "responsible disclosure"]):
                signals["psirt_page"] = True
            
            if any(kw in text_content for kw in ["bug bounty", "hackerone", "bugcrowd", "vulnerability reward"]):
                signals["bug_bounty"] = True
            
            if any(kw in text_content for kw in ["security advisory", "security bulletin", "cve-"]):
                signals["security_advisories"] = True
            
            if "transparency report" in text_content:
                signals["transparency_report"] = True
            
            # Try fetching dedicated security pages
            base_url = homepage.rstrip("/")
            for path in security_paths:
                try:
                    sec_response = client.get(f"{base_url}{path}")
                    if sec_response.status_code == 200:
                        sec_text = sec_response.text.lower()
                        if "security" in sec_text or "vulnerability" in sec_text:
                            signals["psirt_page"] = True
                        if "bug bounty" in sec_text:
                            signals["bug_bounty"] = True
                        break
                except:
                    continue
    
    except Exception as e:
        # Fail gracefully - return empty signals
        pass
    
    return signals


def fetch_vendor_posture_sync(homepage: str, vendor: str, offline: bool = False, snapshot_id: Optional[str] = None) -> Dict[str, bool]:
    """Synchronous wrapper with offline/snapshot support"""
    if offline or snapshot_id:
        # Return empty signals in offline mode
        return {
            "psirt_page": False,
            "bug_bounty": False,
            "security_advisories": False,
            "transparency_report": False
        }
    
    return fetch_vendor_posture(homepage, vendor)