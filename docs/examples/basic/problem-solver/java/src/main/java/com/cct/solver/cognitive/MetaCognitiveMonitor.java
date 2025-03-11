package com.cct.solver.cognitive;

import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import java.util.*;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicReference;

@Slf4j
public class MetaCognitiveMonitor {
    private final Queue<MetaCognitiveEvent> eventStream;
    private final Map<String, MetricTracker> metrics;
    private final AtomicReference<SystemState> currentState;
    
    public MetaCognitiveMonitor() {
        this.eventStream = new ConcurrentLinkedQueue<>();
        this.metrics = new HashMap<>();
        this.currentState = new AtomicReference<>(new SystemState());
        initializeMetrics();
    }
    
    private void initializeMetrics() {
        metrics.put("complexity", new MetricTracker("Thought Space Complexity"));
        metrics.put("coherence", new MetricTracker("Semantic Coherence"));
        metrics.put("recursion_depth", new MetricTracker("Recursive Processing Depth"));
        metrics.put("pattern_emergence", new MetricTracker("Pattern Emergence Rate"));
    }
    
    public void recordThoughtAddition(DimensionalThoughtSpace.ThoughtVector thought) {
        MetaCognitiveEvent event = MetaCognitiveEvent.builder()
            .type(EventType.THOUGHT_ADDITION)
            .thoughtId(thought.getId())
            .timestamp(System.currentTimeMillis())
            .metadata(Map.of(
                "vector_dimension", thought.getVector().length,
                "attribute_count", thought.getAttributes().size(),
                "tags", thought.getTags()
            ))
            .build();
            
        eventStream.offer(event);
        updateMetrics(event);
    }
    
    public void recordTraversal(List<DimensionalThoughtSpace.ThoughtVector> path) {
        MetaCognitiveEvent event = MetaCognitiveEvent.builder()
            .type(EventType.SPACE_TRAVERSAL)
            .timestamp(System.currentTimeMillis())
            .metadata(Map.of(
                "path_length", path.size(),
                "unique_tags", path.stream()
                    .flatMap(t -> t.getTags().stream())
                    .distinct()
                    .count()
            ))
            .build();
            
        eventStream.offer(event);
        updateMetrics(event);
    }
    
    private void updateMetrics(MetaCognitiveEvent event) {
        switch (event.getType()) {
            case THOUGHT_ADDITION:
                updateComplexityMetric(event);
                updateCoherenceMetric(event);
                break;
            case SPACE_TRAVERSAL:
                updateRecursionMetric(event);
                updatePatternMetric(event);
                break;
        }
        
        checkThresholds();
    }
    
    private void updateComplexityMetric(MetaCognitiveEvent event) {
        MetricTracker tracker = metrics.get("complexity");
        double vectorDimension = (Integer) event.getMetadata().get("vector_dimension");
        double attributeCount = (Integer) event.getMetadata().get("attribute_count");
        
        tracker.addValue((vectorDimension + attributeCount) / 2.0);
    }
    
    private void updateCoherenceMetric(MetaCognitiveEvent event) {
        // Implement coherence calculation based on semantic relationships
    }
    
    private void updateRecursionMetric(MetaCognitiveEvent event) {
        if (event.getType() == EventType.SPACE_TRAVERSAL) {
            MetricTracker tracker = metrics.get("recursion_depth");
            long pathLength = (Long) event.getMetadata().get("path_length");
            tracker.addValue(Math.log(pathLength) / Math.log(2)); // Log2 of path length
        }
    }
    
    private void updatePatternMetric(MetaCognitiveEvent event) {
        // Implement pattern emergence detection
    }
    
    private void checkThresholds() {
        SystemState newState = new SystemState();
        
        newState.setComplexityLevel(calculateComplexityLevel());
        newState.setCoherenceLevel(calculateCoherenceLevel());
        newState.setRecursionLevel(calculateRecursionLevel());
        newState.setPatternLevel(calculatePatternLevel());
        
        SystemState oldState = currentState.get();
        if (!newState.equals(oldState)) {
            currentState.set(newState);
            log.info("System state change detected: {}", newState);
        }
    }
    
    private double calculateComplexityLevel() {
        return metrics.get("complexity").getRecentAverage();
    }
    
    private double calculateCoherenceLevel() {
        return metrics.get("coherence").getRecentAverage();
    }
    
    private double calculateRecursionLevel() {
        return metrics.get("recursion_depth").getRecentAverage();
    }
    
    private double calculatePatternLevel() {
        return metrics.get("pattern_emergence").getRecentAverage();
    }
    
    @Data
    private static class MetricTracker {
        private final String name;
        private final Queue<Double> recentValues;
        private static final int WINDOW_SIZE = 100;
        
        public MetricTracker(String name) {
            this.name = name;
            this.recentValues = new LinkedList<>();
        }
        
        public void addValue(double value) {
            recentValues.offer(value);
            if (recentValues.size() > WINDOW_SIZE) {
                recentValues.poll();
            }
        }
        
        public double getRecentAverage() {
            return recentValues.stream()
                .mapToDouble(Double::doubleValue)
                .average()
                .orElse(0.0);
        }
    }
    
    @Data
    private static class SystemState {
        private double complexityLevel;
        private double coherenceLevel;
        private double recursionLevel;
        private double patternLevel;
    }
    
    @Data
    @Builder
    private static class MetaCognitiveEvent {
        private final EventType type;
        private final String thoughtId;
        private final long timestamp;
        private final Map<String, Object> metadata;
    }
    
    private enum EventType {
        THOUGHT_ADDITION,
        SPACE_TRAVERSAL
    }
} 