import json as json_module
from typing import Optional
import typer

from assessor.fetchers.cisa_kev import fetch_cisa_kev_sync
from assessor.fetchers.nvd import fetch_cves_sync
from assessor.fetchers.vendor_psirt import fetch_vendor_posture_sync  # NEW
from assessor.parsers.controls import parse_controls_from_text  # NEW
from assessor.parsers.compliance import parse_compliance_from_text  # NEW
from assessor.resolver.resolver import resolve_entity
from assessor.scoring.engine import calculate_trust_score
from assessor.summarize.summarize import generate_brief
from assessor.alternatives.suggest import suggest_alternatives, generate_alternatives_brief

app = typer.Typer(help="WithSecure Assessor CLI")


@app.command()
def assess(
    entity: str,
    vendor: str = "",
    url: str = "",
    sha1: str = "",
    offline: bool = False,
    snapshot: str = "",
    json_output: bool = False,
):
    """Assess a software product or service."""
    vendor_opt = vendor if vendor else None
    url_opt = url if url else None
    sha1_opt = sha1 if sha1 else None
    snapshot_opt = snapshot if snapshot else None
    
    result = resolve_entity(entity, vendor_opt, url_opt, sha1_opt)
    if not result:
        typer.secho("Unable to resolve entity with provided inputs.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    signals = {}
    
    # Fetch CVE data
    try:
        signals["nvd_cves"] = fetch_cves_sync(result.product, offline=offline, snapshot_id=snapshot_opt)
    except Exception as exc:
        typer.secho(f"NVD fetch failed: {exc}", fg=typer.colors.YELLOW, err=True)
        signals["nvd_cves"] = []

    # Fetch CISA KEV data
    try:
        signals["cisa_kev"] = fetch_cisa_kev_sync(offline=offline, snapshot_id=snapshot_opt)
    except Exception as exc:
        typer.secho(f"CISA KEV fetch failed: {exc}", fg=typer.colors.YELLOW, err=True)
        signals["cisa_kev"] = []

    # Fetch vendor posture (NEW)
    try:
        signals["vendor_posture"] = fetch_vendor_posture_sync(
            result.homepage, result.vendor, offline=offline, snapshot_id=snapshot_opt
        )
    except Exception as exc:
        typer.secho(f"Vendor posture fetch failed: {exc}", fg=typer.colors.YELLOW, err=True)
        signals["vendor_posture"] = {}

    # Parse controls/compliance from known data (NEW)
    # In a real system, this would fetch ToS/security pages
    # For now, we use hardcoded known-good products
    signals["controls"] = _get_known_controls(result.product)
    signals["compliance"] = _get_known_compliance(result.product)

    score = calculate_trust_score(signals)
    
    # Generate alternatives
    alternatives = suggest_alternatives(
        category=result.category,
        current_product=result.product,
        current_score=score["total_score"],
        count=2
    )

    if json_output:
        payload = {
            "entity": result.dict(),
            "signals": signals,
            "score": score,
            "alternatives": alternatives,
            "context": {"offline": offline, "snapshot": snapshot_opt},
        }
        typer.echo(json_module.dumps(payload, indent=2, ensure_ascii=False))
    else:
        brief = generate_brief(result.dict(), signals, score)
        alternatives_brief = generate_alternatives_brief(alternatives)
        typer.echo(brief + "\n" + alternatives_brief)


def _get_known_controls(product_name: str) -> dict:
    """Hardcoded controls for known products (would fetch from ToS in production)"""
    known_controls = {
        "1password": {"sso_saml": True, "mfa": True, "rbac": True, "audit_logs": True, "encryption_at_rest": True},
        "slack": {"sso_saml": True, "mfa": True, "rbac": True, "audit_logs": True, "encryption_at_rest": True},
        "zoom": {"sso_saml": True, "mfa": True, "rbac": True, "audit_logs": True, "encryption_at_rest": True},
        "dropbox": {"sso_saml": True, "mfa": True, "rbac": True, "audit_logs": True, "encryption_at_rest": True},
    }
    return known_controls.get(product_name.lower(), {})


def _get_known_compliance(product_name: str) -> dict:
    """Hardcoded compliance for known products (would fetch from trust center in production)"""
    known_compliance = {
        "1password": {"soc2_type2": True, "iso_27001": True, "gdpr_dpa": True},
        "slack": {"soc2_type2": True, "iso_27001": True, "gdpr_dpa": True, "fedramp": True},
        "zoom": {"soc2_type2": True, "iso_27001": True, "gdpr_dpa": True, "fedramp": True, "hipaa": True},
        "dropbox": {"soc2_type2": True, "iso_27001": True, "gdpr_dpa": True},
    }
    return known_compliance.get(product_name.lower(), {})


@app.command()
def version():
    """Show version information."""
    typer.echo("withsecure-assessor 0.1.0")


if __name__ == "__main__":
    app()