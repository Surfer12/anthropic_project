#!/bin/bash
set -e

echo "Building RCCT project with Magic toolchain..."

# Check if Magic is installed
if ! command -v max &> /dev/null; then
    echo "Magic toolchain not found. Please install it from https://modular.com/max"
    exit 1
fi

# Build the Java application
./gradlew build

# Build the Mojo components
cd anthropic_client_mojo
max run mojo build client.mojo -o bin/claudethink
max run mojo build cli.mojo -o bin/claudethink_cli

echo "Building Docker container..."
docker build -t rcct:latest .

echo "Build complete. Run with: docker-compose up" 