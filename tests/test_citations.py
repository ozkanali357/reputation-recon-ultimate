import pytest
from assessor.models.evidence import Evidence
from assessor.models.claim import Claim

def test_evidence_creation():
    evidence = Evidence(
        claim_id=1,
        url="https://example.com",
        source_type="vendor",
        excerpt="This is a sample excerpt.",
        retrieved_at="2023-10-01T12:00:00Z",
        parser_id="parser_1"
    )
    assert evidence.claim_id == 1
    assert evidence.url == "https://example.com"
    assert evidence.source_type == "vendor"
    assert evidence.excerpt == "This is a sample excerpt."
    assert evidence.retrieved_at == "2023-10-01T12:00:00Z"
    assert evidence.parser_id == "parser_1"

def test_claim_creation():
    claim = Claim(
        id=1,
        product_id=1,
        category="Security",
        text="This product has a known vulnerability.",
        score_contrib=10,
        confidence=0.9
    )
    assert claim.id == 1
    assert claim.product_id == 1
    assert claim.category == "Security"
    assert claim.text == "This product has a known vulnerability."
    assert claim.score_contrib == 10
    assert claim.confidence == 0.9

def test_evidence_association():
    claim = Claim(
        id=1,
        product_id=1,
        category="Security",
        text="This product has a known vulnerability.",
        score_contrib=10,
        confidence=0.9
    )
    evidence = Evidence(
        claim_id=claim.id,
        url="https://example.com",
        source_type="vendor",
        excerpt="This is a sample excerpt.",
        retrieved_at="2023-10-01T12:00:00Z",
        parser_id="parser_1"
    )
    assert evidence.claim_id == claim.id
    assert evidence.url == "https://example.com"