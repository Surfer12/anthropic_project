from benchmark import Benchmark
from tensor import Tensor
from random import random_float32
from time import now
from math import sqrt, exp

struct ProblemGenerator:
    fn generate_simple_problem() -> Tuple[Tensor[DType.float32], DynamicVector[String]]:
        var vector = Tensor[DType.float32](128)
        for i in range(128):
            vector[i] = random_float32()
        
        var constraints = DynamicVector[String]()
        constraints.append("memory < 1GB")
        constraints.append("latency < 100ms")
        
        return (vector, constraints)
    
    fn generate_complex_problem() -> Tuple[Tensor[DType.float32], DynamicVector[String]]:
        var vector = Tensor[DType.float32](128)
        for i in range(128):
            vector[i] = random_float32()
        
        var constraints = DynamicVector[String]()
        constraints.append("CPU usage < 60%")
        constraints.append("memory < 2GB")
        constraints.append("network latency < 50ms")
        constraints.append("disk I/O < 1000 IOPS")
        
        return (vector, constraints)

struct PerformanceBenchmark:
    var thought_space: DimensionalThoughtSpace
    var monitor: MetaCognitiveMonitor
    var exporter: ArtifactExporter
    
    fn __init__(inout self):
        self.thought_space = DimensionalThoughtSpace(128)
        self.monitor = MetaCognitiveMonitor()
        self.exporter = ArtifactExporter()
    
    fn benchmark_thought_addition(self) -> Float64:
        let start_time = now()
        
        # Generate and add thoughts
        for i in range(1000):
            let (vector, constraints) = ProblemGenerator.generate_simple_problem()
            let thought = ThoughtVector(
                "thought-" + String(i),
                vector,
                constraints,
                DynamicVector[String]()
            )
            self.thought_space.add_thought(thought)
        
        return Float64(now() - start_time) / 1_000_000.0  # Convert to milliseconds
    
    fn benchmark_similarity_search(self) -> Float64:
        # First populate thought space
        for i in range(100):
            let (vector, constraints) = ProblemGenerator.generate_simple_problem()
            let thought = ThoughtVector(
                "thought-" + String(i),
                vector,
                constraints,
                DynamicVector[String]()
            )
            self.thought_space.add_thought(thought)
        
        let start_time = now()
        
        # Perform similarity searches
        for i in range(1000):
            let (query_vector, _) = ProblemGenerator.generate_simple_problem()
            let query = ThoughtVector(
                "query",
                query_vector,
                DynamicVector[String](),
                DynamicVector[String]()
            )
            _ = self.thought_space.find_similar_thought(query, 0.8)
        
        return Float64(now() - start_time) / 1_000_000.0  # Convert to milliseconds
    
    fn benchmark_traversal(self) -> Float64:
        # First populate thought space
        for i in range(100):
            let (vector, constraints) = ProblemGenerator.generate_complex_problem()
            let thought = ThoughtVector(
                "thought-" + String(i),
                vector,
                constraints,
                DynamicVector[String]()
            )
            self.thought_space.add_thought(thought)
        
        let start_time = now()
        
        # Perform traversals
        for i in range(100):
            let start_thought = self.thought_space.thought_vectors[0]
            let importance_fn = fn(t: ThoughtVector) -> Float32:
                return exp(-Float32(i) * 0.1)  # Simple decay function
            
            _ = self.thought_space.traverse_thought_space(start_thought, importance_fn)
        
        return Float64(now() - start_time) / 1_000_000.0  # Convert to milliseconds
    
    fn benchmark_artifact_export(self) -> Float64:
        # Generate test data
        var thoughts = DynamicVector[ThoughtVector]()
        for i in range(1000):
            let (vector, constraints) = ProblemGenerator.generate_complex_problem()
            let thought = ThoughtVector(
                "thought-" + String(i),
                vector,
                constraints,
                DynamicVector[String]()
            )
            thoughts.append(thought)
        
        let start_time = now()
        
        # Export artifacts
        var context = DynamicVector[Tuple[String, String]]()
        context.append(("attention_duration", "400"))
        
        for thought in thoughts:
            self.exporter.export_thought(thought, context)
        
        return Float64(now() - start_time) / 1_000_000.0  # Convert to milliseconds

fn main():
    print("Running CCT Framework Performance Benchmarks")
    print("-------------------------------------------")
    
    var benchmark = PerformanceBenchmark()
    
    # Thought Addition Benchmark
    print("Thought Addition (1000 thoughts):")
    let addition_time = benchmark.benchmark_thought_addition()
    print(f"  Average time: {addition_time:.2f}ms")
    print(f"  Throughput: {1000.0 / addition_time:.2f} thoughts/second")
    print()
    
    # Similarity Search Benchmark
    print("Similarity Search (1000 queries):")
    let search_time = benchmark.benchmark_similarity_search()
    print(f"  Average time: {search_time:.2f}ms")
    print(f"  Throughput: {1000.0 / search_time:.2f} queries/second")
    print()
    
    # Traversal Benchmark
    print("Thought Space Traversal (100 traversals):")
    let traversal_time = benchmark.benchmark_traversal()
    print(f"  Average time: {traversal_time:.2f}ms")
    print(f"  Throughput: {100.0 / traversal_time:.2f} traversals/second")
    print()
    
    # Artifact Export Benchmark
    print("Artifact Export (1000 artifacts):")
    let export_time = benchmark.benchmark_artifact_export()
    print(f"  Average time: {export_time:.2f}ms")
    print(f"  Throughput: {1000.0 / export_time:.2f} exports/second")
    print() 