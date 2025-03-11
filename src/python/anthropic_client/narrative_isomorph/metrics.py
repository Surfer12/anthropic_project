"""
NarrativeMetrics module for implementing information-theoretic analysis.
"""

from typing import Dict, List, Any, Optional, Tuple, Union
import numpy as np
import pandas as pd
from scipy import stats
from sentence_transformers import SentenceTransformer
import nltk
from nltk.tokenize import sent_tokenize
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure NLTK resources are available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    logger.info("Downloading NLTK punkt tokenizer")
    nltk.download('punkt')


class NarrativeMetrics:
    """
    Implements information-theoretic analysis of narratives across different architectures.
    """
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the metrics calculator.
        
        Args:
            embedding_model: Name of the sentence-transformers model to use for embeddings
        """
        self.embedding_model = SentenceTransformer(embedding_model)
    
    def _segment_text(self, text: str) -> List[str]:
        """
        Segment text into sentences.
        
        Args:
            text: The text to segment
            
        Returns:
            List of sentences
        """
        sentences = sent_tokenize(text)
        return sentences
    
    def _get_embeddings(self, sentences: List[str]) -> np.ndarray:
        """
        Get embeddings for a list of sentences.
        
        Args:
            sentences: List of sentences to embed
            
        Returns:
            Array of embeddings
        """
        embeddings = self.embedding_model.encode(sentences)
        return embeddings
    
    def semantic_preservation(self, source_text: str, transformed_text: str) -> float:
        """
        Calculate semantic preservation score between source and transformed narratives.
        
        Args:
            source_text: Original narrative text
            transformed_text: Transformed narrative text
            
        Returns:
            Semantic preservation score (0-1, higher is better preservation)
        """
        # Segment both texts
        source_sentences = self._segment_text(source_text)
        transformed_sentences = self._segment_text(transformed_text)
        
        # Get embeddings
        source_embeddings = self._get_embeddings(source_sentences)
        transformed_embeddings = self._get_embeddings(transformed_sentences)
        
        # Calculate average similarity using cosine similarity
        # We use a matching algorithm to find best matches between sentences
        similarity_matrix = np.zeros((len(source_sentences), len(transformed_sentences)))
        
        for i, s_emb in enumerate(source_embeddings):
            for j, t_emb in enumerate(transformed_embeddings):
                # Compute cosine similarity
                similarity_matrix[i, j] = np.dot(s_emb, t_emb) / (np.linalg.norm(s_emb) * np.linalg.norm(t_emb))
        
        # For each source sentence, find the most similar transformed sentence
        max_similarities = np.max(similarity_matrix, axis=1)
        
        # Average similarity across all source sentences
        semantic_preservation_score = float(np.mean(max_similarities))
        
        return semantic_preservation_score
    
    def structural_preservation(self, source_text: str, transformed_text: str) -> float:
        """
        Calculate structural preservation score between source and transformed narratives.
        
        Args:
            source_text: Original narrative text
            transformed_text: Transformed narrative text
            
        Returns:
            Structural preservation score (0-1, higher is better preservation)
        """
        # Segment both texts
        source_sentences = self._segment_text(source_text)
        transformed_sentences = self._segment_text(transformed_text)
        
        # Get embeddings
        source_embeddings = self._get_embeddings(source_sentences)
        transformed_embeddings = self._get_embeddings(transformed_sentences)
        
        # Calculate pairwise distances within each text to capture structure
        def calc_pairwise_distances(embeddings):
            n = embeddings.shape[0]
            distances = np.zeros((n, n))
            for i in range(n):
                for j in range(i+1, n):
                    dist = np.linalg.norm(embeddings[i] - embeddings[j])
                    distances[i, j] = distances[j, i] = dist
            return distances
        
        source_distances = calc_pairwise_distances(source_embeddings)
        transformed_distances = calc_pairwise_distances(transformed_embeddings)
        
        # Normalize distance matrices
        if len(source_distances) > 0 and len(transformed_distances) > 0:
            source_distances = source_distances / np.max(source_distances)
            transformed_distances = transformed_distances / np.max(transformed_distances)
            
            # Take min dimension to compare
            min_dim = min(source_distances.shape[0], transformed_distances.shape[0])
            
            # Calculate correlation between distance matrices (truncated to same size)
            if min_dim > 1:  # Need at least 2 points for correlation
                source_distances_flat = source_distances[:min_dim, :min_dim].flatten()
                transformed_distances_flat = transformed_distances[:min_dim, :min_dim].flatten()
                
                # Calculate Pearson correlation
                correlation, _ = stats.pearsonr(source_distances_flat, transformed_distances_flat)
                
                # Convert to 0-1 scale (from -1,1)
                structural_score = (correlation + 1) / 2
                return structural_score
        
        # Default return if we can't calculate
        return 0.0
    
    def information_content(self, text: str) -> float:
        """
        Calculate information content of a narrative using embedding entropy.
        
        Args:
            text: The narrative text
            
        Returns:
            Information content score
        """
        sentences = self._segment_text(text)
        
        if len(sentences) < 2:
            return 0.0
        
        # Get embeddings
        embeddings = self._get_embeddings(sentences)
        
        # Calculate pairwise distances
        n = embeddings.shape[0]
        distances = np.zeros((n, n))
        for i in range(n):
            for j in range(i+1, n):
                dist = np.linalg.norm(embeddings[i] - embeddings[j])
                distances[i, j] = distances[j, i] = dist
        
        # Use average distance as a proxy for information content
        # Higher average distance = more diverse information
        avg_distance = np.mean(distances) if n > 1 else 0
        
        # Normalize based on typical values (may need calibration)
        # Using sigmoid to get a 0-1 range
        info_content = 2 / (1 + np.exp(-avg_distance)) - 1
        
        return float(info_content)
    
    def invitation_vs_prescription(self, text: str) -> float:
        """
        Analyze text for invitation vs prescription qualities.
        
        Args:
            text: The narrative text
            
        Returns:
            Score from 0 (fully prescriptive) to 1 (fully invitational)
        """
        # This is a simplified version using keyword analysis
        # A more sophisticated version would use a trained classifier
        
        prescriptive_keywords = [
            "must", "should", "always", "never", "required", "need to", 
            "have to", "mandatory", "necessary", "essential", "critical",
            "crucial", "vital", "imperative", "required", "follow", "obey"
        ]
        
        invitational_keywords = [
            "consider", "perhaps", "maybe", "might", "could", "possibly",
            "option", "alternative", "suggestion", "idea", "exploration",
            "invitation", "explore", "discover", "investigate", "wonder"
        ]
        
        # Count occurrences
        prescription_count = 0
        invitation_count = 0
        
        for keyword in prescriptive_keywords:
            prescription_count += text.lower().count(keyword)
            
        for keyword in invitational_keywords:
            invitation_count += text.lower().count(keyword)
            
        total_count = prescription_count + invitation_count
        
        # Compute ratio, default to middle value if no keywords found
        if total_count == 0:
            return 0.5
            
        return invitation_count / total_count
    
    def analyze_narrative_pair(self, source_text: str, transformed_text: str) -> Dict[str, float]:
        """
        Perform comprehensive analysis on a pair of source and transformed narratives.
        
        Args:
            source_text: Original narrative text
            transformed_text: Transformed narrative text
            
        Returns:
            Dictionary of metrics
        """
        metrics = {
            "semantic_preservation": self.semantic_preservation(source_text, transformed_text),
            "structural_preservation": self.structural_preservation(source_text, transformed_text),
            "source_information_content": self.information_content(source_text),
            "transformed_information_content": self.information_content(transformed_text),
            "information_delta": self.information_content(transformed_text) - self.information_content(source_text),
            "source_invitation_score": self.invitation_vs_prescription(source_text),
            "transformed_invitation_score": self.invitation_vs_prescription(transformed_text),
            "invitation_delta": self.invitation_vs_prescription(transformed_text) - self.invitation_vs_prescription(source_text)
        }
        
        return metrics