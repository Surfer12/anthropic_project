from tensor import Tensor
from utils.vector import DynamicVector
from cognitive.dimensional_thought_space import DimensionalThoughtSpace, ThoughtVector
from tests.test_utils import TestSuite, TestResult, generate_test_tensor, compare_tensors
from math import sqrt, exp

struct DimensionalThoughtSpaceTests:
    var suite: TestSuite
    var thought_space: DimensionalThoughtSpace
    
    fn __init__(inout self):
        self.suite = TestSuite("DimensionalThoughtSpace Tests")
        self.thought_space = DimensionalThoughtSpace(128)  # 128-dimensional space
    
    fn run_all_tests(self) raises:
        self.test_thought_creation()
        self.test_thought_addition()
        self.test_similarity_search()
        self.test_traversal()
        self.test_semantic_relations()
        self.suite.print_summary()
    
    fn test_thought_creation(self):
        # Test vector creation
        let vector = generate_test_tensor(128, "random")
        var thought = ThoughtVector(
            "test-thought",
            vector,
            DynamicVector[String]()
        )
        
        # Verify thought properties
        var result = TestResult(
            "Thought Creation",
            thought.id == "test-thought" and
            len(thought.vector) == 128
        )
        self.suite.add_result(result)
    
    fn test_thought_addition(self) raises:
        # Create test thoughts
        for i in range(5):
            let vector = generate_test_tensor(128, "random")
            var thought = ThoughtVector(
                f"thought-{i}",
                vector,
                DynamicVector[String]()
            )
            self.thought_space.add_thought(thought)
        
        # Verify thought space size
        var result = TestResult(
            "Thought Addition",
            len(self.thought_space.thought_vectors) == 5
        )
        self.suite.add_result(result)
    
    fn test_similarity_search(self) raises:
        # Create test thoughts with known patterns
        var base_vector = generate_test_tensor(128, "constant")  # All 1's
        var similar_vector = generate_test_tensor(128, "constant")  # All 1's
        var different_vector = generate_test_tensor(128, "alternating")  # 0's and 1's
        
        var base_thought = ThoughtVector("base", base_vector, DynamicVector[String]())
        var similar_thought = ThoughtVector("similar", similar_vector, DynamicVector[String]())
        var different_thought = ThoughtVector("different", different_vector, DynamicVector[String]())
        
        self.thought_space.add_thought(base_thought)
        self.thought_space.add_thought(similar_thought)
        self.thought_space.add_thought(different_thought)
        
        # Search for similar thoughts
        let similar_matches = self.thought_space.find_similar_thoughts(base_thought, 0.9)
        let different_matches = self.thought_space.find_similar_thoughts(different_thought, 0.9)
        
        # Verify search results
        var result = TestResult(
            "Similarity Search",
            len(similar_matches) == 2 and  # Should find base and similar
            len(different_matches) == 1     # Should only find itself
        )
        self.suite.add_result(result)
    
    fn test_traversal(self) raises:
        # Create a chain of thoughts
        var thoughts = DynamicVector[ThoughtVector]()
        for i in range(5):
            let vector = generate_test_tensor(128, "sequential")
            var thought = ThoughtVector(
                f"chain-{i}",
                vector,
                DynamicVector[String]()
            )
            thoughts.append(thought)
            self.thought_space.add_thought(thought)
        
        # Create importance function
        fn importance(t: ThoughtVector) -> Float32:
            return 1.0  # Equal importance for testing
        
        # Traverse thought space
        let path = self.thought_space.traverse_thought_space(thoughts[0], importance)
        
        # Verify traversal
        var result = TestResult(
            "Thought Space Traversal",
            len(path) == 5  # Should visit all thoughts
        )
        self.suite.add_result(result)
    
    fn test_semantic_relations(self) raises:
        # Create related thoughts
        var thought1_vector = generate_test_tensor(128, "constant")  # All 1's
        var thought2_vector = generate_test_tensor(128, "constant")  # All 1's
        var thought3_vector = generate_test_tensor(128, "alternating")  # Different pattern
        
        var thought1 = ThoughtVector("related1", thought1_vector, DynamicVector[String]())
        var thought2 = ThoughtVector("related2", thought2_vector, DynamicVector[String]())
        var thought3 = ThoughtVector("unrelated", thought3_vector, DynamicVector[String]())
        
        self.thought_space.add_thought(thought1)
        self.thought_space.add_thought(thought2)
        self.thought_space.add_thought(thought3)
        
        # Check relations
        let has_relation = self.thought_space._has_strong_relation(thought1, thought2)
        let no_relation = self.thought_space._has_strong_relation(thought1, thought3)
        
        var result = TestResult(
            "Semantic Relations",
            has_relation and not no_relation
        )
        self.suite.add_result(result)

fn main() raises:
    # Run all tests
    var tests = DimensionalThoughtSpaceTests()
    tests.run_all_tests() 