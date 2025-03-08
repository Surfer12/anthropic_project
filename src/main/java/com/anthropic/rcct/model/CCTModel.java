package com.anthropic.rcct.model;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents a Cognitive Chain of Thought (CCT) model in the system.
 * 
 * This entity serves as a container for a collection of related thoughts that form
 * a cognitive chain or tree structure. Each CCT model can contain multiple thought nodes
 * that are processed recursively to generate insights or visualizations.
 * 
 * The model is used in recursive thought processing, connection evaluation, 
 * and metacognitive analysis operations within the application.
 */
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class CCTModel {
    /**
     * Unique identifier for the CCT model.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    /**
     * The name of the CCT model.
     */
    private String name;
    
    /**
     * A detailed description of the CCT model and its purpose.
     */
    private String description;
    
    /**
     * Collection of thought nodes that make up this CCT model.
     * Configured with cascade to ensure proper management of child entities.
     */
    @OneToMany(cascade = CascadeType.ALL)
    private List<ThoughtNode> thoughts = new ArrayList<>();
    
    /**
     * Additional metadata about the CCT model, stored as a string.
     * This may include serialized JSON or other structured data.
     */
    private String metadata;
}