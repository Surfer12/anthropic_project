#!/bin/bash
set -e

echo "Building RCCT project with Magic toolchain..."

# Check if Magic is installed
if ! command -v magic &> /dev/null; then
    echo "Magic toolchain not found. Please install it from https://docs.modular.com/magic/"
    exit 1
fi

# Build the Java application
./gradlew build

# Build the Mojo components
cd anthropic_client_mojo
magic run mojo build client.mojo -o bin/claudethink
magic run mojo build cli.mojo -o bin/claudethink_cli

echo "Building Docker container..."
docker build -t rcct:latest .

echo "Build complete. Run with: docker-compose up" 