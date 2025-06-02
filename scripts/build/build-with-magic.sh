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

# Building the Mojo components with more verbose output
cd src/mojo/anthropic_client_mojo

echo "===== Building client.mojo ====="
magic run mojo build --verbose src/client/client.mojo -o bin/claudethink || {
    echo "Client build failed. Attempting simplified build..."
    
    # Try to build a minimal version to isolate the issue
    echo "import os" > minimal.mojo
    echo "from python import Python" >> minimal.mojo
    echo "fn main() raises:" >> minimal.mojo
    echo "    var py = Python.import_module(\"anthropic\")" >> minimal.mojo
    echo "    print(\"Python module loaded\")" >> minimal.mojo
    
    magic run mojo build minimal.mojo -o bin/minimal
    echo "Minimal build result: $?"
}

echo "===== Building cli.mojo ====="
magic run mojo build --verbose src/cli/cli.mojo -o bin/claudethink_cli || echo "CLI build failed"

echo "===== Building simplified client ====="
magic run mojo build --verbose simple_client.mojo -o bin/simple_client || echo "Simplified client build failed"

# If simplified client built successfully, copy it to main output
if [ -f "bin/simple_client" ]; then
    echo "Using simplified client as fallback..."
    cp bin/simple_client bin/claudethink
    chmod +x bin/claudethink
fi

echo "Build process complete!" 