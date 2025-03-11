from tensor import Tensor
from metal import MetalDevice, MetalBuffer, MetalCompute
from math import min, max

struct MetalConfig:
    var device: MetalDevice
    var max_buffer_size: Int
    var workgroup_size: Int
    
    fn __init__(inout self, max_buffer_size: Int = 1024 * 1024, workgroup_size: Int = 256):
        self.device = MetalDevice()
        self.max_buffer_size = max_buffer_size
        self.workgroup_size = workgroup_size

# Metal shader code for vector operations
let METAL_SHADERS = """
#include <metal_stdlib>
using namespace metal;

kernel void vector_dot_product(
    device const float* v1 [[buffer(0)]],
    device const float* v2 [[buffer(1)]],
    device float* result [[buffer(2)]],
    device const uint& length [[buffer(3)]],
    uint idx [[thread_position_in_grid]]
) {
    if (idx >= length) return;
    
    result[idx] = v1[idx] * v2[idx];
}

kernel void vector_normalize(
    device const float* input [[buffer(0)]],
    device float* output [[buffer(1)]],
    device const float& norm [[buffer(2)]],
    device const uint& length [[buffer(3)]],
    uint idx [[thread_position_in_grid]]
) {
    if (idx >= length) return;
    
    output[idx] = input[idx] / norm;
}

kernel void vector_similarity_batch(
    device const float* vectors [[buffer(0)]],
    device const float* query [[buffer(1)]],
    device float* similarities [[buffer(2)]],
    device const uint& vector_dim [[buffer(3)]],
    device const uint& num_vectors [[buffer(4)]],
    uint2 idx [[thread_position_in_grid]]
) {
    uint vector_idx = idx.x;
    uint dim_idx = idx.y;
    
    if (vector_idx >= num_vectors || dim_idx >= vector_dim) return;
    
    uint offset = vector_idx * vector_dim + dim_idx;
    similarities[vector_idx] += vectors[offset] * query[dim_idx];
}
"""

@value
struct MetalAccelerator:
    var config: MetalConfig
    var compute: MetalCompute
    
    fn __init__(inout self):
        self.config = MetalConfig()
        self.compute = MetalCompute(self.config.device, METAL_SHADERS)
    
    fn dot_product[dtype: DType](
        self,
        v1: Tensor[dtype],
        v2: Tensor[dtype]
    ) raises -> Float32:
        let size = len(v1)
        let buffer_size = size * sizeof[dtype]()
        
        # Create Metal buffers
        let v1_buffer = self.config.device.buffer_from_memory(v1.data, buffer_size)
        let v2_buffer = self.config.device.buffer_from_memory(v2.data, buffer_size)
        let result_buffer = self.config.device.create_buffer(buffer_size)
        let length_buffer = self.config.device.buffer_from_value(size)
        
        # Configure compute pipeline
        let pipeline = self.compute.make_pipeline("vector_dot_product")
        let command = self.compute.make_command()
        
        # Set compute parameters
        let grid_size = (size + self.config.workgroup_size - 1) // self.config.workgroup_size
        command.set_buffer(v1_buffer, 0)
        command.set_buffer(v2_buffer, 1)
        command.set_buffer(result_buffer, 2)
        command.set_buffer(length_buffer, 3)
        
        # Execute compute
        command.dispatch_1d(grid_size * self.config.workgroup_size, self.config.workgroup_size)
        command.wait()
        
        # Reduce results
        var total: Float32 = 0.0
        let result_ptr = Pointer[dtype](result_buffer.contents())
        for i in range(size):
            total += Float32(result_ptr[i])
        
        return total
    
    fn normalize[dtype: DType](
        self,
        vector: Tensor[dtype]
    ) raises -> Tensor[dtype]:
        let size = len(vector)
        let buffer_size = size * sizeof[dtype]()
        
        # Calculate norm using dot product
        let norm = sqrt(self.dot_product(vector, vector))
        
        # Create Metal buffers
        let input_buffer = self.config.device.buffer_from_memory(vector.data, buffer_size)
        let output_buffer = self.config.device.create_buffer(buffer_size)
        let norm_buffer = self.config.device.buffer_from_value(norm)
        let length_buffer = self.config.device.buffer_from_value(size)
        
        # Configure compute pipeline
        let pipeline = self.compute.make_pipeline("vector_normalize")
        let command = self.compute.make_command()
        
        # Set compute parameters
        let grid_size = (size + self.config.workgroup_size - 1) // self.config.workgroup_size
        command.set_buffer(input_buffer, 0)
        command.set_buffer(output_buffer, 1)
        command.set_buffer(norm_buffer, 2)
        command.set_buffer(length_buffer, 3)
        
        # Execute compute
        command.dispatch_1d(grid_size * self.config.workgroup_size, self.config.workgroup_size)
        command.wait()
        
        # Create result tensor
        var result = Tensor[dtype](size)
        result.data.copy_from(Pointer[dtype](output_buffer.contents()), size)
        return result
    
    fn batch_similarity[dtype: DType](
        self,
        vectors: DynamicVector[Tensor[dtype]],
        query: Tensor[dtype]
    ) raises -> DynamicVector[Float32]:
        let num_vectors = len(vectors)
        let vector_dim = len(query)
        let vectors_buffer_size = num_vectors * vector_dim * sizeof[dtype]()
        let query_buffer_size = vector_dim * sizeof[dtype]()
        let similarities_buffer_size = num_vectors * sizeof[Float32]()
        
        # Create flattened vectors buffer
        var vectors_data = Pointer[dtype].alloc(num_vectors * vector_dim)
        for i in range(num_vectors):
            vectors_data.offset(i * vector_dim).copy_from(vectors[i].data, vector_dim)
        
        # Create Metal buffers
        let vectors_buffer = self.config.device.buffer_from_memory(vectors_data, vectors_buffer_size)
        let query_buffer = self.config.device.buffer_from_memory(query.data, query_buffer_size)
        let similarities_buffer = self.config.device.create_buffer(similarities_buffer_size)
        let vector_dim_buffer = self.config.device.buffer_from_value(vector_dim)
        let num_vectors_buffer = self.config.device.buffer_from_value(num_vectors)
        
        # Configure compute pipeline
        let pipeline = self.compute.make_pipeline("vector_similarity_batch")
        let command = self.compute.make_command()
        
        # Set compute parameters
        let grid_size_x = (num_vectors + 31) // 32
        let grid_size_y = (vector_dim + 31) // 32
        command.set_buffer(vectors_buffer, 0)
        command.set_buffer(query_buffer, 1)
        command.set_buffer(similarities_buffer, 2)
        command.set_buffer(vector_dim_buffer, 3)
        command.set_buffer(num_vectors_buffer, 4)
        
        # Execute compute
        command.dispatch_2d(
            grid_size_x * 32, grid_size_y * 32,
            32, 32
        )
        command.wait()
        
        # Create result vector
        var results = DynamicVector[Float32]()
        let similarities_ptr = Pointer[Float32](similarities_buffer.contents())
        for i in range(num_vectors):
            results.append(similarities_ptr[i])
        
        vectors_data.free()
        return results 