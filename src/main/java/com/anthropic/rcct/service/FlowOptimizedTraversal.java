package com.anthropic.rcct.service;

import com.anthropic.rcct.model.CCTModel;
import com.anthropic.rcct.model.FlowMetrics;
import com.anthropic.rcct.model.ThoughtNode;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Implements flow-optimized traversal strategies for thought graphs.
 * This service adapts traversal patterns based on current flow state
 * to optimize cognitive resource allocation.
 */
@Service
@RequiredArgsConstructor
public class FlowOptimizedTraversal {
    
    private final FlowStateMonitor flowMonitor;
    private final AttentionalModulator attentionModulator;
    
    /**
     * Traversal patterns supported by the flow-optimized traversal
     */
    public enum TraversalPattern {
        DEPTH_FIRST,
        BREADTH_FIRST,
        ATTENTION_WEIGHTED,
        PATTERN_GUIDED,
        FLOW_ADAPTIVE
    }
    
    /**
     * Context object for a traversal operation
     */
    public static class TraversalContext {
        private final Map<String, Object> parameters = new HashMap<>();
        private final List<Long> visitedNodeIds = new ArrayList<>();
        private TraversalPattern pattern;
        
        public TraversalContext(TraversalPattern pattern) {
            this.pattern = pattern;
        }
        
        public void markVisited(Long nodeId) {
            visitedNodeIds.add(nodeId);
        }
        
        public boolean isVisited(Long nodeId) {
            return visitedNodeIds.contains(nodeId);
        }
        
        public TraversalPattern getPattern() {
            return pattern;
        }
        
        public void setParameter(String key, Object value) {
            parameters.put(key, value);
        }
        
        public Object getParameter(String key) {
            return parameters.get(key);
        }
    }
    
    /**
     * Traverses a thought structure using a flow-optimized pattern
     * 
     * @param root The root node to start traversal from
     * @param model The CCT model containing the thought structure
     * @param context Optional traversal context (if null, a default context will be created)
     * @return A flux of thought nodes in traversal order
     */
    public Flux<ThoughtNode> traverse(ThoughtNode root, CCTModel model, TraversalContext context) {
        // If no context provided, create a default context
        if (context == null) {
            // Get current flow metrics
            FlowMetrics metrics = flowMonitor.getCurrentMetrics();
            
            // Select optimal pattern based on flow state
            TraversalPattern optimalPattern = selectOptimalPattern(metrics);
            
            // Create new context with optimal pattern
            context = new TraversalContext(optimalPattern);
        }
        
        // Execute traversal based on the selected pattern
        switch (context.getPattern()) {
            case DEPTH_FIRST:
                return executeDepthFirstTraversal(root, model, context);
            case BREADTH_FIRST:
                return executeBreadthFirstTraversal(root, model, context);
            case ATTENTION_WEIGHTED:
                return executeAttentionWeightedTraversal(root, model, context);
            case PATTERN_GUIDED:
                return executePatternGuidedTraversal(root, model, context);
            case FLOW_ADAPTIVE:
            default:
                return executeFlowAdaptiveTraversal(root, model, context);
        }
    }
    
    /**
     * Selects the optimal traversal pattern based on current flow metrics
     */
    private TraversalPattern selectOptimalPattern(FlowMetrics metrics) {
        // High flow state with recognized patterns suggests pattern-guided traversal
        if (metrics.getFlowIntensity() > 0.8) {
            return TraversalPattern.PATTERN_GUIDED;
        }
        
        // High challenge-skill balance suggests attention-weighted traversal
        if (metrics.getChallengeSkillRatio() > 0.9 && metrics.getChallengeSkillRatio() < 1.1) {
            return TraversalPattern.ATTENTION_WEIGHTED;
        }
        
        // High cognitive load suggests breadth-first (less demanding) traversal
        if (metrics.getCognitiveLoad() > 0.7) {
            return TraversalPattern.BREADTH_FIRST;
        }
        
        // Default to depth-first traversal
        return TraversalPattern.DEPTH_FIRST;
    }
    
