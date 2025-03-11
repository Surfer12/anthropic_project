package com.cct.solver.model;

import lombok.Builder;
import lombok.Data;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Data
@Builder
public class Solution {
    @Builder.Default
    private final String id = UUID.randomUUID().toString();
    
    private final String type;
    private final List<String> steps;
    private final Map<String, String> parameters;
    private final double confidence;
    
    public Map<String, Object> toMap() {
        return Map.of(
            "id", id,
            "type", type,
            "steps", steps,
            "parameters", parameters,
            "confidence", confidence
        );
    }
    
    public boolean isHighConfidence() {
        return confidence >= 0.8;
    }
    
    public boolean requiresValidation() {
        return confidence < 0.95;
    }
    
    public static class SolutionBuilder {
        private String type = "unknown";
        private List<String> steps = List.of();
        private Map<String, String> parameters = Map.of();
        private double confidence = 0.0;
    }
} 