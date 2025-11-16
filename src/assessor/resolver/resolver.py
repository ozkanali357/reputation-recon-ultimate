from __future__ import annotations

import csv
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel
from rapidfuzz import fuzz, process

_ALIAS_FILE = Path(__file__).with_name("aliases.csv")
_PRODUCTS_DB = Path(__file__).with_name("products_db.csv")

# Load product hints from CSV
@lru_cache
def _load_product_hints() -> Dict[str, Dict[str, str]]:
    """Load product hints from products_db.csv"""
    hints = {}
    if not _PRODUCTS_DB.exists():
        return hints
    
    with open(_PRODUCTS_DB, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            product_key = _normalize_text(row["product_name"]).lower()
            hints[product_key] = {
                "vendor": row["company_name"],
                "category": row.get("category", "Unknown"),
                "homepage": row.get("homepage", "https://example.com/"),
            }
            # Also add SHA1 lookup
            if row.get("sha1"):
                hints[row["sha1"].lower()] = hints[product_key]
    
    return hints

DEFAULT_HOMEPAGE = "https://example.com/"
DEFAULT_CATEGORY = "Unknown"


class EntityResolutionResult(BaseModel):
    vendor: str
    product: str
    homepage: str
    category: str
    identifiers: Dict[str, Any] = {}
    source: str = "resolver"


def _normalize_text(value: Optional[str]) -> str:
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKC", value)
    return " ".join(normalized.split())


@lru_cache
def _alias_map() -> Dict[str, str]:
    if not _ALIAS_FILE.exists():
        return {}
    return _load_aliases(_ALIAS_FILE)


def _load_aliases(path: Path) -> Dict[str, str]:
    alias_map = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vendor = row["vendor"]
            alias = row["alias"]
            alias_map[alias.lower()] = vendor
    return alias_map


def _canonicalize_vendor(vendor: Optional[str]) -> Optional[str]:
    if not vendor:
        return None
    vendor_norm = _normalize_text(vendor)
    aliases = _alias_map()
    return aliases.get(vendor_norm.lower(), vendor_norm)


def _choose_homepage(product_key: str, provided_url: Optional[str]) -> str:
    if provided_url:
        return provided_url
    hints = _load_product_hints()
    return hints.get(product_key, {}).get("homepage", DEFAULT_HOMEPAGE)


def _choose_category(product_key: str) -> str:
    hints = _load_product_hints()
    return hints.get(product_key, {}).get("category", DEFAULT_CATEGORY)


def resolve_entity(
    product: str,
    vendor: Optional[str] = None,
    url: Optional[str] = None,
    sha1: Optional[str] = None,
) -> Optional[EntityResolutionResult]:
    product_norm = _normalize_text(product)
    if not product_norm:
        return None

    product_key = product_norm.lower()
    hints = _load_product_hints()
    
    # Try SHA1 lookup first
    if sha1:
        sha1_hints = hints.get(sha1.lower(), {})
        if sha1_hints:
            return EntityResolutionResult(
                vendor=sha1_hints.get("vendor", product_norm),
                product=product_norm,
                homepage=sha1_hints.get("homepage", DEFAULT_HOMEPAGE),
                category=sha1_hints.get("category", DEFAULT_CATEGORY),
                identifiers={"sha1": sha1},
                source="resolver_sha1"
            )
    
    # Try product name lookup
    product_hints = hints.get(product_key, {})
    resolved_vendor = (
        _canonicalize_vendor(vendor)
        or product_hints.get("vendor")
        or _canonicalize_vendor(product_norm)
        or product_norm
    )

    homepage = _choose_homepage(product_key, url)
    category = product_hints.get("category") or _choose_category(product_key)

    identifiers: Dict[str, Any] = {}
    if sha1:
        identifiers["sha1"] = sha1

    return EntityResolutionResult(
        vendor=resolved_vendor,
        product=product_norm,
        homepage=homepage,
        category=category,
        identifiers=identifiers,
    )