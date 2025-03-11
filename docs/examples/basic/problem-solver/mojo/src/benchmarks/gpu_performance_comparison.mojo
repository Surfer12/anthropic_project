from benchmark import Benchmark
from tensor import Tensor
from random import random_float32
from time import now
from math import sqrt, exp
from cognitive.dimensional_thought_space import DimensionalThoughtSpace, ThoughtVector
from utils.parallel import ParallelConfig
from accelerator.metal_compute import MetalAccelerator

struct GPUBenchmark:
    var cpu_thought_space: DimensionalThoughtSpace
    var gpu_thought_space: DimensionalThoughtSpace
    var vector_dim: Int
    var num_vectors: Int
    
    fn __init__(inout self, vector_dim: Int = 128, num_vectors: Int = 10000):
        self.vector_dim = vector_dim
        self.num_vectors = num_vectors
        self.cpu_thought_space = DimensionalThoughtSpace(vector_dim, use_gpu=False)
        self.gpu_thought_space = DimensionalThoughtSpace(vector_dim, use_gpu=True)
        self._populate_thought_spaces()
    
    fn _populate_thought_spaces(self):
        for i in range(self.num_vectors):
            let vector = self._generate_random_vector()
            let cpu_thought = ThoughtVector(
                "thought-" + String(i),
                vector.copy(),
                DynamicVector[String]()
            )
            let gpu_thought = ThoughtVector(
                "thought-" + String(i),
                vector,
                DynamicVector[String]()
            )
            self.cpu_thought_space.add_thought(cpu_thought)
            self.gpu_thought_space.add_thought(gpu_thought)
    
    fn _generate_random_vector(self) -> Tensor[DType.float32]:
        var vector = Tensor[DType.float32](self.vector_dim)
        for i in range(self.vector_dim):
            vector[i] = random_float32()
        return vector
    
    fn benchmark_vector_operations(self) -> Tuple[Float64, Float64]:
        var cpu_time: Float64 = 0
        var gpu_time: Float64 = 0
        let num_trials = 100
        
        # Generate test vectors
        var test_vectors = DynamicVector[Tensor[DType.float32]]()
        for i in range(num_trials):
            test_vectors.append(self._generate_random_vector())
        
        # CPU benchmark
        let cpu_start = now()
        for vector in test_vectors:
            let thought = ThoughtVector(
                "test",
                vector,
                DynamicVector[String]()
            )
            self.cpu_thought_space.add_thought(thought)
        cpu_time = Float64(now() - cpu_start) / 1_000_000.0
        
        # GPU benchmark
        let gpu_start = now()
        for vector in test_vectors:
            let thought = ThoughtVector(
                "test",
                vector,
                DynamicVector[String]()
            )
            self.gpu_thought_space.add_thought(thought)
        gpu_time = Float64(now() - gpu_start) / 1_000_000.0
        
        return (cpu_time, gpu_time)
    
    fn benchmark_similarity_search(self) -> Tuple[Float64, Float64]:
        var cpu_time: Float64 = 0
        var gpu_time: Float64 = 0
        let num_trials = 100
        
        # Generate query vectors
        var query_vectors = DynamicVector[Tensor[DType.float32]]()
        for i in range(num_trials):
            query_vectors.append(self._generate_random_vector())
        
        # CPU benchmark
        let cpu_start = now()
        for vector in query_vectors:
            let query = ThoughtVector(
                "query",
                vector,
                DynamicVector[String]()
            )
            _ = self.cpu_thought_space.find_similar_thoughts(query, 0.5)
        cpu_time = Float64(now() - cpu_start) / 1_000_000.0
        
        # GPU benchmark
        let gpu_start = now()
        for vector in query_vectors:
            let query = ThoughtVector(
                "query",
                vector,
                DynamicVector[String]()
            )
            _ = self.gpu_thought_space.find_similar_thoughts(query, 0.5)
        gpu_time = Float64(now() - gpu_start) / 1_000_000.0
        
        return (cpu_time, gpu_time)

fn main():
    print("Running GPU Acceleration Benchmarks")
    print("----------------------------------")
    
    # Test different vector dimensions
    let dimensions = [128, 256, 512, 1024]
    let num_vectors = 10000
    
    for dim in dimensions:
        print(f"\nVector Dimension: {dim}")
        print("----------------------")
        
        var benchmark = GPUBenchmark(dim, num_vectors)
        
        # Vector operations benchmark
        let (cpu_vec_time, gpu_vec_time) = benchmark.benchmark_vector_operations()
        print("\nVector Operations (100 trials):")
        print(f"  CPU Time: {cpu_vec_time:.2f}ms")
        print(f"  GPU Time: {gpu_vec_time:.2f}ms")
        print(f"  Speedup: {cpu_vec_time / gpu_vec_time:.2f}x")
        
        # Similarity search benchmark
        let (cpu_search_time, gpu_search_time) = benchmark.benchmark_similarity_search()
        print("\nSimilarity Search (100 trials):")
        print(f"  CPU Time: {cpu_search_time:.2f}ms")
        print(f"  GPU Time: {gpu_search_time:.2f}ms")
        print(f"  Speedup: {cpu_search_time / gpu_search_time:.2f}x")
        
        # Memory usage comparison
        print("\nMemory Usage:")
        print("  CPU: Standard memory allocation")
        print("  GPU: Unified memory with Metal")
        
        # Hardware utilization
        print("\nHardware Utilization:")
        print("  CPU: Multi-threaded with SIMD")
        print("  GPU: M4 Max GPU cores with Metal compute") 