    /**
     * Executes a depth-first traversal pattern
     */
    private Flux<ThoughtNode> executeDepthFirstTraversal(
            ThoughtNode root, CCTModel model, TraversalContext context) {
        
        // Mark current node as visited
        context.markVisited(root.getId());
        
        // Get child nodes
        List<ThoughtNode> children = model.getChildThoughtNodes(root.getId());
        
        // First emit the current node
        return Flux.just(root)
            // Then traverse children depth-first
            .concatWith(Flux.fromIterable(children)
                .filter(child -> !context.isVisited(child.getId()))
                .concatMap(child -> executeDepthFirstTraversal(child, model, context))
            );
    }
    
    /**
     * Executes a breadth-first traversal pattern
     */
    private Flux<ThoughtNode> executeBreadthFirstTraversal(
            ThoughtNode root, CCTModel model, TraversalContext context) {
        
        // Use a queue-based approach for BFS
        List<ThoughtNode> queue = new ArrayList<>();
        queue.add(root);
        
        return Flux.create(emitter -> {
            while (!queue.isEmpty()) {
                // Get next node from queue
                ThoughtNode current = queue.remove(0);
                
                // Skip if already visited
                if (context.isVisited(current.getId())) {
                    continue;
                }
                
                // Mark as visited
                context.markVisited(current.getId());
                
                // Emit current node
                emitter.next(current);
                
                // Add children to queue
                List<ThoughtNode> children = model.getChildThoughtNodes(current.getId());
                queue.addAll(children);
            }
            emitter.complete();
        });
    }
    
    /**
     * Executes an attention-weighted traversal pattern
     */
    private Flux<ThoughtNode> executeAttentionWeightedTraversal(
            ThoughtNode root, CCTModel model, TraversalContext context) {
        
        // Get current flow metrics
        FlowMetrics metrics = flowMonitor.getCurrentMetrics();
        
        // Mark current node as visited
        context.markVisited(root.getId());
        
        // Get child nodes and calculate their attentional weights
        List<ThoughtNode> children = model.getChildThoughtNodes(root.getId());
        
        // Calculate weights for all children
        Map<ThoughtNode, Double> weights = new HashMap<>();
        for (ThoughtNode child : children) {
            if (!context.isVisited(child.getId())) {
                double weight = attentionModulator.calculateAttentionalWeight(child, metrics);
                weights.put(child, weight);
            }
        }
        
        // Sort children by weight (highest first)
        List<ThoughtNode> sortedChildren = weights.entrySet().stream()
                .sorted(Map.Entry.<ThoughtNode, Double>comparingByValue().reversed())
                .map(Map.Entry::getKey)
                .collect(Collectors.toList());
        
        // First emit the current node
        return Flux.just(root)
            // Then traverse children in weight order
            .concatWith(Flux.fromIterable(sortedChildren)
                .concatMap(child -> executeAttentionWeightedTraversal(child, model, context))
            );
    }
    
    /**
     * Executes a pattern-guided traversal based on recognized patterns
     */
    private Flux<ThoughtNode> executePatternGuidedTraversal(
            ThoughtNode root, CCTModel model, TraversalContext context) {
        // In a full implementation, this would use pattern recognition to guide traversal
        // For now, this is a simplified version similar to attention-weighted
        return executeAttentionWeightedTraversal(root, model, context);
    }
    
    /**
     * Executes a flow-adaptive traversal that adjusts dynamically
     */
    private Flux<ThoughtNode> executeFlowAdaptiveTraversal(
            ThoughtNode root, CCTModel model, TraversalContext context) {
        
        // Get current flow metrics
        FlowMetrics metrics = flowMonitor.getCurrentMetrics();
        
        // Continuously re-evaluate optimal pattern based on flow state
        TraversalPattern adaptivePattern = selectOptimalPattern(metrics);
        
        // Update context with the adaptive pattern
        context.pattern = adaptivePattern;
        
        // Execute traversal with the adaptive pattern
        switch (adaptivePattern) {
            case DEPTH_FIRST:
                return executeDepthFirstTraversal(root, model, context);
            case BREADTH_FIRST:
                return executeBreadthFirstTraversal(root, model, context);
            case ATTENTION_WEIGHTED:
                return executeAttentionWeightedTraversal(root, model, context);
            case PATTERN_GUIDED:
                return executePatternGuidedTraversal(root, model, context);
            default:
                return executeDepthFirstTraversal(root, model, context);
        }
    }
} 