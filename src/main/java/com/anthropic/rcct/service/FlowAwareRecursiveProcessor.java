package com.anthropic.rcct.service;

import com.anthropic.rcct.model.CCTModel;
import com.anthropic.rcct.model.FlowMetrics;
import com.anthropic.rcct.model.ThoughtNode;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.Collectors;

/**
 * Enhanced recursive thought processor that integrates flow state awareness
 * into the evaluation of thought nodes. This service adjusts processing depth,
 * parallelism, and resource allocation based on the current flow state.
 */
@Service
@RequiredArgsConstructor
public class FlowAwareRecursiveProcessor {
    
    private final FlowStateMonitor flowMonitor;
    private final AttentionalModulator attentionModulator;
    private final ThoughtProcessingService processingService;
    
    // Executor service for parallel processing
    private final ExecutorService processingPool = 
            Executors.newWorkStealingPool(Runtime.getRuntime().availableProcessors());
    
    /**
     * Evaluates a thought node recursively with flow-optimized traversal patterns.
     * 
     * @param rootNode The starting point for evaluation
     * @param model The CCT model containing the thought nodes
     * @return Processed result with adaptive depth processing
     */
    public Mono<String> evaluateRecursively(ThoughtNode rootNode, CCTModel model) {
        // Acquire current flow metrics
        FlowMetrics currentMetrics = flowMonitor.getCurrentMetrics();
        
        // Determine optimal processing parameters based on flow state
        Map<String, Object> params = new HashMap<>();
        
        // Apply flow-optimized resource allocation
        return attentionModulator.allocateResources(params)
            .flatMap(allocatedResources -> {
                // Extract processing parameters
                int processingDepth = (int) allocatedResources.get("processingDepth");
                double memoizationThreshold = (double) allocatedResources.get("memoizationThreshold");
                
                // Check if we've already processed this node (memoization)
                if (model.getMemoizationCache().containsKey(rootNode.getId())) {
                    double randomValue = Math.random();
                    
                    // Only use memoized result if random value exceeds threshold
                    // Lower threshold = more likely to use memoized result
                    if (randomValue > memoizationThreshold) {
                        return Mono.just(model.getMemoizationCache().get(rootNode.getId()));
                    }
                }
                
                // Process the current node
                return processCurrentNode(rootNode, model, currentMetrics, processingDepth, 0);
            })
            .doOnNext(result -> 
                // Update flow metrics based on processing outcome
                flowMonitor.updateMetrics(rootNode.getId(), result)
            );
    }
    
    /**
     * Process the current node and its children based on flow state.
     * 
     * @param node The current thought node
     * @param model The CCT model
     * @param metrics Current flow metrics
     * @param maxDepth Maximum processing depth
     * @param currentDepth Current depth in the recursion
     * @return Processed node result
     */
    private Mono<String> processCurrentNode(
            ThoughtNode node, 
            CCTModel model, 
            FlowMetrics metrics,
            int maxDepth,
            int currentDepth) {
        
        // Stop recursion if we've reached maximum depth
        if (currentDepth >= maxDepth) {
            return Mono.just("Depth limit reached for node: " + node.getId());
        }
        
        // Calculate attentional weight to determine processing focus
        double attentionalWeight = attentionModulator.calculateAttentionalWeight(node, metrics);
        
        // Process sub-thoughts based on attentional weight
        return Mono.just(node)
            .flatMap(currentNode -> {
                // Get child nodes
                List<ThoughtNode> childNodes = model.getChildThoughtNodes(currentNode.getId());
                
                // Filter children based on attentional weight
                List<ThoughtNode> prioritizedChildren = childNodes.stream()
                    .filter(child -> 
                        // Higher attentional weight = process more children
                        attentionModulator.calculateAttentionalWeight(child, metrics) > 
                        (1.0 - attentionalWeight) * 0.7
                    )
                    .collect(Collectors.toList());
                
                // Process children in parallel if we have multiple children
                if (!prioritizedChildren.isEmpty()) {
                    return Flux.fromIterable(prioritizedChildren)
                        .flatMap(child -> 
                            // Dynamic depth adjustment based on flow state
                            processCurrentNode(child, model, metrics, maxDepth, currentDepth + 1)
                                .subscribeOn(Schedulers.fromExecutor(processingPool))
                        )
                        .collectList()
                        .flatMap(childResults -> {
                            // Combine child results with current node processing
                            String processedContent = processingService.processNodeContent(node);
                            String combinedResult = processedContent + "\n" + 
                                    String.join("\n", childResults);
                            
                            // Store in memoization cache
                            model.getMemoizationCache().put(node.getId(), combinedResult);
                            
                            return Mono.just(combinedResult);
                        });
                } else {
                    // Process leaf node
                    String processedContent = processingService.processNodeContent(node);
                    
                    // Store in memoization cache
                    model.getMemoizationCache().put(node.getId(), processedContent);
                    
                    return Mono.just(processedContent);
                }
            });
    }
    
    /**
     * Process all nodes in the model with flow-optimized evaluation.
     * 
     * @param model The CCT model to process
     * @return List of processed results
     */
    public Mono<List<String>> processAllNodes(CCTModel model) {
        // Get root nodes of the model
        List<ThoughtNode> rootNodes = model.getRootThoughtNodes();
        
        // Process each root node
        return Flux.fromIterable(rootNodes)
            .flatMap(rootNode -> evaluateRecursively(rootNode, model))
            .collectList();
    }
    
    /**
     * Shut down the processing pool when no longer needed
     */
    public void shutdown() {
        processingPool.shutdown();
    }
} 