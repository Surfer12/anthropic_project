# Narrative Isomorph

A Python package for analyzing narrative structures, detecting isomorphic patterns, and performing cross-architectural narrative analysis.

## Overview

The Narrative Isomorph package provides tools for:

1. Representing narrative structures using advanced semantic embeddings
2. Calculating isomorphism between narrative structures
3. Performing multi-scale temporal analysis
4. Statistically validating isomorphism measures
5. Analyzing ethical considerations in narrative transformations
6. Optimizing computational resources during analysis
7. Handling cross-cultural narrative schemas

## Installation

```bash
pip install -e .
```

## Usage

```python
from anthropic_client.narrative_isomorph.corpus import NarrativeCorpus
from anthropic_client.narrative_isomorph.pipeline import NarrativeAnalysisPipeline

# Create a corpus with source narratives and architecture outputs
corpus = NarrativeCorpus(
    source_narratives={"n1": "Once upon a time, a hero embarked on an epic journey."},
    architecture_outputs={("n1", "archA"): "In a land far away, a legend was born."}
)
corpus.preprocess_corpus()

# Run the analysis pipeline
pipeline = NarrativeAnalysisPipeline(corpus)
results = pipeline.run_full_analysis(frameworks={"framework1": "example"})

print(f"Isomorphism Measure: {results['isomorphism_measure']}")
print(f"Temporal Measures: {results['temporal_measures']}")
print(f"Statistical Significance: p-value={results['p_value']}, effect size={results['effect_size']}")
```

## Components

- `representation.py`: Advanced semantic representations and narrative structure encodings
- `interface.py`: Standardizes cross-architectural model interfaces
- `calculus.py`: Implements formal isomorphism calculus for comparing narrative structures
- `temporal.py`: Implements multi-scale temporal analysis
- `validation.py`: Implements statistical validation methods
- `cultural.py`: Handles cross-cultural narrative schema registration and analysis
- `optimization.py`: Optimizes computational resource usage during analysis
- `ethics.py`: Implements ethical assessments for narrative analysis
- `detector.py`: Detects structural isomorphisms in narratives
- `metrics.py`: Implements information-theoretic analysis
- `pipeline.py`: Integrates all components into a comprehensive analysis pipeline

## Testing

```bash
python -m unittest discover tests
```

## Build with MCP

```bash
mcp build
mcp test
```