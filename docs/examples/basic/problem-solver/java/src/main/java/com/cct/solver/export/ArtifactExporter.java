package com.cct.solver.export;

import com.cct.solver.cognitive.DimensionalThoughtSpace.ThoughtVector;
import lombok.Builder;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import java.util.*;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.time.Instant;

@Slf4j
public class ArtifactExporter {
    private final Queue<Artifact> exportQueue;
    private final Map<String, RetentionPolicy> retentionPolicies;
    private final InterestObjectIdentifier interestIdentifier;
    
    public ArtifactExporter() {
        this.exportQueue = new ConcurrentLinkedQueue<>();
        this.retentionPolicies = new HashMap<>();
        this.interestIdentifier = new InterestObjectIdentifier();
        initializeRetentionPolicies();
    }
    
    private void initializeRetentionPolicies() {
        retentionPolicies.put("sensory", RetentionPolicy.builder()
            .type(RetentionType.CIRCULAR_BUFFER)
            .duration(2000) // 2 seconds
            .build());
            
        retentionPolicies.put("feature", RetentionPolicy.builder()
            .type(RetentionType.COMPLETE)
            .build());
            
        retentionPolicies.put("cognitive", RetentionPolicy.builder()
            .type(RetentionType.HIERARCHICAL)
            .compressionRatio(0.5)
            .build());
            
        retentionPolicies.put("meta", RetentionPolicy.builder()
            .type(RetentionType.COMPLETE)
            .indexing(true)
            .build());
    }
    
    public void exportThought(ThoughtVector thought, Map<String, Object> context) {
        if (interestIdentifier.isInteresting(thought, context)) {
            Artifact artifact = createArtifact(thought, context);
            exportQueue.offer(artifact);
            log.debug("Queued artifact for export: {}", artifact.getId());
        }
    }
    
    private Artifact createArtifact(ThoughtVector thought, Map<String, Object> context) {
        return Artifact.builder()
            .id(UUID.randomUUID().toString())
            .timestamp(Instant.now())
            .type(determineArtifactType(thought))
            .content(Map.of(
                "thought", thought,
                "context", context,
                "metadata", extractMetadata(thought, context)
            ))
            .retentionPolicy(selectRetentionPolicy(thought))
            .build();
    }
    
    private ArtifactType determineArtifactType(ThoughtVector thought) {
        if (thought.getTags().contains("sensory")) {
            return ArtifactType.SENSORY;
        } else if (thought.getTags().contains("feature")) {
            return ArtifactType.FEATURE;
        } else if (thought.getTags().contains("meta")) {
            return ArtifactType.META_COGNITIVE;
        } else {
            return ArtifactType.COGNITIVE;
        }
    }
    
    private Map<String, Object> extractMetadata(ThoughtVector thought, Map<String, Object> context) {
        Map<String, Object> metadata = new HashMap<>();
        metadata.putAll(thought.getAttributes());
        metadata.put("vector_dimension", thought.getVector().length);
        metadata.put("context_type", context.get("type"));
        metadata.put("timestamp", System.currentTimeMillis());
        return metadata;
    }
    
    private RetentionPolicy selectRetentionPolicy(ThoughtVector thought) {
        switch (determineArtifactType(thought)) {
            case SENSORY:
                return retentionPolicies.get("sensory");
            case FEATURE:
                return retentionPolicies.get("feature");
            case COGNITIVE:
                return retentionPolicies.get("cognitive");
            case META_COGNITIVE:
                return retentionPolicies.get("meta");
            default:
                return RetentionPolicy.builder()
                    .type(RetentionType.COMPLETE)
                    .build();
        }
    }
    
    @Data
    @Builder
    public static class Artifact {
        private final String id;
        private final Instant timestamp;
        private final ArtifactType type;
        private final Map<String, Object> content;
        private final RetentionPolicy retentionPolicy;
    }
    
    @Data
    @Builder
    public static class RetentionPolicy {
        private final RetentionType type;
        
        @Builder.Default
        private final long duration = -1; // -1 means indefinite
        
        @Builder.Default
        private final double compressionRatio = 1.0;
        
        @Builder.Default
        private final boolean indexing = false;
    }
    
    public enum RetentionType {
        CIRCULAR_BUFFER,
        COMPLETE,
        HIERARCHICAL
    }
    
    public enum ArtifactType {
        SENSORY,
        FEATURE,
        COGNITIVE,
        META_COGNITIVE
    }
    
    private static class InterestObjectIdentifier {
        public boolean isInteresting(ThoughtVector thought, Map<String, Object> context) {
            return isAttentionDriven(thought, context) ||
                   isAnomalyDriven(thought) ||
                   isPatternCompletion(thought) ||
                   isMetaCognitive(thought);
        }
        
        private boolean isAttentionDriven(ThoughtVector thought, Map<String, Object> context) {
            return context.containsKey("attention_duration") &&
                   (Long) context.get("attention_duration") > 300;
        }
        
        private boolean isAnomalyDriven(ThoughtVector thought) {
            return thought.getTags().contains("anomaly") ||
                   thought.getAttributes().containsKey("deviation_score");
        }
        
        private boolean isPatternCompletion(ThoughtVector thought) {
            return thought.getTags().contains("pattern_match") ||
                   thought.getAttributes().containsKey("completion_score");
        }
        
        private boolean isMetaCognitive(ThoughtVector thought) {
            return thought.getTags().contains("meta") ||
                   thought.getTags().contains("recursive");
        }
    }
} 