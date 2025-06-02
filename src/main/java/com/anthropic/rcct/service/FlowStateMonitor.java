package com.anthropic.rcct.service;

import com.anthropic.rcct.model.FlowMetrics;
import com.anthropic.rcct.model.ThoughtNode;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Service responsible for monitoring and tracking flow state metrics during
 * thought processing operations. This service integrates biopsychological
 * principles of flow state with computational processing.
 */
@Service
public class FlowStateMonitor {
    
    private final AtomicReference<FlowMetrics> currentMetrics = 
            new AtomicReference<>(FlowMetrics.createDefault());
    
    private final List<FlowMetrics> historicalMetrics = new CopyOnWriteArrayList<>();
    private final Map<Long, Integer> nodeTraversalCounts = new ConcurrentHashMap<>();
    private final Map<Long, Instant> nodeProcessingTimes = new ConcurrentHashMap<>();
    
    private Instant flowStateStartTime = Instant.now();
    
    /**
     * Returns the current flow metrics
     */
    public FlowMetrics getCurrentMetrics() {
        return currentMetrics.get();
    }
    
    /**
     * Returns the list of historical metrics
     */
    public List<FlowMetrics> getHistoricalMetrics() {
        return Collections.unmodifiableList(historicalMetrics);
    }
    
    /**
     * Updates the flow state metrics based on processing operations
     * 
     * @param nodeId The ID of the node being processed
     * @param processingResult The result of processing the node
     * @return Updated flow metrics
     */
    public Mono<FlowMetrics> updateMetrics(Long nodeId, Object processingResult) {
        // Update traversal counts
        nodeTraversalCounts.compute(nodeId, (k, v) -> v == null ? 1 : v + 1);
        
        // Record processing time
        nodeProcessingTimes.put(nodeId, Instant.now());
        
        // Calculate new metrics
        FlowMetrics newMetrics = calculateNewMetrics(nodeId, processingResult);
        
        // Store in history if significant change detected
        if (isSignificantChange(currentMetrics.get(), newMetrics)) {
            historicalMetrics.add(newMetrics);
            
            // If flow state changed significantly, reset the flow state timer
            if (Math.abs(currentMetrics.get().getFlowIntensity() - newMetrics.getFlowIntensity()) > 0.2) {
                flowStateStartTime = Instant.now();
            }
        }
        
        // Update current metrics
        currentMetrics.set(newMetrics);
        
        return Mono.just(newMetrics);
    }
    
    /**
     * Calculates updated flow metrics based on processing operations
     * 
     * @param nodeId The ID of the node being processed
     * @param processingResult The result of processing the node
     * @return Updated flow metrics
     */
    private FlowMetrics calculateNewMetrics(Long nodeId, Object processingResult) {
        FlowMetrics current = currentMetrics.get();
        
        // Create a copy of traversal frequencies
        Map<Long, Integer> traversalFrequencies = new HashMap<>(nodeTraversalCounts);
        
        // Calculate processing speed metric
        double processingSpeed = calculateProcessingSpeed();
        
        // Calculate attentional focus based on traversal pattern
        double attentionalFocus = calculateAttentionalFocus(nodeId);
        
        // Calculate challenge level based on node complexity
        double challengeLevel = calculateChallengeLevel(nodeId);
        
        // Calculate skill level based on processing history
        double skillLevel = calculateSkillLevel();
        
        // Calculate challenge-skill ratio (1.0 is ideal)
        double challengeSkillRatio = challengeLevel / Math.max(0.1, skillLevel);
        
        // Calculate cognitive load
        double cognitiveLoad = calculateCognitiveLoad(nodeId);
        
        // Calculate flow state intensity
        double flowIntensity = calculateFlowIntensity(
                challengeSkillRatio, 
                attentionalFocus, 
                processingSpeed, 
                cognitiveLoad);
        
        // Calculate flow state duration
        long flowStateDuration = Duration.between(flowStateStartTime, Instant.now()).toMillis();
        
        // Calculate processing capacity under current flow conditions
        double processingCapacity = calculateProcessingCapacity(flowIntensity, cognitiveLoad);
        
        return FlowMetrics.builder()
                .timestamp(Instant.now())
                .flowIntensity(flowIntensity)
                .challengeSkillRatio(challengeSkillRatio)
                .cognitiveLoad(cognitiveLoad)
                .attentionalFocus(attentionalFocus)
                .traversalFrequencies(traversalFrequencies)
                .processingCapacity(processingCapacity)
                .flowStateDuration(flowStateDuration)
                .build();
    }
    
