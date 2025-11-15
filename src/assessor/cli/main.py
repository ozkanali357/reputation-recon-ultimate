# main.py
import typer

app = typer.Typer(help="WithSecure Assessor CLI")

@app.command()
def assess(entity: str):
    """
    Assess the security posture of a given entity (placeholder).
    Deterministic scaffolding for later integration.
    """
    typer.echo(f"Assessing: {entity}")
    # TODO(step 2+): integrate resolver + fetchers + scoring + summarize.

@app.command()
def version():
    typer.echo("withsecure-assessor 0.1.0")

if __name__ == "__main__":
    app()