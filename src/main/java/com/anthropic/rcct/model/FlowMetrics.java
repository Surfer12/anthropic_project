package com.anthropic.rcct.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.Map;

/**
 * Represents the metrics related to flow state in cognitive processing.
 * Flow state metrics measure various aspects of optimal cognitive engagement,
 * including challenge-skill balance, attention focus, and cognitive load.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class FlowMetrics {
    
    /**
     * Timestamp when these metrics were recorded
     */
    private Instant timestamp;
    
    /**
     * Overall measure of flow state intensity (0.0 to 1.0)
     */
    private double flowIntensity;
    
    /**
     * Ratio of challenge level to skill level (1.0 is optimal balance)
     */
    private double challengeSkillRatio;
    
    /**
     * Measure of cognitive load (0.0 to 1.0)
     */
    private double cognitiveLoad;
    
    /**
     * Current level of attentional focus (0.0 to 1.0)
     */
    private double attentionalFocus;
    
    /**
     * Map of thought node IDs to their traversal frequencies
     */
    private Map<Long, Integer> traversalFrequencies;
    
    /**
     * Estimated processing capacity under current flow conditions
     */
    private double processingCapacity;
    
    /**
     * Time spent in current flow state (in milliseconds)
     */
    private long flowStateDuration;
    
    /**
     * Returns whether the current state is considered a high flow state
     */
    public boolean isHighFlowState() {
        return flowIntensity > 0.7 && 
               challengeSkillRatio > 0.9 && challengeSkillRatio < 1.1 &&
               attentionalFocus > 0.8;
    }
    
    /**
     * Returns whether the current state indicates cognitive overload
     */
    public boolean isCognitiveOverload() {
        return cognitiveLoad > 0.8 || challengeSkillRatio > 1.3;
    }
    
    /**
     * Creates a default metrics object with neutral values
     */
    public static FlowMetrics createDefault() {
        return FlowMetrics.builder()
                .timestamp(Instant.now())
                .flowIntensity(0.5)
                .challengeSkillRatio(1.0)
                .cognitiveLoad(0.5)
                .attentionalFocus(0.5)
                .processingCapacity(0.5)
                .flowStateDuration(0)
                .build();
    }
} 