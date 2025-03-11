"""
NarrativeIsomorph: A computational framework for analyzing narrative transformations
across different language model architectures.
"""

from .corpus import NarrativeCorpus
from .metrics import NarrativeMetrics
from .detector import IsomorphicDetector
from .pipeline import ModelInteractionPipeline, NarrativeAnalysisPipeline
from .visualizer import NarrativeVisualizer

__version__ = "0.1.0"
__all__ = [
    "NarrativeCorpus",
    "NarrativeMetrics",
    "IsomorphicDetector",
    "ModelInteractionPipeline",
    "NarrativeAnalysisPipeline",
    "NarrativeVisualizer"
]