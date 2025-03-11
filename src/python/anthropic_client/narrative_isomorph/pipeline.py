"""
Pipeline modules for managing narrative analysis workflows.
"""

from typing import Dict, List, Any, Optional, Tuple, Union, Callable
import pandas as pd
import numpy as np
import logging
import json
from pathlib import Path
import time

from ..client import AnthropicClient, ModelName, OutputFormat
from .corpus import NarrativeCorpus
from .metrics import NarrativeMetrics
from .detector import IsomorphicDetector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelInteractionPipeline:
    """
    Handles interactions with various model architectures for narrative processing.
    """
    
    def __init__(self, anthropic_client: Optional[AnthropicClient] = None):
        """
        Initialize the model interaction pipeline.
        
        Args:
            anthropic_client: An AnthropicClient instance to use
        """
        self.client = anthropic_client or AnthropicClient()
        self.registered_architectures = {
            "claude-sonnet": self._process_claude_sonnet,
            "claude-haiku": self._process_claude_haiku,
            "claude-opus": self._process_claude_opus
        }
    
    def register_architecture(self, architecture_id: str, processor: Callable[[str, Dict[str, Any]], str]) -> None:
        """
        Register a new model architecture for narrative processing.
        
        Args:
            architecture_id: Unique identifier for the architecture
            processor: Function that processes a narrative, taking text and params and returning text
        """
        self.registered_architectures[architecture_id] = processor
    
    def _process_claude_sonnet(self, text: str, params: Dict[str, Any] = None) -> str:
        """Process narrative using Claude Sonnet model."""
        params = params or {}
        system = params.get("system", "You are an expert in narrative analysis.")
        prompt = params.get("prompt_template", "Transform the following narrative while preserving its core meaning: {text}").format(text=text)
        
        try:
            response = self.client.get_response(
                prompt=prompt,
                model=ModelName.SONNET,
                temperature=params.get("temperature", 0.7),
                stream=False,
                system=system
            )
            return response
        except Exception as e:
            logger.error(f"Error processing with Claude Sonnet: {str(e)}")
            return f"Error: {str(e)}"
    
    def _process_claude_haiku(self, text: str, params: Dict[str, Any] = None) -> str:
        """Process narrative using Claude Haiku model."""
        params = params or {}
        system = params.get("system", "You are an expert in narrative analysis.")
        prompt = params.get("prompt_template", "Transform the following narrative while preserving its core meaning: {text}").format(text=text)
        
        try:
            response = self.client.get_response(
                prompt=prompt,
                model=ModelName.HAIKU,
                temperature=params.get("temperature", 0.7),
                stream=False,
                system=system
            )
            return response
        except Exception as e:
            logger.error(f"Error processing with Claude Haiku: {str(e)}")
            return f"Error: {str(e)}"
    
    def _process_claude_opus(self, text: str, params: Dict[str, Any] = None) -> str:
        """Process narrative using Claude Opus model."""
        params = params or {}
        system = params.get("system", "You are an expert in narrative analysis.")
        prompt = params.get("prompt_template", "Transform the following narrative while preserving its core meaning: {text}").format(text=text)
        
        try:
            response = self.client.get_response(
                prompt=prompt,
                model=ModelName.OPUS,
                temperature=params.get("temperature", 0.7),
                stream=False,
                system=system
            )
            return response
        except Exception as e:
            logger.error(f"Error processing with Claude Opus: {str(e)}")
            return f"Error: {str(e)}"
    
    def process_narrative(self, narrative_text: str, architecture_id: str, params: Dict[str, Any] = None) -> str:
        """
        Process a narrative using a specific architecture.
        
        Args:
            narrative_text: The narrative text to process
            architecture_id: Identifier for the architecture to use
            params: Additional parameters for the processor
            
        Returns:
            Processed narrative text
            
        Raises:
            ValueError: If architecture_id is not registered
        """
        if architecture_id not in self.registered_architectures:
            raise ValueError(f"Architecture '{architecture_id}' not registered")
        
        processor = self.registered_architectures[architecture_id]
        
        # Apply rate limiting if specified
        rate_limit = params.get("rate_limit_seconds", 0) if params else 0
        if rate_limit > 0:
            logger.info(f"Rate limiting: sleeping for {rate_limit} seconds")
            time.sleep(rate_limit)
        
        return processor(narrative_text, params)
    
    def process_batch(self, corpus: NarrativeCorpus, 
                     architecture_ids: List[str], 
                     params: Dict[str, Any] = None) -> Dict[str, Dict[str, str]]:
        """
        Process multiple narratives with multiple architectures.
        
        Args:
            corpus: NarrativeCorpus containing source narratives
            architecture_ids: List of architecture IDs to use
            params: Additional parameters for processors
            
        Returns:
            Dictionary mapping narrative_id -> architecture_id -> processed_text
        """
        results = {}
        params = params or {}
        
        for narrative_id in corpus.list_narratives():
            source_narrative = corpus.get_source_narrative(narrative_id)
            results[narrative_id] = {}
            
            for architecture_id in architecture_ids:
                logger.info(f"Processing narrative '{narrative_id}' with architecture '{architecture_id}'")
                
                # Get architecture-specific parameters
                arch_params = params.get(architecture_id, {})
                
                # Process the narrative
                processed_text = self.process_narrative(source_narrative, architecture_id, arch_params)
                
                # Store the result
                results[narrative_id][architecture_id] = processed_text
                
                # Add to corpus
                corpus.add_architecture_output(
                    narrative_id=narrative_id,
                    architecture_id=architecture_id,
                    output_text=processed_text,
                    metadata={"params": arch_params}
                )
        
        return results


