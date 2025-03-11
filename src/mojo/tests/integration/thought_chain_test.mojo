from testing import assert_equal, assert_true, assert_false
from memory.unsafe import Pointer
from collections.vector import DynamicVector
from math import sqrt

from rcct.model.thought import Thought
from rcct.model.thought_chain import ThoughtChain
from rcct.model.domain import Domain
from rcct.service.thought_processing import ThoughtProcessingService
from rcct.service.domain_mapping import DomainMappingService
from rcct.service.metacognitive_monitor import MetaCognitiveMonitor

struct ThoughtChainIntegrationTest:
    var thought_processing_service: ThoughtProcessingService
    var domain_mapping_service: DomainMappingService
    var metacognitive_monitor: MetaCognitiveMonitor
    var test_chain: ThoughtChain
    var source_domain: Domain
    var target_domain: Domain

    fn __init__(inout self):
        # Initialize services
        self.thought_processing_service = ThoughtProcessingService()
        self.domain_mapping_service = DomainMappingService()
        self.metacognitive_monitor = MetaCognitiveMonitor()
        
        # Set up test domains
        self.source_domain = Domain("mathematics")
        self.source_domain.set_property("dimensionality", 3)
        self.source_domain.set_property("complexity", "high")
        
        self.target_domain = Domain("physics")
        self.target_domain.set_property("dimensionality", 4)
        self.target_domain.set_property("complexity", "high")
        
        # Initialize test chain
        self.test_chain = ThoughtChain()
        self.test_chain.set_source_domain(self.source_domain)
        self.test_chain.set_target_domain(self.target_domain)

    fn test_complete_thought_chain_processing(self):
        # Create initial thought
        var initial_thought = Thought("Vector spaces in R3")
        initial_thought.set_dimensional_coordinates([1.0, 0.5, 0.8])
        self.test_chain.add_thought(initial_thought)

        # Process the thought chain
        let processed_chain = self.thought_processing_service.process_chain(self.test_chain)

        # Verify chain processing
        assert_true(processed_chain is not None)
        assert_true(processed_chain.get_thoughts().size() > 1)

        # Verify domain mapping
        let domain_mapping = self.domain_mapping_service.calculate_domain_mapping(
            processed_chain.get_source_domain(),
            processed_chain.get_target_domain()
        )
        assert_true(domain_mapping["mapping_score"] > 0.5)

        # Verify metacognitive monitoring
        assert_true(self.metacognitive_monitor.is_processing_coherent(processed_chain))
        assert_false(self.metacognitive_monitor.detect_anomalies(processed_chain))

    fn test_cross_domain_transformation(self):
        # Set up cross-domain test data
        var mathematical_thought = Thought("Differential equations")
        mathematical_thought.set_dimensional_coordinates([0.7, 0.9, 0.6])
        self.test_chain.add_thought(mathematical_thought)

        # Transform to physics domain
        let transformed_chain = self.thought_processing_service.transform_across_domains(
            self.test_chain,
            self.source_domain,
            self.target_domain
        )

        # Verify transformation
        assert_true(transformed_chain is not None)
        assert_true(transformed_chain.get_thoughts().size() >= self.test_chain.get_thoughts().size())

        # Verify semantic preservation
        let semantic_preservation = self.thought_processing_service.calculate_semantic_preservation(
            self.test_chain,
            transformed_chain
        )
        assert_true(semantic_preservation > 0.7)

    fn test_error_handling_and_recovery(self):
        # Create invalid thought
        var invalid_thought = Thought(None)
        self.test_chain.add_thought(invalid_thought)

        # Process chain with invalid thought
        let processed_chain = self.thought_processing_service.process_chain(self.test_chain)

        # Verify error handling
        assert_true(processed_chain is not None)
        assert_true(self.metacognitive_monitor.get_processing_errors().size() > 0)

        # Verify recovery
        assert_true(processed_chain.is_valid())
        assert_false(processed_chain.get_thoughts().contains(invalid_thought))

fn main():
    # Create test instance
    var test = ThoughtChainIntegrationTest()
    
    # Run tests
    test.test_complete_thought_chain_processing()
    test.test_cross_domain_transformation()
    test.test_error_handling_and_recovery()
    
    print("All integration tests passed!") 