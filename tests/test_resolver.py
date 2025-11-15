from src.assessor.resolver.resolver import resolve_entity
import pytest

def test_resolve_entity_valid():
    # Test with a valid product name and vendor
    result = resolve_entity("PeaZip", "PeaZip")
    assert result['vendor'] == "PeaZip"
    assert result['product'] == "PeaZip"
    assert result['homepage'] is not None
    assert result['category'] == "File archiver"

def test_resolve_entity_alias():
    # Test with an alias
    result = resolve_entity("PeaZip", "PeaZip Alias")
    assert result['vendor'] == "PeaZip"
    assert result['product'] == "PeaZip"
    assert result['homepage'] is not None

def test_resolve_entity_invalid():
    # Test with an invalid product name
    result = resolve_entity("InvalidProduct", "UnknownVendor")
    assert result is None

def test_resolve_entity_unicode():
    # Test with a unicode product name
    result = resolve_entity("Программное обеспечение", "VendorName")
    assert result['vendor'] == "VendorName"
    assert result['product'] == "Программное обеспечение"
    assert result['homepage'] is not None

def test_resolve_entity_collision():
    # Test with a name that causes a collision
    result = resolve_entity("CommonName", "VendorA")
    assert result['vendor'] in ["VendorA", "VendorB"]
    assert result['product'] == "CommonName"