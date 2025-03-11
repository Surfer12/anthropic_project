from tensor import Tensor
from utils.vector import DynamicVector
from accelerator.metal_optimizer import MetalOptimizer
from accelerator.memory_pool import MemoryPool
from tests.test_utils import TestSuite, TestResult, generate_test_tensor, generate_test_matrix
from tests.test_utils import compare_tensors, compare_matrices, benchmark_operation
from metal import MetalDevice
from math import sqrt, exp

struct MetalOptimizerTests:
    var suite: TestSuite
    var device: MetalDevice
    var optimizer: MetalOptimizer
    var memory_pool: MemoryPool
    
    fn __init__(inout self):
        self.suite = TestSuite("Metal Optimizer Tests")
        self.device = MetalDevice()
        self.memory_pool = MemoryPool(self.device)
        self.optimizer = MetalOptimizer(self.device)
    
    fn run_all_tests(self) raises:
        self.test_matrix_multiply()
        self.test_vector_quantization()
        self.test_knn_search()
        self.test_cosine_similarity()
        self.test_memory_pool()
        self.suite.print_summary()
    
    fn test_matrix_multiply(self) raises:
        # Create test matrices
        let M = 128
        let K = 256
        let N = 128
        
        let matrix1 = generate_test_matrix(M, K, "random")
        let matrix2 = generate_test_matrix(K, N, "random")
        
        # CPU implementation for comparison
        fn cpu_matrix_multiply() raises -> Tensor[DType.float32]:
            var result = Tensor[DType.float32](M, N)
            for i in range(M):
                for j in range(N):
                    var sum: Float32 = 0.0
                    for k in range(K):
                        sum += matrix1[i, k] * matrix2[k, j]
                    result[i, j] = sum
            return result
        
        # Run CPU version
        let cpu_time = benchmark_operation(cpu_matrix_multiply)
        let cpu_result = cpu_matrix_multiply()
        
        # Run GPU version
        fn gpu_matrix_multiply() raises -> None:
            _ = self.optimizer.matrix_multiply(matrix1, matrix2)
        
        let gpu_time = benchmark_operation(gpu_matrix_multiply)
        let gpu_result = self.optimizer.matrix_multiply(matrix1, matrix2)
        
        # Verify results
        let accuracy_result = verify_gpu_results(cpu_result, gpu_result)
        self.suite.add_result(accuracy_result)
        
        # Verify performance
        let performance_result = verify_performance_improvement(cpu_time, gpu_time)
        self.suite.add_result(performance_result)
    
    fn test_vector_quantization(self) raises:
        # Create test data
        let num_vectors = 1000
        let vector_dim = 128
        let num_centroids = 16
        
        let vectors = generate_test_matrix(num_vectors, vector_dim, "random")
        let centroids = generate_test_matrix(num_centroids, vector_dim, "random")
        
        # Run GPU version
        fn gpu_quantize() raises -> None:
            _ = self.optimizer.vector_quantize(vectors, centroids)
        
        let gpu_time = benchmark_operation(gpu_quantize)
        let assignments = self.optimizer.vector_quantize(vectors, centroids)
        
        # Verify results
        var result = TestResult(
            "Vector Quantization",
            len(assignments) == num_vectors and
            all(a < num_centroids for a in assignments)
        )
        self.suite.add_result(result)
    
    fn test_knn_search(self) raises:
        # Create test data
        let num_vectors = 1000
        let vector_dim = 128
        let k = 5
        
        let vectors = generate_test_matrix(num_vectors, vector_dim, "random")
        let query = generate_test_tensor(vector_dim, "random")
        
        # Run GPU version
        fn gpu_knn() raises -> None:
            _ = self.optimizer.knn_search(vectors, query, k)
        
        let gpu_time = benchmark_operation(gpu_knn)
        let (indices, distances) = self.optimizer.knn_search(vectors, query, k)
        
        # Verify results
        var result = TestResult(
            "KNN Search",
            len(indices) == k and
            len(distances) == k and
            all(i < num_vectors for i in indices) and
            all(d >= 0.0 for d in distances)
        )
        self.suite.add_result(result)
    
    fn test_cosine_similarity(self) raises:
        # Create test data
        let num_vectors = 1000
        let vector_dim = 128
        
        let vectors = generate_test_matrix(num_vectors, vector_dim, "random")
        let query = generate_test_tensor(vector_dim, "random")
        
        # Run GPU version
        fn gpu_cosine() raises -> None:
            _ = self.optimizer.cosine_similarity_batch(vectors, query)
        
        let gpu_time = benchmark_operation(gpu_cosine)
        let similarities = self.optimizer.cosine_similarity_batch(vectors, query)
        
        # Verify results
        var result = TestResult(
            "Cosine Similarity",
            len(similarities) == num_vectors and
            all(-1.0 <= s <= 1.0 for s in similarities)
        )
        self.suite.add_result(result)
    
    fn test_memory_pool(self) raises:
        # Test buffer allocation
        let buffer_size = 1024 * 1024  # 1MB
        var buffers = DynamicVector[MetalBuffer]()
        
        # Allocate multiple buffers
        for i in range(10):
            let buffer = self.memory_pool.allocate(buffer_size)
            buffers.append(buffer)
        
        # Verify allocations
        var allocation_result = TestResult(
            "Buffer Allocation",
            len(buffers) == 10
        )
        self.suite.add_result(allocation_result)
        
        # Deallocate some buffers
        for i in range(5):
            self.memory_pool.deallocate(buffers[i].id)
        
        # Verify pool stats
        let stats = self.memory_pool.get_stats()
        var stats_result = TestResult(
            "Memory Pool Stats",
            stats.num_active_blocks == 5 and
            stats.fragmentation < 0.5  # Less than 50% fragmentation
        )
        self.suite.add_result(stats_result)

fn main() raises:
    # Run all tests
    var tests = MetalOptimizerTests()
    tests.run_all_tests() 