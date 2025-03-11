"""
IsomorphicDetector module for identifying structural isomorphisms in narratives.
"""

from typing import Dict, List, Any, Optional, Tuple, Union
import numpy as np
import networkx as nx
from sentence_transformers import SentenceTransformer
import nltk
from nltk.tokenize import sent_tokenize
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IsomorphicDetector:
    """
    Identifies structural isomorphisms (shared patterns) between narratives
    across different architectures.
    """
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2", threshold: float = 0.7):
        """
        Initialize the isomorphic detector.
        
        Args:
            embedding_model: Model to use for semantic embeddings
            threshold: Similarity threshold for connecting nodes in the graph (0-1)
        """
        self.embedding_model = SentenceTransformer(embedding_model)
        self.threshold = threshold
    
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
    
    def _build_narrative_graph(self, text: str) -> nx.Graph:
        """
        Build a graph representation of a narrative, where nodes are sentences
        and edges represent semantic similarity above threshold.
        
        Args:
            text: The narrative text
            
        Returns:
            NetworkX graph representation
        """
        # Segment text into sentences
        sentences = self._segment_text(text)
        
        # Handle empty text
        if len(sentences) == 0:
            return nx.Graph()
        
        # Get embeddings
        embeddings = self._get_embeddings(sentences)
        
        # Create graph
        G = nx.Graph()
        
        # Add nodes (sentences)
        for i, sentence in enumerate(sentences):
            G.add_node(i, text=sentence, embedding=embeddings[i])
        
        # Add edges based on semantic similarity
        for i in range(len(sentences)):
            for j in range(i+1, len(sentences)):
                # Calculate cosine similarity
                similarity = np.dot(embeddings[i], embeddings[j]) / (np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j]))
                
                # Add edge if similarity is above threshold
                if similarity >= self.threshold:
                    G.add_edge(i, j, weight=float(similarity))
        
        return G
    
    def detect_isomorphism(self, source_text: str, transformed_text: str) -> Dict[str, Any]:
        """
        Detect isomorphic structures between source and transformed narratives.
        
        Args:
            source_text: Original narrative text
            transformed_text: Transformed narrative text
            
        Returns:
            Dictionary with isomorphism analysis results
        """
        # Build graphs for both texts
        source_graph = self._build_narrative_graph(source_text)
        transformed_graph = self._build_narrative_graph(transformed_text)
        
        # Extract graph features for comparison
        source_features = {
            "node_count": source_graph.number_of_nodes(),
            "edge_count": source_graph.number_of_edges(),
            "density": nx.density(source_graph) if source_graph.number_of_nodes() > 1 else 0,
            "components": nx.number_connected_components(source_graph),
            "avg_clustering": nx.average_clustering(source_graph) if source_graph.number_of_nodes() > 0 else 0,
        }
        
        transformed_features = {
            "node_count": transformed_graph.number_of_nodes(),
            "edge_count": transformed_graph.number_of_edges(),
            "density": nx.density(transformed_graph) if transformed_graph.number_of_nodes() > 1 else 0,
            "components": nx.number_connected_components(transformed_graph),
            "avg_clustering": nx.average_clustering(transformed_graph) if transformed_graph.number_of_nodes() > 0 else 0,
        }
        
        # Calculate structural similarity score
        # This is a simple heuristic - a more sophisticated approach would use graph matching algorithms
        if source_features["node_count"] > 0 and transformed_features["node_count"] > 0:
            # Normalize each feature and calculate distance
            features = ["node_count", "edge_count", "density", "components", "avg_clustering"]
            normalized_distance = 0
            
            for feature in features:
                # Handle zero division
                if source_features[feature] == 0 and transformed_features[feature] == 0:
                    feature_distance = 0
                elif source_features[feature] == 0 or transformed_features[feature] == 0:
                    feature_distance = 1
                else:
                    # Normalize by taking ratio and capping at 1
                    ratio = source_features[feature] / transformed_features[feature]
                    ratio = ratio if ratio <= 1 else 1/ratio
                    feature_distance = 1 - ratio
                
                normalized_distance += feature_distance
            
            # Average the distances
            normalized_distance /= len(features)
            
            # Convert distance to similarity (0-1)
            structural_similarity = 1 - normalized_distance
        else:
            structural_similarity = 0
        
        # Calculate approximate optimal subgraph isomorphism
        # We do this by looking at the most similar k-core subgraphs
        source_cores = {}
        transformed_cores = {}
        
        # Extract k-cores of different depths
        max_core = min(
            nx.core_number(source_graph).values() if source_graph.number_of_nodes() > 0 else [0],
            nx.core_number(transformed_graph).values() if transformed_graph.number_of_nodes() > 0 else [0]
        )
        
        isomorphic_subgraph_found = False
        max_matching_core = 0
        
        for k in range(max_core + 1):
            source_core = nx.k_core(source_graph, k=k)
            transformed_core = nx.k_core(transformed_graph, k=k)
            
            # Check if cores are potentially isomorphic (same number of nodes and edges)
            if (source_core.number_of_nodes() == transformed_core.number_of_nodes() and
                source_core.number_of_edges() == transformed_core.number_of_edges() and
                source_core.number_of_nodes() > 0):
                
                # Attempt to verify isomorphism (this is an expensive check)
                if source_core.number_of_nodes() <= 10:  # Limit check to small subgraphs to avoid performance issues
                    try:
                        # Check graph isomorphism using VF2 algorithm
                        matcher = nx.algorithms.isomorphism.GraphMatcher(source_core, transformed_core)
                        if matcher.is_isomorphic():
                            isomorphic_subgraph_found = True
                            max_matching_core = k
                    except Exception as e:
                        logger.warning(f"Error checking isomorphism: {str(e)}")
                
                # For larger graphs, we'll rely on heuristics
                elif (nx.density(source_core) == nx.density(transformed_core) and
                      sorted(nx.degree(source_core)) == sorted(nx.degree(transformed_core))):
                    isomorphic_subgraph_found = True
                    max_matching_core = k
        
        # Collect results
        results = {
            "source_graph_features": source_features,
            "transformed_graph_features": transformed_features,
            "structural_similarity_score": structural_similarity,
            "isomorphic_subgraph_found": isomorphic_subgraph_found,
            "max_matching_core": max_matching_core,
            "isomorphism_score": max_matching_core / (max_core + 0.1) if max_core > 0 else 0,
        }
        
        return results
    
    def detect_narrative_framework(self, text: str, frameworks: Dict[str, str]) -> Dict[str, float]:
        """
        Analyze a narrative for isomorphism with known narrative frameworks.
        
        Args:
            text: The narrative text to analyze
            frameworks: Dictionary of framework_name -> framework_description
            
        Returns:
            Dictionary of framework_name -> similarity_score
        """
        # Build graph for the text
        text_graph = self._build_narrative_graph(text)
        
        # Calculate graph features
        text_features = {
            "node_count": text_graph.number_of_nodes(),
            "edge_count": text_graph.number_of_edges(),
            "density": nx.density(text_graph) if text_graph.number_of_nodes() > 1 else 0,
            "components": nx.number_connected_components(text_graph),
            "avg_clustering": nx.average_clustering(text_graph) if text_graph.number_of_nodes() > 0 else 0,
        }
        
        # Calculate embedding of the full text for semantic comparison
        full_text_embedding = np.mean(self._get_embeddings(self._segment_text(text)), axis=0) if text else np.zeros(384)
        
        # Compare with each framework
        results = {}
        
        for framework_name, framework_description in frameworks.items():
            # Build graph for the framework
            framework_graph = self._build_narrative_graph(framework_description)
            
            # Calculate graph features
            framework_features = {
                "node_count": framework_graph.number_of_nodes(),
                "edge_count": framework_graph.number_of_edges(),
                "density": nx.density(framework_graph) if framework_graph.number_of_nodes() > 1 else 0,
                "components": nx.number_connected_components(framework_graph),
                "avg_clustering": nx.average_clustering(framework_graph) if framework_graph.number_of_nodes() > 0 else 0,
            }
            
            # Calculate structural similarity (feature-based)
            if text_features["node_count"] > 0 and framework_features["node_count"] > 0:
                features = ["density", "components", "avg_clustering"]
                normalized_distance = 0
                
                for feature in features:
                    # Handle zero division
                    if text_features[feature] == 0 and framework_features[feature] == 0:
                        feature_distance = 0
                    elif text_features[feature] == 0 or framework_features[feature] == 0:
                        feature_distance = 1
                    else:
                        # Normalize by taking ratio and capping at 1
                        ratio = text_features[feature] / framework_features[feature]
                        ratio = ratio if ratio <= 1 else 1/ratio
                        feature_distance = 1 - ratio
                    
                    normalized_distance += feature_distance
                
                # Average the distances
                normalized_distance /= len(features)
                
                # Convert distance to similarity (0-1)
                structural_similarity = 1 - normalized_distance
            else:
                structural_similarity = 0
            
            # Calculate semantic similarity
            framework_embedding = np.mean(self._get_embeddings(self._segment_text(framework_description)), axis=0) if framework_description else np.zeros(384)
            
            if np.linalg.norm(full_text_embedding) * np.linalg.norm(framework_embedding) > 0:
                semantic_similarity = np.dot(full_text_embedding, framework_embedding) / (np.linalg.norm(full_text_embedding) * np.linalg.norm(framework_embedding))
            else:
                semantic_similarity = 0
            
            # Combine structural and semantic similarity
            # Weight structural similarity less since it's more approximate
            combined_score = 0.3 * structural_similarity + 0.7 * semantic_similarity
            
            results[framework_name] = float(combined_score)
        
        return results