    /**
     * Calculates the processing speed based on recent operations
     */
    private double calculateProcessingSpeed() {
        // Simplified implementation - could be expanded with more sophisticated metrics
        if (nodeProcessingTimes.size() < 2) {
            return 0.5; // Default value
        }
        
        // Calculate average time between node processing operations
        List<Instant> times = new ArrayList<>(nodeProcessingTimes.values());
        times.sort(Instant::compareTo);
        
        double totalDuration = 0;
        for (int i = 1; i < times.size(); i++) {
            totalDuration += Duration.between(times.get(i-1), times.get(i)).toMillis();
        }
        
        double avgDuration = totalDuration / (times.size() - 1);
        
        // Normalize to 0-1 range (faster processing = higher value)
        // 10ms is considered very fast, 1000ms is considered very slow
        return Math.max(0, Math.min(1, 1.0 - (avgDuration - 10) / 990));
    }
    
    /**
     * Calculates attentional focus based on traversal pattern
     */
    private double calculateAttentionalFocus(Long currentNodeId) {
        // If we're repeatedly visiting the same nodes, that indicates high focus
        // If we're jumping around randomly, that indicates low focus
        
        // Get the distinct count of nodes visited
        int distinctNodes = nodeTraversalCounts.size();
        
        // Get the total count of traversals
        int totalTraversals = nodeTraversalCounts.values().stream().mapToInt(Integer::intValue).sum();
        
        if (totalTraversals < 5) {
            return 0.5; // Default for new sessions
        }
        
        // Calculate ratio of distinct nodes to total traversals
        // Lower ratio (fewer distinct nodes) suggests higher focus
        double distinctRatio = (double) distinctNodes / totalTraversals;
        
        // Calculate focus score (inverse of distinct ratio, normalized)
        double focusScore = 1.0 - Math.min(1.0, distinctRatio * 5);
        
        return focusScore;
    }
    
    /**
     * Calculates challenge level based on node complexity
     */
    private double calculateChallengeLevel(Long nodeId) {
        // Simplified implementation - placeholder for more sophisticated node complexity analysis
        return 0.6; // Default moderate challenge level
    }
    
    /**
     * Calculates skill level based on processing history
     */
    private double calculateSkillLevel() {
        // Simplified implementation - could analyze historical metrics
        // to determine skill level based on processing patterns
        return 0.6; // Default moderate skill level
    }
    
    /**
     * Calculates cognitive load based on processing complexity
     */
    private double calculateCognitiveLoad(Long nodeId) {
        // Simplified implementation - placeholder for more sophisticated
        // cognitive load analysis based on node complexity and processing depth
        return 0.5; // Default moderate cognitive load
    }
    
    /**
     * Calculates flow intensity based on multiple metrics
     */
    private double calculateFlowIntensity(
            double challengeSkillRatio, 
            double attentionalFocus,
            double processingSpeed,
            double cognitiveLoad) {
        
        // Flow is highest when:
        // - Challenge-skill ratio is close to 1.0
        // - Attentional focus is high
        // - Processing speed is high
        // - Cognitive load is moderate (not too high, not too low)
        
        // Calculate challenge-skill balance contribution to flow
        // (closer to 1.0 is better)
        double challengeSkillBalance = 1.0 - Math.min(1.0, Math.abs(challengeSkillRatio - 1.0));
        
        // Calculate cognitive load contribution
        // (highest at moderate cognitive load, around 0.5-0.7)
        double cognitiveLoadContribution = 1.0 - Math.min(1.0, Math.abs(cognitiveLoad - 0.6) * 2.5);
        
        // Calculate weighted average of all factors
        return 0.35 * challengeSkillBalance +
               0.30 * attentionalFocus +
               0.20 * processingSpeed +
               0.15 * cognitiveLoadContribution;
    }
    
    /**
     * Calculates processing capacity under current flow conditions
     */
    private double calculateProcessingCapacity(double flowIntensity, double cognitiveLoad) {
        // High flow intensity increases capacity
        // Excessive cognitive load decreases capacity
        
        double baseCapacity = 0.5;
        double flowBonus = flowIntensity * 0.5;
        double loadPenalty = Math.max(0, (cognitiveLoad - 0.7) * 0.5);
        
        return Math.min(1.0, Math.max(0, baseCapacity + flowBonus - loadPenalty));
    }
    
    /**
     * Determines if there's a significant change in metrics
     */
    private boolean isSignificantChange(FlowMetrics previous, FlowMetrics current) {
        // Check if any key metric has changed by more than the significance threshold
        final double THRESHOLD = 0.1;
        
        return Math.abs(previous.getFlowIntensity() - current.getFlowIntensity()) > THRESHOLD ||
               Math.abs(previous.getChallengeSkillRatio() - current.getChallengeSkillRatio()) > THRESHOLD ||
               Math.abs(previous.getCognitiveLoad() - current.getCognitiveLoad()) > THRESHOLD ||
               Math.abs(previous.getAttentionalFocus() - current.getAttentionalFocus()) > THRESHOLD;
    }
    
    /**
     * Resets the flow state monitor
     */
    public void reset() {
        currentMetrics.set(FlowMetrics.createDefault());
        historicalMetrics.clear();
        nodeTraversalCounts.clear();
        nodeProcessingTimes.clear();
        flowStateStartTime = Instant.now();
    }
} 