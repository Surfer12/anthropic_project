package com.anthropic.rcct.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

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
@Entity
@Data
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class ThoughtNode {
    /**
     * Unique identifier for the thought node.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    /**
     * The actual content of the thought, typically text that represents
     * an idea, observation, or reasoning step.
     */
    private String content;
    
    /**
     * The type of thought, which categorizes the thought according to its
     * function or role in the cognitive process (e.g., "analysis", "reflection", 
     * "observation", "meta").
     */
    private String type;
    
    /**
     * The depth level of this thought in the hierarchy, with higher numbers
     * typically representing more detailed or deeper levels of thinking.
     */
    private Integer depth;
    
    /**
     * The ID of the parent thought node, establishing hierarchical relationships
     * between thoughts. A null value typically indicates a root-level thought.
     */
    private Long parentId;
    
    /**
     * Additional metadata about the thought node, stored as a string.
     * This may include serialized JSON or other structured data about the thought's
     * properties, context, or relationships.
     */
    private String metadata;
}