import json
import typer

from assessor.resolver.resolver import resolve_entity

app = typer.Typer(help="WithSecure Assessor CLI")


@app.command()
def assess(
    entity: str = typer.Argument(..., help="Product or service name to assess."),
    vendor: str = typer.Option(None, "--vendor", help="Declared or suspected vendor name."),
    url: str = typer.Option(None, "--url", help="Homepage or documentation URL."),
    sha1: str = typer.Option(None, "--sha1", help="Optional SHA-1 hash identifier."),
    offline: bool = typer.Option(False, "--offline/--online", help="Force offline mode (cache only)."),
    snapshot: str = typer.Option(None, "--snapshot", help="Snapshot timestamp or ID for deterministic reads."),
):
    _ = offline  # placeholder until cache lands
    _ = snapshot

    result = resolve_entity(entity, vendor, url, sha1)
    if not result:
        typer.secho("Unable to resolve entity with provided inputs.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    typer.echo(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))


@app.command()
def version():
    typer.echo("withsecure-assessor 0.1.0")


if __name__ == "__main__":
    app()