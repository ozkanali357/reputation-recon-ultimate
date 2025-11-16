def test_calculate_trust_score_basic():
    """Test the trust score calculation with basic inputs."""
    from assessor.scoring.engine import calculate_trust_score
    
    # Test case 1: No CVEs, no signals (baseline)
    signals = {
        "nvd_cves": [],
        "cisa_kev": [],
        "controls": {},
        "vendor_posture": {},
        "compliance": {}
    }
    
    result = calculate_trust_score(signals)
    
    # Should have basic structure
    assert "total_score" in result
    assert "max_score" in result
    assert "confidence" in result
    assert "components" in result
    assert result["max_score"] == 100
    assert 0 <= result["total_score"] <= 100
    assert 0 <= result["confidence"] <= 1.0


def test_calculate_trust_score_with_cves():
    """Test scoring with CVE data."""
    from assessor.scoring.engine import calculate_trust_score
    
    signals = {
        "nvd_cves": [
            {"id": "CVE-2021-12345", "severity": "CRITICAL", "in_kev": True},
            {"id": "CVE-2021-12346", "severity": "HIGH", "in_kev": False}
        ],
        "cisa_kev": [],
        "controls": {},
        "vendor_posture": {},
        "compliance": {}
    }
    
    result = calculate_trust_score(signals)
    
    # KEV presence should lower the score
    assert result["total_score"] < 50  # Severe penalty for KEV
    assert result["components"]["exposure"]["score"] < 20
    assert "KEV hits: 1" in result["components"]["exposure"]["rationale"]


def test_calculate_trust_score_with_controls():
    """Test scoring with security controls."""
    from assessor.scoring.engine import calculate_trust_score
    
    signals = {
        "nvd_cves": [],
        "cisa_kev": [],
        "controls": {
            "sso_saml": True,
            "mfa": True,
            "rbac": True,
            "audit_logs": True,
            "encryption_at_rest": True
        },
        "vendor_posture": {},
        "compliance": {}
    }
    
    result = calculate_trust_score(signals)
    
    # Controls should increase the score
    assert result["components"]["controls"]["score"] == 20  # Max controls score
    assert "SSO/SAML" in result["components"]["controls"]["rationale"]


def test_calculate_trust_score_with_compliance():
    """Test scoring with compliance attestations."""
    from assessor.scoring.engine import calculate_trust_score
    
    signals = {
        "nvd_cves": [],
        "cisa_kev": [],
        "controls": {},
        "vendor_posture": {},
        "compliance": {
            "soc2_type2": True,
            "iso_27001": True,
            "gdpr_dpa": True
        }
    }
    
    result = calculate_trust_score(signals)
    
    # Compliance should increase the score
    assert result["components"]["compliance"]["score"] == 15  # Max compliance score
    assert "SOC 2 Type II" in result["components"]["compliance"]["rationale"]