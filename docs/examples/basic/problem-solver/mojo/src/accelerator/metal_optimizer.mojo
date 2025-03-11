from tensor import Tensor
from metal import MetalDevice, MetalBuffer, MetalCompute
from math import sqrt, exp
from memory.unsafe import Pointer
from utils.vector import DynamicVector
from accelerator.metal_kernels import ADVANCED_METAL_KERNELS
from accelerator.memory_pool import MemoryPool
from profiler.gpu_profiler import GPUProfiler

@value
struct MetalOptimizer:
    var device: MetalDevice
    var compute: MetalCompute
    var workgroup_size: Int
    var max_buffer_size: Int
    var shared_memory_size: Int
    var memory_pool: MemoryPool
    var profiler: GPUProfiler
    
    fn __init__(inout self, 
                workgroup_size: Int = 256, 
                max_buffer_size: Int = 1024 * 1024,
                shared_memory_size: Int = 32 * 1024):
        self.device = MetalDevice()
        self.compute = MetalCompute(self.device, ADVANCED_METAL_KERNELS)
        self.workgroup_size = workgroup_size
        self.max_buffer_size = max_buffer_size
        self.shared_memory_size = shared_memory_size
        self.memory_pool = MemoryPool(self.device)
        self.profiler = GPUProfiler()
    
    fn matrix_multiply[dtype: DType](
        self,
        matrix1: Tensor[dtype],
        matrix2: Tensor[dtype]
    ) raises -> Tensor[dtype]:
        self.profiler.start_kernel("matrix_multiply")
        let bytes_processed = matrix1.size() * matrix2.size() * sizeof[dtype]()
        
        let M = matrix1.shape[0]
        let K = matrix1.shape[1]
        let N = matrix2.shape[1]
        
        # Create result tensor
        var result = Tensor[dtype](M, N)
        
        # Allocate buffers from pool
        let matrix1_buffer = self.memory_pool.allocate(M * K * sizeof[dtype]())
        let matrix2_buffer = self.memory_pool.allocate(K * N * sizeof[dtype]())
        let result_buffer = self.memory_pool.allocate(M * N * sizeof[dtype]())
        let M_buffer = self.memory_pool.allocate(sizeof[Int]())
        let N_buffer = self.memory_pool.allocate(sizeof[Int]())
        let K_buffer = self.memory_pool.allocate(sizeof[Int]())
        
        # Copy data to buffers
        matrix1_buffer.copy_from(matrix1.data, M * K * sizeof[dtype]())
        matrix2_buffer.copy_from(matrix2.data, K * N * sizeof[dtype]())
        M_buffer.copy_from(Pointer[Int](&M), sizeof[Int]())
        N_buffer.copy_from(Pointer[Int](&N), sizeof[Int]())
        K_buffer.copy_from(Pointer[Int](&K), sizeof[Int]())
        
        # Configure compute pipeline
        let pipeline = self.compute.make_pipeline("matrix_multiply")
        let command = self.compute.make_command()
        
        # Set compute parameters
        let grid_size_x = (M + 31) // 32
        let grid_size_y = (N + 31) // 32
        command.set_buffer(matrix1_buffer, 0)
        command.set_buffer(matrix2_buffer, 1)
        command.set_buffer(result_buffer, 2)
        command.set_buffer(M_buffer, 3)
        command.set_buffer(N_buffer, 4)
        command.set_buffer(K_buffer, 5)
        
        # Execute compute
        command.dispatch_2d(grid_size_x * 32, grid_size_y * 32, 32, 32)
        command.wait()
        
        # Copy result
        result.data.copy_from(Pointer[dtype](result_buffer.contents()), M * N)
        
        # Deallocate buffers
        self.memory_pool.deallocate(matrix1_buffer.id)
        self.memory_pool.deallocate(matrix2_buffer.id)
        self.memory_pool.deallocate(result_buffer.id)
        self.memory_pool.deallocate(M_buffer.id)
        self.memory_pool.deallocate(N_buffer.id)
        self.memory_pool.deallocate(K_buffer.id)
        
        self.profiler.end_kernel("matrix_multiply", bytes_processed)
        return result
    
    fn vector_quantize[dtype: DType](
        self,
        vectors: Tensor[dtype],
        centroids: Tensor[dtype]
    ) raises -> Tensor[Int]:
        let num_vectors = vectors.shape[0]
        let vector_dim = vectors.shape[1]
        let num_centroids = centroids.shape[0]
        
        # Create result tensor
        var assignments = Tensor[Int](num_vectors)
        
        # Create Metal buffers
        let vectors_buffer = self.device.buffer_from_memory(vectors.data, num_vectors * vector_dim * sizeof[dtype]())
        let centroids_buffer = self.device.buffer_from_memory(centroids.data, num_centroids * vector_dim * sizeof[dtype]())
        let assignments_buffer = self.device.create_buffer(num_vectors * sizeof[Int]())
        let num_vectors_buffer = self.device.buffer_from_value(num_vectors)
        let vector_dim_buffer = self.device.buffer_from_value(vector_dim)
        let num_centroids_buffer = self.device.buffer_from_value(num_centroids)
        
        # Configure compute pipeline
        let pipeline = self.compute.make_pipeline("vector_quantize")
        let command = self.compute.make_command()
        
        # Set compute parameters
        let grid_size = (num_vectors + self.workgroup_size - 1) // self.workgroup_size
        command.set_buffer(vectors_buffer, 0)
        command.set_buffer(centroids_buffer, 1)
        command.set_buffer(assignments_buffer, 2)
        command.set_buffer(num_vectors_buffer, 3)
        command.set_buffer(vector_dim_buffer, 4)
        command.set_buffer(num_centroids_buffer, 5)
        
        # Execute compute
        command.dispatch_1d(grid_size * self.workgroup_size, self.workgroup_size)
        command.wait()
        
        # Copy result
        assignments.data.copy_from(Pointer[Int](assignments_buffer.contents()), num_vectors)
        return assignments
    
    fn knn_search[dtype: DType](
        self,
        vectors: Tensor[dtype],
        query: Tensor[dtype],
        k: Int
    ) raises -> Tuple[Tensor[Int], Tensor[dtype]]:
        let num_vectors = vectors.shape[0]
        let vector_dim = vectors.shape[1]
        
        # Create result tensors
        var indices = Tensor[Int](k)
        var distances = Tensor[dtype](k)
        
        # Create Metal buffers
        let vectors_buffer = self.device.buffer_from_memory(vectors.data, num_vectors * vector_dim * sizeof[dtype]())
        let query_buffer = self.device.buffer_from_memory(query.data, vector_dim * sizeof[dtype]())
        let indices_buffer = self.device.create_buffer(k * sizeof[Int]())
        let distances_buffer = self.device.create_buffer(k * sizeof[dtype]())
        let num_vectors_buffer = self.device.buffer_from_value(num_vectors)
        let vector_dim_buffer = self.device.buffer_from_value(vector_dim)
        let k_buffer = self.device.buffer_from_value(k)
        
        # Allocate shared memory
        let shared_distances = self.device.create_buffer(self.shared_memory_size)
        let shared_indices = self.device.create_buffer(self.shared_memory_size)
        
        # Configure compute pipeline
        let pipeline = self.compute.make_pipeline("knn_search")
        let command = self.compute.make_command()
        
        # Set compute parameters
        let grid_size = (num_vectors + self.workgroup_size - 1) // self.workgroup_size
        command.set_buffer(vectors_buffer, 0)
        command.set_buffer(query_buffer, 1)
        command.set_buffer(indices_buffer, 2)
        command.set_buffer(distances_buffer, 3)
        command.set_buffer(num_vectors_buffer, 4)
        command.set_buffer(vector_dim_buffer, 5)
        command.set_buffer(k_buffer, 6)
        command.set_threadgroup_memory(shared_distances, 0)
        command.set_threadgroup_memory(shared_indices, 1)
        
        # Execute compute
        command.dispatch_1d(grid_size * self.workgroup_size, self.workgroup_size)
        command.wait()
        
        # Copy results
        indices.data.copy_from(Pointer[Int](indices_buffer.contents()), k)
        distances.data.copy_from(Pointer[dtype](distances_buffer.contents()), k)
        return (indices, distances)
    
    fn cosine_similarity_batch[dtype: DType](
        self,
        vectors: Tensor[dtype],
        query: Tensor[dtype]
    ) raises -> Tensor[dtype]:
        let num_vectors = vectors.shape[0]
        let vector_dim = vectors.shape[1]
        
        # Create result tensor
        var similarities = Tensor[dtype](num_vectors)
        
        # Create Metal buffers
        let vectors_buffer = self.device.buffer_from_memory(vectors.data, num_vectors * vector_dim * sizeof[dtype]())
        let query_buffer = self.device.buffer_from_memory(query.data, vector_dim * sizeof[dtype]())
        let similarities_buffer = self.device.create_buffer(num_vectors * sizeof[dtype]())
        let vector_dim_buffer = self.device.buffer_from_value(vector_dim)
        let num_vectors_buffer = self.device.buffer_from_value(num_vectors)
        
        # Allocate shared memory
        let shared_mem = self.device.create_buffer(self.shared_memory_size)
        
        # Configure compute pipeline
        let pipeline = self.compute.make_pipeline("cosine_similarity_batch")
        let command = self.compute.make_command()
        
        # Set compute parameters
        let grid_size_x = (num_vectors + 31) // 32
        let grid_size_y = (vector_dim + 31) // 32
        command.set_buffer(vectors_buffer, 0)
        command.set_buffer(query_buffer, 1)
        command.set_buffer(similarities_buffer, 2)
        command.set_buffer(vector_dim_buffer, 3)
        command.set_buffer(num_vectors_buffer, 4)
        command.set_threadgroup_memory(shared_mem, 0)
        
        # Execute compute
        command.dispatch_2d(grid_size_x * 32, grid_size_y * 32, 32, 32)
        command.wait()
        
        # Copy result
        similarities.data.copy_from(Pointer[dtype](similarities_buffer.contents()), num_vectors)
        return similarities 
    
    fn get_performance_stats(self) -> Tuple[DynamicVector[KernelStats], MemoryStats]:
        return (
            self.profiler.get_kernel_stats(),
            self.profiler.get_memory_stats()
        )
    
    fn reset_profiler(inout self):
        self.profiler.reset()
    
    fn enable_profiling(inout self):
        self.profiler.enable()
    
    fn disable_profiling(inout self):
        self.profiler.disable()
    
    fn get_memory_pool_stats(self) -> PerfStats:
        return self.memory_pool.get_stats() 