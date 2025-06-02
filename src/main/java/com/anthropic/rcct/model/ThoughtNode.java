package com.anthropic.rcct.model;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents a single thought or node within a Cognitive Chain of Thought (CCT) model.
 * 
 * Each ThoughtNode contains content representing an individual thought, along with metadata
 * that describes its type, depth in the thought hierarchy, parent relationships, and other
 * properties. ThoughtNodes can form tree structures or complex graphs that represent
 * cognitive processes or reasoning chains.
 * 
 * ThoughtNodes are processed by the ThoughtProcessingService for recursive analysis,
 * connection evaluation, and meta-cognitive operations.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ThoughtNode {
    /**
     * Unique identifier for the thought node.
     */
    private Long id;
    
    /**
     * The textual content of this thought
     */
    private String content;
    
    /**
     * The type of thought (e.g., "analysis", "reflection", "observation")
     */
    private String type;
    
    /**
     * The depth level of this thought in the hierarchy (0 = root)
     */
    private Integer depth;
    
    /**
     * The ID of the parent thought node, or null if this is a root thought
     */
    private Long parentId;
    
    /**
     * Aliases a reference to another node (similar to YAML anchors)
     */
    private ThoughtNode aliasNode;
    
    /**
     * Child thoughts that are part of this thought
     */
    @Builder.Default
    private List<ThoughtNode> subThoughts = new ArrayList<>();
    
    /**
     * Cached result for memoization
     */
    private String cachedInsight;
    
    /**
     * Attentional focus weighting for this thought (0.0 to 1.0)
     */
    private Double attentionalWeight;
    
    /**
     * Estimated complexity of this thought node (0.0 to 1.0)
     */
    private Double complexity;
    
    /**
     * Last time this thought was processed
     */
    private Long lastProcessedTimestamp;
    
    /**
     * Count of how many times this thought has been processed
     */
    @Builder.Default
    private Integer processingCount = 0;
}