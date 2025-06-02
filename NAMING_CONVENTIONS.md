# File Naming Conventions: Fractal/Multi-Scale Approach

## Overview
This document outlines the systematic naming conventions implemented across the anthropic_project repository using a fractal/multi-scale approach.

## Naming Principles

### Micro Level (Individual Files)
- **No spaces**: Use CamelCase or kebab-case
- **No special characters**: Avoid `<>`, `:`, `#`, `*`, `?`, `|`
- **Descriptive names**: Clearly indicate file purpose and content
- **Consistent extensions**: Use standard file extensions

### Meso Level (File Groups/Categories)
Files are grouped by function using consistent prefixes:

- `doc-`: Documentation files
- `config-`: Configuration files
- `analysis-`: Analysis and research documents
- `debug-`: Debugging and troubleshooting files
- `diagram-`: Visual diagrams and flowcharts
- `impl-`: Implementation guides and code examples
- `test-`: Test files and test documentation

### Macro Level (Directory Structure)
- Directory names use lowercase with hyphens
- Clear hierarchical organization
- Consistent naming across similar directories

## Renamed Files Log

### Documentation Files
- `# NarrativeIsomorph: Computational Analy.md` → `doc-NarrativeIsomorphComputationalAnalysis.md`
- `# CLI Tool Examples and Test Cases.md` → `doc-CLIToolExamplesAndTestCases.md`
- `Recursive Intention Modeling for Spravato Therapeutic.md` → `doc-RecursiveIntentionModelingSpravato.md`
- `*Run Tests:** Execute both the Python CL.md` → `doc-PythonTestingInstructions.md`
- `Cognitive Chamelon.md` → `doc-CognitiveChameleon.md`

### Analysis Files
- `2<structured_analysis>.xml` → `analysis-StructuredCognitiveAnalysis.xml`
- `<structured_analysis>` → `analysis-StructuredCognitive`

### Debug Files
- `Build Failure Debug Plan:.yaml.yml` → `debug-BuildFailurePlan.yaml`

### Code Files
- `from agents import Agent, Runner` → `AgentRunnerExample.py`

### Implementation Guides
- `Java implementation for analyzing isomorphic structures across model architectures.md` → `impl-JavaIsomorphicStructureAnalysis.md`

### Diagrams
- `Platform Integrations and Fallback Logic.png` → `diagram-PlatformIntegrationsAndFallbackLogic.png`
- `Unified Model Registry Workflow.png` → `diagram-UnifiedModelRegistryWorkflow.png`

### Directory Corrections
- `integrateation/` → `integration/`

## Benefits of This Approach

1. **Enhanced Searchability**: Files can be easily found by category or content
2. **Consistent Organization**: Related files follow similar naming patterns
3. **Cross-Platform Compatibility**: No problematic characters that cause issues
4. **Scalable Structure**: New files can easily fit into existing categories
5. **Clear Purpose**: File names immediately indicate their function and content

## Implementation Notes

- All renames preserve file content and functionality
- No references to old filenames were found that required updating
- The fractal approach ensures consistency at multiple organizational levels
- Future files should follow these established conventions