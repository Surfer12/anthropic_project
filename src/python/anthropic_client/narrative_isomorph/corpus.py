"""
NarrativeCorpus module for managing source narratives and their transformations.
"""

from typing import Dict, List, Any, Optional, Union
import pandas as pd
import numpy as np
import json
import os
from pathlib import Path


class NarrativeCorpus:
    """
    Manages source narratives and their transformations across different
    language model architectures.
    """
    
    def __init__(self, name: str = "default_corpus"):
        """
        Initialize a new NarrativeCorpus.
        
        Args:
            name: A descriptive name for this corpus
        """
        self.name = name
        self.source_narratives: Dict[str, Dict[str, Any]] = {}
        self.architecture_outputs: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self.metadata: Dict[str, Any] = {"version": "0.1.0", "created_at": pd.Timestamp.now().isoformat()}
    
    def add_source_narrative(self, narrative_id: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a source narrative to the corpus.
        
        Args:
            narrative_id: Unique identifier for the narrative
            text: The narrative text content
            metadata: Optional metadata about the narrative (source, genre, etc.)
        """
        if narrative_id in self.source_narratives:
            raise ValueError(f"Narrative ID '{narrative_id}' already exists in corpus")
        
        self.source_narratives[narrative_id] = {
            "text": text,
            "metadata": metadata or {},
            "added_at": pd.Timestamp.now().isoformat()
        }
    
    def add_architecture_output(self, 
                               narrative_id: str, 
                               architecture_id: str, 
                               output_text: str,
                               metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add an architecture's output for a given source narrative.
        
        Args:
            narrative_id: ID of the source narrative
            architecture_id: Identifier for the architecture (e.g., "claude-3-opus")
            output_text: The transformed narrative from the architecture
            metadata: Optional metadata about the transformation process
        """
        if narrative_id not in self.source_narratives:
            raise ValueError(f"Source narrative '{narrative_id}' not found in corpus")
        
        if narrative_id not in self.architecture_outputs:
            self.architecture_outputs[narrative_id] = {}
        
        self.architecture_outputs[narrative_id][architecture_id] = {
            "text": output_text,
            "metadata": metadata or {},
            "processed_at": pd.Timestamp.now().isoformat()
        }
    
    def get_source_narrative(self, narrative_id: str) -> str:
        """
        Get a source narrative text by ID.
        
        Args:
            narrative_id: ID of the narrative to retrieve
            
        Returns:
            The narrative text
        """
        if narrative_id not in self.source_narratives:
            raise ValueError(f"Source narrative '{narrative_id}' not found in corpus")
        
        return self.source_narratives[narrative_id]["text"]
    
    def get_architecture_output(self, narrative_id: str, architecture_id: str) -> str:
        """
        Get the output of a specific architecture for a specific narrative.
        
        Args:
            narrative_id: ID of the source narrative
            architecture_id: ID of the architecture
            
        Returns:
            The transformed narrative text
        """
        if (narrative_id not in self.architecture_outputs or 
            architecture_id not in self.architecture_outputs[narrative_id]):
            raise ValueError(
                f"No output found for narrative '{narrative_id}' and architecture '{architecture_id}'"
            )
        
        return self.architecture_outputs[narrative_id][architecture_id]["text"]
    
    def list_narratives(self) -> List[str]:
        """List all narrative IDs in the corpus."""
        return list(self.source_narratives.keys())
    
    def list_architectures(self) -> List[str]:
        """List all unique architecture IDs across all narratives."""
        architectures = set()
        for outputs in self.architecture_outputs.values():
            architectures.update(outputs.keys())
        return list(architectures)
    
    def save(self, directory: Union[str, Path]) -> None:
        """
        Save the corpus to disk.
        
        Args:
            directory: Directory where to save the corpus
        """
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        
        # Save metadata and structure
        with open(directory / f"{self.name}_metadata.json", "w") as f:
            json.dump(self.metadata, f, indent=2)
        
        # Save source narratives
        source_dir = directory / "sources"
        source_dir.mkdir(exist_ok=True)
        
        for narrative_id, narrative in self.source_narratives.items():
            with open(source_dir / f"{narrative_id}.json", "w") as f:
                json.dump(narrative, f, indent=2)
        
        # Save architecture outputs
        outputs_dir = directory / "outputs"
        outputs_dir.mkdir(exist_ok=True)
        
        for narrative_id, architectures in self.architecture_outputs.items():
            narrative_dir = outputs_dir / narrative_id
            narrative_dir.mkdir(exist_ok=True)
            
            for architecture_id, output in architectures.items():
                with open(narrative_dir / f"{architecture_id}.json", "w") as f:
                    json.dump(output, f, indent=2)
    
    @classmethod
    def load(cls, directory: Union[str, Path]) -> "NarrativeCorpus":
        """
        Load a corpus from disk.
        
        Args:
            directory: Directory containing the corpus
            
        Returns:
            The loaded NarrativeCorpus
        """
        directory = Path(directory)
        
        # Find metadata file
        metadata_files = list(directory.glob("*_metadata.json"))
        if not metadata_files:
            raise ValueError(f"No metadata file found in {directory}")
        
        with open(metadata_files[0], "r") as f:
            metadata = json.load(f)
        
        corpus_name = metadata_files[0].stem.replace("_metadata", "")
        corpus = cls(name=corpus_name)
        corpus.metadata = metadata
        
        # Load source narratives
        source_dir = directory / "sources"
        if source_dir.exists():
            for source_file in source_dir.glob("*.json"):
                with open(source_file, "r") as f:
                    narrative_data = json.load(f)
                
                narrative_id = source_file.stem
                corpus.source_narratives[narrative_id] = narrative_data
        
        # Load architecture outputs
        outputs_dir = directory / "outputs"
        if outputs_dir.exists():
            for narrative_dir in outputs_dir.iterdir():
                if narrative_dir.is_dir():
                    narrative_id = narrative_dir.name
                    corpus.architecture_outputs[narrative_id] = {}
                    
                    for output_file in narrative_dir.glob("*.json"):
                        with open(output_file, "r") as f:
                            output_data = json.load(f)
                        
                        architecture_id = output_file.stem
                        corpus.architecture_outputs[narrative_id][architecture_id] = output_data
        
        return corpus