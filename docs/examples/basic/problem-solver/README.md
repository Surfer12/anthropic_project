# Problem Solver Example

## Overview

This example demonstrates how to use thought chains, patterns, and domains together to create a simple problem-solving system. The system will:
1. Break down a problem into components
2. Analyze each component
3. Generate and evaluate solutions
4. Select and implement the best solution

## Project Structure

```
problem-solver/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── thought_manager.py
│   ├── pattern_analyzer.py
│   ├── domain_processor.py
│   └── solver.py
└── tests/
    ├── __init__.py
    ├── test_thought_manager.py
    ├── test_pattern_analyzer.py
    ├── test_domain_processor.py
    └── test_solver.py
```

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage Example

```python
from src.solver import ProblemSolver

# Create solver
solver = ProblemSolver()

# Define problem
problem = {
    "name": "Optimize Data Processing",
    "description": "Need to improve data processing pipeline performance",
    "constraints": ["memory < 1GB", "latency < 100ms"],
    "success_criteria": ["30% performance improvement"]
}

# Solve problem
solution = solver.solve(problem)

# Apply solution
result = solver.apply_solution(solution)
```

## Implementation Details

### 1. Thought Management (`thought_manager.py`)

```python
from cct_framework import ThoughtChain, Thought

class ThoughtManager:
    def __init__(self):
        self.chain = ThoughtChain("Problem Analysis")
        
    def analyze_problem(self, problem):
        """Break down problem into thought components."""
        # Create root thought
        root = self.chain.add_thought(
            Thought("Problem",
                   content=problem["description"])
        )
        
        # Add components
        for constraint in problem["constraints"]:
            self.chain.add_thought(
                Thought("Constraint",
                       content=constraint),
                parent=root
            )
            
        # Add success criteria
        for criterion in problem["success_criteria"]:
            self.chain.add_thought(
                Thought("Success Criterion",
                       content=criterion),
                parent=root
            )
            
        return self.chain
```

### 2. Pattern Analysis (`pattern_analyzer.py`)

```python
from cct_framework.patterns import (
    StructuralPattern,
    BehavioralPattern,
    PatternMatcher
)

class PatternAnalyzer:
    def __init__(self):
        self.matcher = PatternMatcher()
        self._init_patterns()
        
    def _init_patterns(self):
        """Initialize common patterns."""
        # Problem breakdown pattern
        self.problem_pattern = StructuralPattern(
            name="Problem Structure",
            structure=[
                {"type": "problem"},
                {"type": "constraint", "repeat": "1+"},
                {"type": "success_criterion", "repeat": "1+"}
            ]
        )
        
        # Solution approach pattern
        self.solution_pattern = BehavioralPattern(
            name="Solution Approach",
            steps=[
                "analyze_constraints",
                "generate_solutions",
                "evaluate_solutions",
                "select_solution"
            ]
        )
        
        # Register patterns
        self.matcher.add_pattern(self.problem_pattern)
        self.matcher.add_pattern(self.solution_pattern)
        
    def analyze_chain(self, chain):
        """Find patterns in thought chain."""
        return self.matcher.find_matches(chain)
```

### 3. Domain Processing (`domain_processor.py`)

```python
from cct_framework.domains import Domain, DomainConnector

class DomainProcessor:
    def __init__(self):
        self._init_domains()
        self._init_connectors()
        
    def _init_domains(self):
        """Initialize processing domains."""
        # Analysis domain
        self.analysis_domain = Domain(
            name="Analysis",
            type="processing"
        )
        
        # Solution domain
        self.solution_domain = Domain(
            name="Solution",
            type="processing"
        )
        
        # Implementation domain
        self.implementation_domain = Domain(
            name="Implementation",
            type="processing"
        )
        
    def _init_connectors(self):
        """Initialize domain connectors."""
        # Analysis to Solution connector
        self.analysis_to_solution = DomainConnector(
            source=self.analysis_domain,
            target=self.solution_domain
        )
        
        # Solution to Implementation connector
        self.solution_to_implementation = DomainConnector(
            source=self.solution_domain,
            target=self.implementation_domain
        )
        
    def process_analysis(self, data):
        """Process data in analysis domain."""
        return self.analysis_domain.execute(
            "analyze",
            data
        )
        
    def generate_solution(self, analysis):
        """Generate solution from analysis."""
        # Transform analysis to solution domain
        solution_data = self.analysis_to_solution.translate(
            analysis
        )
        
        # Generate solution
        return self.solution_domain.execute(
            "generate",
            solution_data
        )
        
    def implement_solution(self, solution):
        """Implement the solution."""
        # Transform solution to implementation domain
        impl_data = self.solution_to_implementation.translate(
            solution
        )
        
        # Implement solution
        return self.implementation_domain.execute(
            "implement",
            impl_data
        )
```

### 4. Problem Solver (`solver.py`)

```python
from .thought_manager import ThoughtManager
from .pattern_analyzer import PatternAnalyzer
from .domain_processor import DomainProcessor

class ProblemSolver:
    def __init__(self):
        self.thought_manager = ThoughtManager()
        self.pattern_analyzer = PatternAnalyzer()
        self.domain_processor = DomainProcessor()
        
    def solve(self, problem):
        """Solve the given problem."""
        # Create thought chain
        chain = self.thought_manager.analyze_problem(problem)
        
        # Analyze patterns
        patterns = self.pattern_analyzer.analyze_chain(chain)
        
        # Process in domains
        analysis = self.domain_processor.process_analysis(
            {"chain": chain, "patterns": patterns}
        )
        
        solution = self.domain_processor.generate_solution(
            analysis
        )
        
        return solution
        
    def apply_solution(self, solution):
        """Apply the solution."""
        return self.domain_processor.implement_solution(
            solution
        )
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_solver.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Example Test (`test_solver.py`)

```python
import pytest
from src.solver import ProblemSolver

def test_problem_solving():
    # Create solver
    solver = ProblemSolver()
    
    # Test problem
    problem = {
        "name": "Test Problem",
        "description": "Simple test problem",
        "constraints": ["test constraint"],
        "success_criteria": ["test criterion"]
    }
    
    # Test solution generation
    solution = solver.solve(problem)
    assert solution is not None
    
    # Test solution application
    result = solver.apply_solution(solution)
    assert result["success"] == True
```

## Next Steps

1. Add more complex problem types
2. Implement additional patterns
3. Extend domain capabilities
4. Add visualization tools

## Related Documentation

- [Thought Chains Guide](../../user-guides/basic/thought-chains.md)
- [Basic Patterns Guide](../../user-guides/basic/basic-patterns.md)
- [Domain Basics Guide](../../user-guides/basic/domain-basics.md) 