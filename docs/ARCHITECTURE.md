# Architecture of the WithSecure Assessor

## Overview
The WithSecure Assessor is designed to deliver a deterministic, source-backed assessment of software products with a focus on entity resolution, citation quality, and risk scoring. The architecture is modular, allowing for easy maintenance and extensibility.

## Components

### 1. Resolver
The resolver is responsible for entity resolution, taking inputs such as product name, vendor, URL, and optional SHA1. It normalizes text, utilizes a curated alias table, and performs targeted web queries to resolve entities to their canonical forms.

- **Inputs**: Product name, vendor, URL, optional SHA1
- **Outputs**: {vendor, product, homepage, category, identifiers}

### 2. Fetchers
Fetchers are high-signal sources that gather data from various repositories and APIs. Each fetcher is designed to write raw content and normalized facts to a local cache.

- **Sources**:
  - NVD/CVE
  - CISA KEV JSON
  - Vendor PSIRT/security/trust center
  - Compliance documents
  - Reputable CERT/advisories

### 3. Parsers
Parsers extract relevant information from the fetched data. They are equipped with tests to ensure accuracy and reliability.

- **Key Functions**:
  - CVE timeline and severity distribution
  - Compliance claims and incident summaries
  - Labeling of evidence sources

### 4. Scoring Engine
The scoring engine calculates a transparent risk score based on various signals, including exposure, controls, vendor posture, compliance, incidents, and data handling.

- **Score Calculation**: 
  - Exposure (30%)
  - Controls (20%)
  - Vendor posture (15%)
  - Compliance (15%)
  - Incidents (10%)
  - Data handling (10%)

### 5. Summarization
The summarization module generates concise briefs for CISOs, utilizing a template-first approach to ensure clarity and consistency.

- **Output**: CISO-ready one-pager with inline citations and evidence appendix.

### 6. Alternatives
The alternatives module suggests safer product picks based on the assessment, providing a side-by-side comparison of similar tools.

### 7. Cache
The cache module implements a local database for storing fetched data, with a TTL (time-to-live) mechanism and snapshot functionality for reproducibility.

### 8. CLI and Web Interface
The command-line interface (CLI) allows users to assess one or multiple products, while the web interface provides a minimal comparison view and search functionality.

## Data Model
The data model is built around a claim-evidence structure, ensuring that all claims are backed by verifiable evidence.

- **Claim**: {id, product_id, category, text, score_contrib, confidence}
- **Evidence**: {claim_id, url, source_type, excerpt, retrieved_at, parser_id}

## Risk Management
The architecture incorporates risk management strategies to avoid common pitfalls, such as ensuring all claims are backed by citations and handling conflicting claims transparently.

## Conclusion
The WithSecure Assessor is a robust and modular architecture designed to provide high-quality assessments of software products, ensuring transparency, reliability, and ease of use.