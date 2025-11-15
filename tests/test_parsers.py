import pytest
from src.assessor.parsers.cve import parse_cve_data
from src.assessor.parsers.vendor_posture import parse_vendor_posture
from src.assessor.parsers.controls import parse_controls
from src.assessor.parsers.compliance import parse_compliance

def test_parse_cve_data():
    sample_data = {
        "CVE_data_meta": {
            "ID": "CVE-2021-12345",
            "ASSIGNER": "cve@mitre.org"
        },
        "impact": {
            "baseMetricV3": {
                "cvssV3": {
                    "baseScore": 7.5
                }
            }
        }
    }
    result = parse_cve_data(sample_data)
    assert result['id'] == "CVE-2021-12345"
    assert result['score'] == 7.5

def test_parse_vendor_posture():
    sample_data = {
        "vendor": "ExampleVendor",
        "security_posture": {
            "bug_bounty": True,
            "psirt": True
        }
    }
    result = parse_vendor_posture(sample_data)
    assert result['vendor'] == "ExampleVendor"
    assert result['bug_bounty'] is True
    assert result['psirt'] is True

def test_parse_controls():
    sample_data = {
        "controls": {
            "encryption": True,
            "multi_factor_authentication": False
        }
    }
    result = parse_controls(sample_data)
    assert result['encryption'] is True
    assert result['multi_factor_authentication'] is False

def test_parse_compliance():
    sample_data = {
        "compliance": {
            "soc2": True,
            "iso27001": False
        }
    }
    result = parse_compliance(sample_data)
    assert result['soc2'] is True
    assert result['iso27001'] is False