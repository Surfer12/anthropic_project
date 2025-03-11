package com.cct.solver.model;

import lombok.Builder;
import lombok.Data;
import java.util.Map;

@Data
@Builder
public class Result {
    private final boolean success;
    private final String status;
    
    @Builder.Default
    private final Map<String, Double> metrics = Map.of();
    
    @Builder.Default
    private final String error = null;
    
    public boolean hasError() {
        return error != null;
    }
    
    public double getMetric(String name) {
        return metrics.getOrDefault(name, 0.0);
    }
    
    public boolean meetsThreshold(String metric, double threshold) {
        return getMetric(metric) >= threshold;
    }
    
    public boolean isOptimal() {
        return success && 
               metrics.values().stream()
                     .allMatch(value -> value >= 0.8);
    }
    
    public Map<String, Object> toMap() {
        return Map.of(
            "success", success,
            "status", status,
            "metrics", metrics,
            "error", error != null ? error : "none"
        );
    }
} 