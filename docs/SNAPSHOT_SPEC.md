# SNAPSHOT SPECIFICATION

## Overview
This document outlines the specifications for the snapshot functionality within the WithSecure Assessor project. The snapshot feature is designed to ensure reproducibility of assessments by capturing the state of data at a specific point in time.

## Purpose
The snapshot functionality allows users to freeze the current state of the data, including all fetched evidence and resolved entities, enabling consistent assessments even if the underlying data changes over time.

## Snapshot Structure
A snapshot consists of the following components:

- **Snapshot ID**: A unique identifier for the snapshot.
- **Created At**: Timestamp indicating when the snapshot was created.
- **Dependency Lock**: A record of the versions of dependencies used at the time of the snapshot.

## Data Model
The snapshot data model includes the following fields:

- `snapshot_id`: Unique identifier for the snapshot.
- `created_at`: Date and time when the snapshot was created.
- `dependency_lock`: A JSON object containing the versions of all dependencies.

## Storage
Snapshots will be stored in a JSON format within the cache database. Each snapshot will be associated with a timestamp to ensure that it can be referenced later for reproducibility.

## Usage
To create a snapshot, the following steps will be executed:

1. Capture the current state of all relevant data.
2. Generate a unique snapshot ID.
3. Record the current timestamp.
4. Lock the versions of all dependencies.
5. Store the snapshot in the cache database.

## Retrieval
Snapshots can be retrieved by their unique ID, allowing users to access the exact state of the data at the time the snapshot was created. This is crucial for audits and historical comparisons.

## Example
A typical snapshot entry in the database might look like this:

```json
{
  "snapshot_id": "snapshot_001",
  "created_at": "2023-10-01T12:00:00Z",
  "dependency_lock": {
    "package_name": "1.0.0",
    "another_package": "2.3.4"
  }
}
```

## Conclusion
The snapshot functionality is a critical component of the WithSecure Assessor project, providing users with the ability to maintain consistency in their assessments over time. By adhering to this specification, the project will ensure that snapshots are created and managed effectively.