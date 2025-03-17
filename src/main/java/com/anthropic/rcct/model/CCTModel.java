package com.anthropic.rcct.model;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

/**
 * The Cognitive Chain of Thought (CCT) model implements a cross-domain integration
 * between computational, cognitive, and representational systems. This model manages
 * a collection of ThoughtNodes, their relationships, and evaluation strategies.
 */
public class CCTModel {
    
    /**
     * Unique identifier for this model
     */
    private Long id;
    
    /**
     * The name of the CCT model
     */
    private String name;
    
    /**
     * Description of this model's purpose
     */
    private String description;
    
    /**
     * Collection of thought nodes managed by this model
     */
    private List<ThoughtNode> thoughts = new ArrayList<>();
    
    /**
     * Memoization cache for storing computed results to save computational resources
     */
    private Map<Long, String> memoizationCache = new ConcurrentHashMap<>();
    
    /**
     * Additional metadata and contextual information about the model
     */
    private Map<String, Object> metadata = new HashMap<>();
    
    /**
     * Adds a thought node to the model
     */
    public void addThought(ThoughtNode thought) {
        thoughts.add(thought);
    }
    
    /**
     * Returns a list of all root thought nodes (nodes with no parent)
     */
    public List<ThoughtNode> getRootThoughtNodes() {
        return thoughts.stream()
                .filter(node -> node.getParentId() == null)
                .collect(Collectors.toList());
    }
    
    /**
     * Returns a list of child thought nodes for a given parent ID
     */
    public List<ThoughtNode> getChildThoughtNodes(Long parentId) {
        return thoughts.stream()
                .filter(node -> parentId.equals(node.getParentId()))
                .collect(Collectors.toList());
    }
    
    /**
     * Finds a thought node by its ID
     */
    public ThoughtNode findThoughtById(Long id) {
        return thoughts.stream()
                .filter(node -> id.equals(node.getId()))
                .findFirst()
                .orElse(null);
    }
    
    /**
     * Clear the memoization cache to force re-evaluation of thoughts
     */
    public void clearMemoizationCache() {
        memoizationCache.clear();
    }
    
    /**
     * Updates the memoization cache for a specific thought
     */
    public void updateMemoizationCache(Long thoughtId, String result) {
        memoizationCache.put(thoughtId, result);
    }
    
    /**
     * Calculates the estimated complexity of a thought node and its subtree
     */
    public double calculateNodeComplexity(ThoughtNode node) {
        // Base complexity based on content size
        double baseComplexity = Math.min(1.0, node.getContent().length() / 1000.0);
        
        // Add complexity for having many child nodes
        List<ThoughtNode> children = getChildThoughtNodes(node.getId());
        double childComplexity = Math.min(0.5, children.size() * 0.1);
        
        // Add complexity for depth
        double depthComplexity = Math.min(0.3, (node.getDepth() == null ? 0 : node.getDepth()) * 0.05);
        
        return Math.min(1.0, baseComplexity + childComplexity + depthComplexity);
    }
    
    // Getters and setters
    
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public List<ThoughtNode> getThoughts() {
        return thoughts;
    }
    
    public void setThoughts(List<ThoughtNode> thoughts) {
        this.thoughts = thoughts;
    }
    
    public Map<Long, String> getMemoizationCache() {
        return memoizationCache;
    }
    
    public void setMemoizationCache(Map<Long, String> memoizationCache) {
        this.memoizationCache = memoizationCache;
    }
    
    public Map<String, Object> getMetadata() {
        return metadata;
    }
    
    public void setMetadata(Map<String, Object> metadata) {
        this.metadata = metadata;
    }
}