# Evidence Schema Documentation

This document outlines the schema for the evidence used in the WithSecure Assessor project. The evidence schema is designed to ensure that all claims made by the assessor are backed by verifiable sources, maintaining a strict claim-evidence relationship.

## Evidence Schema

### Evidence
- **id**: Unique identifier for the evidence entry.
- **claim_id**: Reference to the associated claim's unique identifier.
- **url**: The URL from which the evidence was retrieved.
- **source_type**: The type of source from which the evidence is derived (e.g., vendor, independent, registry).
- **excerpt**: A verbatim excerpt from the source that supports the claim.
- **retrieved_at**: Timestamp indicating when the evidence was retrieved.
- **parser_id**: Identifier for the parser that processed the evidence.

### Example Evidence Entry
```json
{
  "id": "evidence_001",
  "claim_id": "claim_001",
  "url": "https://example.com/security-report",
  "source_type": "vendor",
  "excerpt": "The product has no known vulnerabilities as of the last audit.",
  "retrieved_at": "2023-10-01T12:00:00Z",
  "parser_id": "parser_001"
}
```

### Notes
- All evidence must be linked to a claim to ensure traceability.
- The `source_type` helps in categorizing the reliability of the evidence.
- The `retrieved_at` field is crucial for assessing the recency of the evidence, which impacts the confidence score.

This schema is intended to facilitate robust evidence collection and citation, ensuring that the WithSecure Assessor provides accurate and trustworthy assessments.