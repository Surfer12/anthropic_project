# Advanced Metal compute kernels for M4 Max GPU
let ADVANCED_METAL_KERNELS = """
#include <metal_stdlib>
using namespace metal;

// Matrix multiplication optimized for M4 Max
kernel void matrix_multiply(
    device const float* matrix1 [[buffer(0)]],
    device const float* matrix2 [[buffer(1)]],
    device float* result [[buffer(2)]],
    device const uint& M [[buffer(3)]],
    device const uint& N [[buffer(4)]],
    device const uint& K [[buffer(5)]],
    uint2 thread_pos [[thread_position_in_grid]],
    uint2 thread_groups [[threadgroups_per_grid]]
) {
    const uint row = thread_pos.x;
    const uint col = thread_pos.y;
    
    if (row >= M || col >= N) return;
    
    // Tile size optimization for M4 Max cache
    const int TILE_SIZE = 32;
    float sum = 0.0f;
    
    for (uint t = 0; t < K; t += TILE_SIZE) {
        // Load tile into shared memory
        threadgroup float tile1[TILE_SIZE][TILE_SIZE];
        threadgroup float tile2[TILE_SIZE][TILE_SIZE];
        
        for (uint i = 0; i < TILE_SIZE; i++) {
            if (row < M && (t + i) < K)
                tile1[thread_pos.x][i] = matrix1[row * K + t + i];
            if (col < N && (t + i) < K)
                tile2[i][thread_pos.y] = matrix2[(t + i) * N + col];
        }
        
        threadgroup_barrier(mem_flags::mem_threadgroup);
        
        for (uint i = 0; i < TILE_SIZE; i++) {
            if ((t + i) < K)
                sum += tile1[thread_pos.x][i] * tile2[i][thread_pos.y];
        }
        
        threadgroup_barrier(mem_flags::mem_threadgroup);
    }
    
    result[row * N + col] = sum;
}

// Optimized batch vector quantization
kernel void vector_quantize(
    device const float* vectors [[buffer(0)]],
    device float* centroids [[buffer(1)]],
    device uint* assignments [[buffer(2)]],
    device const uint& num_vectors [[buffer(3)]],
    device const uint& vector_dim [[buffer(4)]],
    device const uint& num_centroids [[buffer(5)]],
    uint vector_idx [[thread_position_in_grid]]
) {
    if (vector_idx >= num_vectors) return;
    
    float min_distance = INFINITY;
    uint best_centroid = 0;
    
    // Vector start in memory
    const uint vector_start = vector_idx * vector_dim;
    
    // Find nearest centroid
    for (uint c = 0; c < num_centroids; c++) {
        float distance = 0.0f;
        
        // Compute distance using SIMD
        for (uint d = 0; d < vector_dim; d += 4) {
            float4 vec = float4(
                d + 0 < vector_dim ? vectors[vector_start + d + 0] : 0,
                d + 1 < vector_dim ? vectors[vector_start + d + 1] : 0,
                d + 2 < vector_dim ? vectors[vector_start + d + 2] : 0,
                d + 3 < vector_dim ? vectors[vector_start + d + 3] : 0
            );
            
            float4 cent = float4(
                d + 0 < vector_dim ? centroids[c * vector_dim + d + 0] : 0,
                d + 1 < vector_dim ? centroids[c * vector_dim + d + 1] : 0,
                d + 2 < vector_dim ? centroids[c * vector_dim + d + 2] : 0,
                d + 3 < vector_dim ? centroids[c * vector_dim + d + 3] : 0
            );
            
            float4 diff = vec - cent;
            distance += dot(diff, diff);
        }
        
        if (distance < min_distance) {
            min_distance = distance;
            best_centroid = c;
        }
    }
    
    assignments[vector_idx] = best_centroid;
}

// Optimized KNN search using shared memory
kernel void knn_search(
    device const float* vectors [[buffer(0)]],
    device const float* query [[buffer(1)]],
    device uint* indices [[buffer(2)]],
    device float* distances [[buffer(3)]],
    device const uint& num_vectors [[buffer(4)]],
    device const uint& vector_dim [[buffer(5)]],
    device const uint& k [[buffer(6)]],
    threadgroup float* shared_distances [[threadgroup(0)]],
    threadgroup uint* shared_indices [[threadgroup(1)]],
    uint thread_idx [[thread_position_in_grid]],
    uint thread_per_group [[threads_per_threadgroup]]
) {
    const uint BLOCK_SIZE = thread_per_group;
    
    // Initialize local top-k
    for (uint i = 0; i < k; i++) {
        shared_distances[thread_idx * k + i] = INFINITY;
        shared_indices[thread_idx * k + i] = UINT_MAX;
    }
    
    // Process vectors in blocks
    for (uint block_start = 0; block_start < num_vectors; block_start += BLOCK_SIZE) {
        uint vec_idx = block_start + thread_idx;
        if (vec_idx >= num_vectors) continue;
        
        // Compute distance using SIMD
        float distance = 0.0f;
        for (uint d = 0; d < vector_dim; d += 4) {
            float4 vec = float4(
                d + 0 < vector_dim ? vectors[vec_idx * vector_dim + d + 0] : 0,
                d + 1 < vector_dim ? vectors[vec_idx * vector_dim + d + 1] : 0,
                d + 2 < vector_dim ? vectors[vec_idx * vector_dim + d + 2] : 0,
                d + 3 < vector_dim ? vectors[vec_idx * vector_dim + d + 3] : 0
            );
            
            float4 q = float4(
                d + 0 < vector_dim ? query[d + 0] : 0,
                d + 1 < vector_dim ? query[d + 1] : 0,
                d + 2 < vector_dim ? query[d + 2] : 0,
                d + 3 < vector_dim ? query[d + 3] : 0
            );
            
            float4 diff = vec - q;
            distance += dot(diff, diff);
        }
        
        // Update local top-k
        for (uint i = 0; i < k; i++) {
            if (distance < shared_distances[thread_idx * k + i]) {
                // Shift existing entries
                for (uint j = k - 1; j > i; j--) {
                    shared_distances[thread_idx * k + j] = shared_distances[thread_idx * k + j - 1];
                    shared_indices[thread_idx * k + j] = shared_indices[thread_idx * k + j - 1];
                }
                shared_distances[thread_idx * k + i] = distance;
                shared_indices[thread_idx * k + i] = vec_idx;
                break;
            }
        }
    }
    
    threadgroup_barrier(mem_flags::mem_threadgroup);
    
    // Merge results from all threads
    if (thread_idx == 0) {
        for (uint i = 0; i < k; i++) {
            float min_dist = INFINITY;
            uint min_idx = UINT_MAX;
            uint min_thread = UINT_MAX;
            
            for (uint t = 0; t < thread_per_group; t++) {
                if (shared_distances[t * k + i] < min_dist) {
                    min_dist = shared_distances[t * k + i];
                    min_idx = shared_indices[t * k + i];
                    min_thread = t;
                }
            }
            
            distances[i] = min_dist;
            indices[i] = min_idx;
        }
    }
}

// Optimized cosine similarity with tensor cores
kernel void cosine_similarity_batch(
    device const float* vectors [[buffer(0)]],
    device const float* query [[buffer(1)]],
    device float* similarities [[buffer(2)]],
    device const uint& vector_dim [[buffer(3)]],
    device const uint& num_vectors [[buffer(4)]],
    threadgroup float* shared_mem [[threadgroup(0)]],
    uint2 thread_pos [[thread_position_in_grid]],
    uint2 thread_groups [[threadgroups_per_grid]]
) {
    const uint vector_idx = thread_pos.x;
    const uint local_idx = thread_pos.y;
    const uint group_size = thread_groups.y;
    
    if (vector_idx >= num_vectors) return;
    
    // Compute partial dot products using SIMD
    float dot_product = 0.0f;
    float vec_norm = 0.0f;
    float query_norm = 0.0f;
    
    for (uint d = local_idx; d < vector_dim; d += group_size) {
        float vec_val = vectors[vector_idx * vector_dim + d];
        float query_val = query[d];
        
        dot_product += vec_val * query_val;
        vec_norm += vec_val * vec_val;
        query_norm += query_val * query_val;
    }
    
    // Store partial results in shared memory
    shared_mem[local_idx * 3 + 0] = dot_product;
    shared_mem[local_idx * 3 + 1] = vec_norm;
    shared_mem[local_idx * 3 + 2] = query_norm;
    
    threadgroup_barrier(mem_flags::mem_threadgroup);
    
    // Reduce partial results
    if (local_idx == 0) {
        float final_dot = 0.0f;
        float final_vec_norm = 0.0f;
        float final_query_norm = 0.0f;
        
        for (uint i = 0; i < group_size; i++) {
            final_dot += shared_mem[i * 3 + 0];
            final_vec_norm += shared_mem[i * 3 + 1];
            final_query_norm += shared_mem[i * 3 + 2];
        }
        
        similarities[vector_idx] = final_dot / (sqrt(final_vec_norm) * sqrt(final_query_norm));
    }
}
""" 