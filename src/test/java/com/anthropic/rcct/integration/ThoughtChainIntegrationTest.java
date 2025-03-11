package com.anthropic.rcct.integration;

import com.anthropic.rcct.model.Thought;
import com.anthropic.rcct.model.ThoughtChain;
import com.anthropic.rcct.model.Domain;
import com.anthropic.rcct.service.ThoughtProcessingService;
import com.anthropic.rcct.service.DomainMappingService;
import com.anthropic.rcct.service.MetaCognitiveMonitor;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@ActiveProfiles("test")
public class ThoughtChainIntegrationTest {

    @Autowired
    private ThoughtProcessingService thoughtProcessingService;

    @Autowired
    private DomainMappingService domainMappingService;

    @Autowired
    private MetaCognitiveMonitor metaCognitiveMonitor;

    private ThoughtChain testChain;
    private Domain sourceDomain;
    private Domain targetDomain;

    @BeforeEach
    void setUp() {
        sourceDomain = new Domain("mathematics", Map.of(
            "dimensionality", 3,
            "complexity", "high"
        ));
        
        targetDomain = new Domain("physics", Map.of(
            "dimensionality", 4,
            "complexity", "high"
        ));

        testChain = new ThoughtChain();
        testChain.setSourceDomain(sourceDomain);
        testChain.setTargetDomain(targetDomain);
    }

    @Test
    void testCompleteThoughtChainProcessing() {
        // Create initial thought
        Thought initialThought = new Thought("Vector spaces in R3");
        initialThought.setDimensionalCoordinates(new double[]{1.0, 0.5, 0.8});
        testChain.addThought(initialThought);

        // Process the thought chain
        ThoughtChain processedChain = thoughtProcessingService.processChain(testChain);

        // Verify the chain was processed correctly
        assertNotNull(processedChain);
        assertTrue(processedChain.getThoughts().size() > 1);
        
        // Verify domain mapping
        Map<String, Double> domainMapping = domainMappingService.calculateDomainMapping(
            processedChain.getSourceDomain(),
            processedChain.getTargetDomain()
        );
        assertTrue(domainMapping.get("mappingScore") > 0.5);

        // Verify metacognitive monitoring
        assertTrue(metaCognitiveMonitor.isProcessingCoherent(processedChain));
        assertFalse(metaCognitiveMonitor.detectAnomalies(processedChain));
    }

    @Test
    void testCrossDomainTransformation() {
        // Set up cross-domain test data
        Thought mathematicalThought = new Thought("Differential equations");
        mathematicalThought.setDimensionalCoordinates(new double[]{0.7, 0.9, 0.6});
        testChain.addThought(mathematicalThought);

        // Transform to physics domain
        ThoughtChain transformedChain = thoughtProcessingService.transformAcrossDomains(
            testChain,
            sourceDomain,
            targetDomain
        );

        // Verify transformation
        assertNotNull(transformedChain);
        assertTrue(transformedChain.getThoughts().size() >= testChain.getThoughts().size());
        
        // Verify semantic preservation
        double semanticPreservation = thoughtProcessingService.calculateSemanticPreservation(
            testChain,
            transformedChain
        );
        assertTrue(semanticPreservation > 0.7);
    }

    @Test
    void testErrorHandlingAndRecovery() {
        // Create invalid thought to test error handling
        Thought invalidThought = new Thought(null);
        testChain.addThought(invalidThought);

        // Process chain with invalid thought
        ThoughtChain processedChain = thoughtProcessingService.processChain(testChain);

        // Verify error handling
        assertNotNull(processedChain);
        assertTrue(metaCognitiveMonitor.getProcessingErrors().size() > 0);
        
        // Verify recovery mechanism
        assertTrue(processedChain.isValid());
        assertFalse(processedChain.getThoughts().contains(invalidThought));
    }
} 