#!/bin/bash

# This script packages the necessary files for an offline demo of the WithSecure Assessor.

# Define the output directory for the demo pack
OUTPUT_DIR="./offline_demo_pack"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Copy the necessary files to the output directory
cp -r ../src/assessor "$OUTPUT_DIR/src"
cp -r ../tests/fixtures "$OUTPUT_DIR/tests"
cp ../README.md "$OUTPUT_DIR"
cp ../LICENSE "$OUTPUT_DIR"

# Create a README for the offline demo pack
cat <<EOL > "$OUTPUT_DIR/README.md"
# Offline Demo Pack for WithSecure Assessor

This directory contains the necessary files for running an offline demo of the WithSecure Assessor.

## Contents

- **src/assessor**: The source code for the assessor.
- **tests/fixtures**: Sample data for testing.
- **README.md**: This file.
- **LICENSE**: License information.

## Usage

To run the demo, navigate to the src/assessor directory and execute the appropriate scripts.
EOL

echo "Offline demo pack created at $OUTPUT_DIR"