package com.anthropic.rcct.service;

import com.anthropic.rcct.model.FlowMetrics;
import com.anthropic.rcct.model.ThoughtNode;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.util.HashMap;
import java.util.Map;

/**
 * Service responsible for modulating attentional resources based on flow state.
 * This service determines how computational resources should be allocated based
 * on the current flow state and thought characteristics.
 */
@Service
public class AttentionalModulator {
    
    private final FlowStateMonitor flowStateMonitor;
    
    /**
     * Construct a new AttentionalModulator with the specified FlowStateMonitor
     */
    public AttentionalModulator(FlowStateMonitor flowStateMonitor) {
        this.flowStateMonitor = flowStateMonitor;
    }
    
    /**
     * Calculate the attentional weight for a given thought node based on current flow metrics.
     * This weight determines how much computational focus should be placed on the node.
     * 
     * @param node The thought node to calculate weight for
     * @param metrics The current flow metrics
     * @return Attentional weight (0.0 to 1.0)
     */
    public double calculateAttentionalWeight(ThoughtNode node, FlowMetrics metrics) {
        // Base weight starts at medium value
        double baseWeight = 0.5;
        
        // Adjustments based on node characteristics
        double depthAdjustment = calculateDepthAdjustment(node);
        double complexityAdjustment = calculateComplexityAdjustment(node);
        double recencyAdjustment = calculateRecencyAdjustment(node, metrics);
        double relevanceAdjustment = calculateRelevanceAdjustment(node, metrics);
        
        // Flow state adjustments
        double flowAdjustment = calculateFlowAdjustment(metrics);
        
        // Combine adjustments with appropriate weights
        double finalWeight = baseWeight +
                (0.15 * depthAdjustment) +
                (0.20 * complexityAdjustment) +
                (0.25 * recencyAdjustment) +
                (0.20 * relevanceAdjustment) +
                (0.20 * flowAdjustment);
        
        // Ensure weight is within valid range
        return Math.max(0.0, Math.min(1.0, finalWeight));
    }
    
    /**
     * Allocate computational resources based on the provided processing parameters
     * and current flow state.
     * 
     * @param params Processing parameters that guide resource allocation
     * @return Allocated computational resources
     */
    public Mono<Map<String, Object>> allocateResources(Map<String, Object> params) {
        FlowMetrics currentMetrics = flowStateMonitor.getCurrentMetrics();
        
        // Create resources map with default allocations
        Map<String, Object> resources = new HashMap<>();
        
        // Base resource allocation
        resources.put("processingDepth", calculateProcessingDepth(currentMetrics));
        resources.put("parallelismLevel", calculateParallelismLevel(currentMetrics));
        resources.put("memoizationThreshold", calculateMemoizationThreshold(currentMetrics));
        resources.put("timeoutDuration", calculateTimeoutDuration(currentMetrics));
        
        // Apply any overrides from parameters
        params.forEach((key, value) -> {
            if (resources.containsKey(key)) {
                resources.put(key, value);
            }
        });
        
        return Mono.just(resources);
    }
    
    /**
     * Calculate adjustment based on node depth in the thought hierarchy
     */
    private double calculateDepthAdjustment(ThoughtNode node) {
        // Higher depth nodes get lower weight in default traversal
        if (node.getDepth() == null) {
            return 0.0;
        }
        
        // Normalize depth adjustment (-0.3 to +0.1)
        // Deeper nodes get less attention by default
        return Math.max(-0.3, Math.min(0.1, 0.1 - (node.getDepth() * 0.1)));
    }
    
    /**
     * Calculate adjustment based on thought complexity
     */
    private double calculateComplexityAdjustment(ThoughtNode node) {
        // Simplified implementation - would use more sophisticated
        // complexity metrics in a full implementation
        return 0.0;
    }
    
    /**
     * Calculate adjustment based on recency of node access
     */
    private double calculateRecencyAdjustment(ThoughtNode node, FlowMetrics metrics) {
        // If the node has been traversed frequently, it gets higher weight
        Integer traversalCount = metrics.getTraversalFrequencies().get(node.getId());
        
        if (traversalCount == null || traversalCount == 0) {
            return -0.1; // Slight negative adjustment for never-visited nodes
        }
        
        // Normalize traversal count adjustment (-0.1 to +0.2)
        return Math.max(-0.1, Math.min(0.2, (traversalCount - 1) * 0.05));
    }
    
    /**
     * Calculate adjustment based on thought relevance to current focus
     */
    private double calculateRelevanceAdjustment(ThoughtNode node, FlowMetrics metrics) {
        // Simplified implementation
        return 0.0;
    }
    
    /**
     * Calculate adjustment based on flow state
     */
    private double calculateFlowAdjustment(FlowMetrics metrics) {
        // In high flow states, we want to deepen focus on a few relevant nodes
        // In low flow states, we want to broaden focus across more nodes
        
        if (metrics.isHighFlowState()) {
            return 0.2; // Increase focus in high flow states
        } else if (metrics.isCognitiveOverload()) {
            return -0.2; // Decrease focus in overload states
        } else {
            return 0.0; // No adjustment for neutral states
        }
    }
    
    /**
     * Calculate optimal processing depth based on current flow metrics
     */
    private int calculateProcessingDepth(FlowMetrics metrics) {
        // Base depth
        int baseDepth = 3;
        
        // Adjust based on flow intensity and processing capacity
        if (metrics.isHighFlowState()) {
            // Deeper processing in high flow states
            return baseDepth + 2;
        } else if (metrics.isCognitiveOverload()) {
            // Shallower processing in overload states
            return Math.max(1, baseDepth - 1);
        } else {
            return baseDepth;
        }
    }
    
    /**
     * Calculate optimal parallelism level based on current flow metrics
     */
    private int calculateParallelismLevel(FlowMetrics metrics) {
        // Base parallelism
        int baseParallelism = Runtime.getRuntime().availableProcessors() / 2;
        
        // Adjust based on flow intensity and processing capacity
        double adjustment = metrics.getProcessingCapacity() * 0.5;
        
        return Math.max(1, (int)(baseParallelism * (1.0 + adjustment)));
    }
    
    /**
     * Calculate optimal memoization threshold based on current flow metrics
     */
    private double calculateMemoizationThreshold(FlowMetrics metrics) {
        // Base threshold
        double baseThreshold = 0.5;
        
        // In high flow states, we can be more aggressive with memoization
        if (metrics.isHighFlowState()) {
            return baseThreshold - 0.2; // Lower threshold = more memoization
        } else if (metrics.isCognitiveOverload()) {
            return baseThreshold - 0.3; // Even more memoization in overload
        } else {
            return baseThreshold;
        }
    }
    
    /**
     * Calculate optimal timeout duration based on current flow metrics
     */
    private long calculateTimeoutDuration(FlowMetrics metrics) {
        // Base timeout in milliseconds
        long baseTimeout = 1000;
        
        // In high flow states, we can allocate more time to processing
        if (metrics.isHighFlowState()) {
            return (long)(baseTimeout * 1.5);
        } else if (metrics.isCognitiveOverload()) {
            return (long)(baseTimeout * 0.7); // Shorter timeouts in overload
        } else {
            return baseTimeout;
        }
    }
} 