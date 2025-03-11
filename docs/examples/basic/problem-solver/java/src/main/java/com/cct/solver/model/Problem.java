package com.cct.solver.model;

import lombok.Builder;
import lombok.Data;
import lombok.Singular;

import java.util.List;

@Data
@Builder
public class Problem {
    private String name;
    private String description;
    
    @Singular
    private List<String> constraints;
    
    @Singular("successCriterion")
    private List<String> successCriteria;
    
    @Builder.Default
    private ProblemType type = ProblemType.GENERAL;
    
    @Builder.Default
    private ProblemPriority priority = ProblemPriority.MEDIUM;
    
    public enum ProblemType {
        GENERAL,
        OPTIMIZATION,
        ANALYSIS,
        DESIGN,
        IMPLEMENTATION
    }
    
    public enum ProblemPriority {
        LOW,
        MEDIUM,
        HIGH,
        CRITICAL
    }
    
    public boolean isValid() {
        return name != null && !name.isEmpty() &&
               description != null && !description.isEmpty() &&
               constraints != null && !constraints.isEmpty() &&
               successCriteria != null && !successCriteria.isEmpty();
    }
    
    public boolean isHighPriority() {
        return priority == ProblemPriority.HIGH || 
               priority == ProblemPriority.CRITICAL;
    }
    
    public boolean requiresOptimization() {
        return type == ProblemType.OPTIMIZATION ||
               constraints.stream().anyMatch(c -> 
                   c.toLowerCase().contains("performance") ||
                   c.toLowerCase().contains("optimize") ||
                   c.toLowerCase().contains("efficiency")
               );
    }
} 