class NarrativeAnalysisPipeline:
    """
    Coordinates the full analysis workflow for narratives across architectures.
    """
    
    def __init__(self, 
                corpus: Optional[NarrativeCorpus] = None,
                interaction_pipeline: Optional[ModelInteractionPipeline] = None,
                metrics: Optional[NarrativeMetrics] = None,
                detector: Optional[IsomorphicDetector] = None):
        """
        Initialize the narrative analysis pipeline.
        
        Args:
            corpus: NarrativeCorpus to use (created if None)
            interaction_pipeline: ModelInteractionPipeline to use (created if None)
            metrics: NarrativeMetrics to use (created if None)
            detector: IsomorphicDetector to use (created if None)
        """
        self.corpus = corpus or NarrativeCorpus()
        self.interaction_pipeline = interaction_pipeline or ModelInteractionPipeline()
        self.metrics = metrics or NarrativeMetrics()
        self.detector = detector or IsomorphicDetector()
        self.results: Dict[str, Dict[str, Dict[str, Any]]] = {}
    
    def add_source_narratives(self, narratives: Dict[str, str]) -> None:
        """
        Add multiple source narratives to the corpus.
        
        Args:
            narratives: Dictionary mapping narrative_id -> narrative_text
        """
        for narrative_id, text in narratives.items():
            self.corpus.add_source_narrative(narrative_id, text)
    
    def process_with_architectures(self, architecture_ids: List[str], params: Dict[str, Any] = None) -> None:
        """
        Process all source narratives with the specified architectures.
        
        Args:
            architecture_ids: List of architecture IDs to use
            params: Additional parameters for processors
        """
        self.interaction_pipeline.process_batch(self.corpus, architecture_ids, params)
    
    def analyze_corpus(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Analyze all narrative pairs in the corpus.
        
        Returns:
            Dictionary of analysis results
        """
        results = {}
        
        for narrative_id in self.corpus.list_narratives():
            source_text = self.corpus.get_source_narrative(narrative_id)
            results[narrative_id] = {}
            
            for architecture_id in self.corpus.architecture_outputs.get(narrative_id, {}):
                transformed_text = self.corpus.get_architecture_output(narrative_id, architecture_id)
                
                # Run metrics analysis
                metrics_results = self.metrics.analyze_narrative_pair(source_text, transformed_text)
                
                # Run isomorphism detection
                isomorphism_results = self.detector.detect_isomorphism(source_text, transformed_text)
                
                # Combine results
                combined_results = {
                    "metrics": metrics_results,
                    "isomorphism": isomorphism_results
                }
                
                results[narrative_id][architecture_id] = combined_results
        
        self.results = results
        return results
    
    def analyze_frameworks(self, frameworks: Dict[str, str]) -> Dict[str, Dict[str, Dict[str, float]]]:
        """
        Analyze all narratives against provided frameworks.
        
        Args:
            frameworks: Dictionary mapping framework_name -> framework_description
            
        Returns:
            Dictionary mapping narrative_id -> architecture_id -> framework_results
        """
        framework_results = {}
        
        for narrative_id in self.corpus.list_narratives():
            source_text = self.corpus.get_source_narrative(narrative_id)
            framework_results[narrative_id] = {}
            
            # Analyze source narrative
            source_framework_scores = self.detector.detect_narrative_framework(source_text, frameworks)
            framework_results[narrative_id]["source"] = source_framework_scores
            
            # Analyze transformed narratives
            for architecture_id in self.corpus.architecture_outputs.get(narrative_id, {}):
                transformed_text = self.corpus.get_architecture_output(narrative_id, architecture_id)
                
                # Analyze against frameworks
                transformed_framework_scores = self.detector.detect_narrative_framework(transformed_text, frameworks)
                framework_results[narrative_id][architecture_id] = transformed_framework_scores
        
        return framework_results
    
    def generate_report(self, output_dir: Union[str, Path] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive analysis report.
        
        Args:
            output_dir: Optional directory to save the report
            
        Returns:
            Dictionary containing the full report
        """
        if not self.results:
            self.analyze_corpus()
        
        # Generate report data
        report = {
            "corpus_summary": {
                "narrative_count": len(self.corpus.list_narratives()),
                "architecture_count": len(self.corpus.list_architectures()),
                "total_transformations": sum(
                    len(outputs) for outputs in self.corpus.architecture_outputs.values()
                )
            },
            "narratives": {},
            "architectures": {},
            "cross_architecture_analysis": {}
        }
        
        # Narrative-specific results
        for narrative_id in self.corpus.list_narratives():
            narrative_results = {
                "source_length": len(self.corpus.get_source_narrative(narrative_id)),
                "architecture_results": {},
                "best_preservation": {"architecture": None, "score": 0},
                "worst_preservation": {"architecture": None, "score": 1}
            }
            
            for architecture_id in self.results.get(narrative_id, {}):
                arch_results = self.results[narrative_id][architecture_id]
                
                # Extract key metrics
                semantic_preservation = arch_results["metrics"]["semantic_preservation"]
                structural_preservation = arch_results["metrics"]["structural_preservation"]
                isomorphism_score = arch_results["isomorphism"]["isomorphism_score"]
                
                # Store in narrative results
                narrative_results["architecture_results"][architecture_id] = {
                    "semantic_preservation": semantic_preservation,
                    "structural_preservation": structural_preservation,
                    "isomorphism_score": isomorphism_score,
                    "info_content_delta": arch_results["metrics"]["information_delta"],
                    "invitation_delta": arch_results["metrics"]["invitation_delta"]
                }
                
                # Update best/worst preservation
                combined_preservation = (semantic_preservation + structural_preservation) / 2
                if combined_preservation > narrative_results["best_preservation"]["score"]:
                    narrative_results["best_preservation"] = {
                        "architecture": architecture_id,
                        "score": combined_preservation
                    }
                
                if combined_preservation < narrative_results["worst_preservation"]["score"]:
                    narrative_results["worst_preservation"] = {
                        "architecture": architecture_id,
                        "score": combined_preservation
                    }
            
            report["narratives"][narrative_id] = narrative_results
        
        # Architecture-specific results
        for architecture_id in self.corpus.list_architectures():
            arch_metrics = {
                "avg_semantic_preservation": 0,
                "avg_structural_preservation": 0,
                "avg_isomorphism_score": 0,
                "avg_info_content_delta": 0,
                "avg_invitation_delta": 0,
                "transformation_count": 0
            }
            
            # Collect metrics across narratives
            for narrative_id, architecture_results in self.results.items():
                if architecture_id in architecture_results:
                    arch_metrics["avg_semantic_preservation"] += architecture_results[architecture_id]["metrics"]["semantic_preservation"]
                    arch_metrics["avg_structural_preservation"] += architecture_results[architecture_id]["metrics"]["structural_preservation"]
                    arch_metrics["avg_isomorphism_score"] += architecture_results[architecture_id]["isomorphism"]["isomorphism_score"]
                    arch_metrics["avg_info_content_delta"] += architecture_results[architecture_id]["metrics"]["information_delta"]
                    arch_metrics["avg_invitation_delta"] += architecture_results[architecture_id]["metrics"]["invitation_delta"]
                    arch_metrics["transformation_count"] += 1
            
            # Calculate averages
            if arch_metrics["transformation_count"] > 0:
                for key in ["avg_semantic_preservation", "avg_structural_preservation", 
                           "avg_isomorphism_score", "avg_info_content_delta", "avg_invitation_delta"]:
                    arch_metrics[key] /= arch_metrics["transformation_count"]
            
            report["architectures"][architecture_id] = arch_metrics
        
        # Save report if output_dir is provided
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            with open(output_dir / "narrative_analysis_report.json", "w") as f:
                json.dump(report, f, indent=2)
        
        return report
    
    def save(self, directory: Union[str, Path]) -> None:
        """
        Save the pipeline state, including corpus and results.
        
        Args:
            directory: Directory where to save
        """
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        
        # Save corpus
        corpus_dir = directory / "corpus"
        self.corpus.save(corpus_dir)
        
        # Save results
        with open(directory / "analysis_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
    
    @classmethod
    def load(cls, directory: Union[str, Path]) -> "NarrativeAnalysisPipeline":
        """
        Load a pipeline from a saved state.
        
        Args:
            directory: Directory containing saved pipeline
            
        Returns:
            Loaded NarrativeAnalysisPipeline
        """
        directory = Path(directory)
        
        # Load corpus
        corpus_dir = directory / "corpus"
        corpus = NarrativeCorpus.load(corpus_dir)
        
        # Create pipeline
        pipeline = cls(corpus=corpus)
        
        # Load results if available
        results_file = directory / "analysis_results.json"
        if results_file.exists():
            with open(results_file, "r") as f:
                pipeline.results = json.load(f)
        
        return pipeline