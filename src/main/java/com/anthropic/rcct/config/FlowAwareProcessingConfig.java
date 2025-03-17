package com.anthropic.rcct.config;

import com.anthropic.rcct.model.CCTModel;
import com.anthropic.rcct.service.AttentionalModulator;
import com.anthropic.rcct.service.FlowAwareRecursiveProcessor;
import com.anthropic.rcct.service.FlowOptimizedTraversal;
import com.anthropic.rcct.service.FlowStateMonitor;
import com.anthropic.rcct.service.ThoughtProcessingService;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Configuration class that sets up the flow-aware processing components
 * and defines their dependencies.
 */
@Configuration
public class FlowAwareProcessingConfig {

    /**
     * Creates the CCTModel bean that serves as the central model
     * for the recursive chain of thought framework.
     */
    @Bean
    public CCTModel cctModel() {
        return new CCTModel();
    }
    
    /**
     * Creates the FlowStateMonitor bean that tracks flow state metrics.
     */
    @Bean
    public FlowStateMonitor flowStateMonitor() {
        return new FlowStateMonitor();
    }
    
    /**
     * Creates the AttentionalModulator bean that modulates attentional resources
     * based on flow state.
     */
    @Bean
    public AttentionalModulator attentionalModulator(FlowStateMonitor flowStateMonitor) {
        return new AttentionalModulator(flowStateMonitor);
    }
    
    /**
     * Creates the FlowOptimizedTraversal bean that implements flow-optimized
     * traversal strategies.
     */
    @Bean
    public FlowOptimizedTraversal flowOptimizedTraversal(
            FlowStateMonitor flowStateMonitor,
            AttentionalModulator attentionalModulator) {
        return new FlowOptimizedTraversal(flowStateMonitor, attentionalModulator);
    }
    
    /**
     * Creates the FlowAwareRecursiveProcessor bean that enhances thought processing
     * with flow state awareness.
     */
    @Bean
    public FlowAwareRecursiveProcessor flowAwareRecursiveProcessor(
            FlowStateMonitor flowStateMonitor,
            AttentionalModulator attentionalModulator,
            ThoughtProcessingService processingService) {
        return new FlowAwareRecursiveProcessor(
                flowStateMonitor, 
                attentionalModulator,
                processingService);
    }
    
    /**
     * Creates the ThoughtProcessingService bean that processes thoughts
     * with flow-optimized strategies.
     */
    @Bean
    public ThoughtProcessingService thoughtProcessingService(
            CCTModel cctModel,
            FlowStateMonitor flowStateMonitor,
            AttentionalModulator attentionalModulator,
            FlowOptimizedTraversal traversalStrategy) {
        return new ThoughtProcessingService(
                cctModel,
                flowStateMonitor,
                attentionalModulator,
                traversalStrategy);
    }
} 