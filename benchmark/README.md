# Benchmarking

This directory contains benchmarks for the Anthropic client library.

## Directory Structure

- `performance/`: Performance benchmarks for API calls and data processing
- `memory/`: Memory usage and leak detection tests
- `integration/`: End-to-end integration benchmarks

## Running Benchmarks

To run all benchmarks:

```bash
python -m pytest benchmark/
```

To run a specific category:

```bash
python -m pytest benchmark/performance/
python -m pytest benchmark/memory/
python -m pytest benchmark/integration/
```

## Adding New Benchmarks

When adding new benchmarks:

1. Create a new file in the appropriate directory
2. Use the pytest-benchmark fixture for performance tests
3. Add documentation for the benchmark
4. Include baseline results if applicable 