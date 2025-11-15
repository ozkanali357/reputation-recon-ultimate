from __future__ import annotations

import csv
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from rapidfuzz import fuzz, process

_ALIAS_FILE = Path(__file__).with_name("aliases.csv")

_PRODUCT_HINTS: Dict[str, Dict[str, str]] = {
    "peazip": {
        "vendor": "PeaZip",
        "category": "File archiver",
        "homepage": "https://peazip.github.io/",
    },
    "7-zip": {
        "vendor": "7-Zip",
        "category": "File archiver",
        "homepage": "https://www.7-zip.org/",
    },
    "bandizip": {
        "vendor": "Bandisoft",
        "category": "File archiver",
        "homepage": "https://www.bandisoft.com/bandizip/",
    },
}

DEFAULT_HOMEPAGE = "https://example.com/"
DEFAULT_CATEGORY = "Unknown"


class EntityResolutionResult(BaseModel):
    vendor: str
    product: str
    homepage: str
    category: str
    identifiers: Dict[str, Any] = Field(default_factory=dict)
    source: str = "resolver"


def _normalize_text(value: Optional[str]) -> str:
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKC", value).strip()
    return " ".join(normalized.split())


def _load_aliases(path: Path) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    if not path.exists():
        return mapping
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            alias = _normalize_text(row.get("alias"))
            vendor = _normalize_text(row.get("vendor"))
            if alias:
                mapping[alias.lower()] = vendor or alias
    return mapping


@lru_cache
def _alias_map() -> Dict[str, str]:
    return _load_aliases(_ALIAS_FILE)


def _canonicalize_vendor(vendor: Optional[str]) -> Optional[str]:
    if not vendor:
        return None
    normalized = _normalize_text(vendor)
    if not normalized:
        return None

    aliases = _alias_map()
    direct = aliases.get(normalized.lower())
    if direct:
        return direct

    if len(aliases) == 0:
        return normalized

    match = process.extractOne(
        normalized,
        aliases.keys(),
        scorer=fuzz.WRatio,
        score_cutoff=90,
    )
    if match:
        alias_key = match[0]
        return aliases.get(alias_key, normalized)
    return normalized


def _choose_homepage(product_key: str, provided_url: Optional[str]) -> str:
    if provided_url:
        return provided_url
    hint = _PRODUCT_HINTS.get(product_key)
    if hint and hint.get("homepage"):
        return hint["homepage"]
    return DEFAULT_HOMEPAGE


def _choose_category(product_key: str) -> str:
    hint = _PRODUCT_HINTS.get(product_key)
    if hint and hint.get("category"):
        return hint["category"]
    return DEFAULT_CATEGORY


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
    hints = _PRODUCT_HINTS.get(product_key, {})
    resolved_vendor = (
        _canonicalize_vendor(vendor)
        or hints.get("vendor")
        or _canonicalize_vendor(product_norm)
        or product_norm
    )

    homepage = _choose_homepage(product_key, url)
    category = hints.get("category") or _choose_category(product_key)

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