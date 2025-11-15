# withsecure-assessor

## Overview
The WithSecure Assessor is a tool designed to provide a deterministic, source-backed assessment of software products, focusing on entity resolution, citation quality, and risk scoring. It aims to assist security professionals in evaluating the security posture of various tools and services.

## Features
- **Entity Resolution**: Robust resolver for identifying vendors and products based on various inputs.
- **High-Quality Citations**: Strict claim-evidence schema with verbatim excerpts, URLs, and timestamps.
- **Risk Scoring**: Transparent scoring system based on multiple factors, including exposure, controls, vendor posture, and compliance.
- **Alternatives Suggestion**: Provides safer alternatives based on assessment results.
- **Offline Functionality**: Ability to run assessments and comparisons without an internet connection.

## Installation (Poetry)
```bash
pipx install poetry || python3 -m pip install --user poetry
poetry install
poetry lock
```

## Usage
### Command-Line Interface (Typer)
```bash
poetry run assessor version
poetry run assessor assess "PeaZip"
```

### Web Application (FastAPI)
```bash
poetry run uvicorn assessor.web.app:app --reload
```

## Testing
```bash
poetry run assessor version
poetry run assessor assess "PeaZip"
```

## Architecture
See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Scoring
See [docs/SCORING.md](docs/SCORING.md).

## Evidence schema
See [docs/EVIDENCE_SCHEMA.md](docs/EVIDENCE_SCHEMA.md).

## Snapshot spec
See [docs/SNAPSHOT_SPEC.md](docs/SNAPSHOT_SPEC.md).

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.