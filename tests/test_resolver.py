import pytest

from src.assessor.resolver.resolver import resolve_entity


def test_resolve_entity_valid():
    result = resolve_entity("PeaZip", "PeaZip")
    assert result is not None
    assert result.vendor == "PeaZip"
    assert result.product == "PeaZip"
    assert result.category == "File archiver"


def test_resolve_entity_alias_strict_match():
    result = resolve_entity("PeaZip", "PeaZip Alias")
    assert result is not None
    assert result.vendor == "PeaZip"


def test_resolve_entity_unicode_alias():
    result = resolve_entity("PeaZip", " PeaZip Alias ")
    assert result is not None
    assert result.vendor == "PeaZip"


def test_resolve_entity_unicode_product():
    name = "Программное обеспечение"
    result = resolve_entity(name, "VendorName")
    assert result is not None
    assert result.product == name
    assert result.vendor == "VendorName"


def test_resolve_entity_collision_prefers_vendor_hint():
    result = resolve_entity("7-Zip", "7Z")
    assert result is not None
    assert result.vendor == "7-Zip"
    assert result.category == "File archiver"


def test_resolve_entity_invalid_product():
    assert resolve_entity("   ", "UnknownVendor") is None