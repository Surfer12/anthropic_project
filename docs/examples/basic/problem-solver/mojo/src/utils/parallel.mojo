from tensor import Tensor
from algorithm import parallelize, vectorize
from math import min, max
from memory.unsafe import Pointer

struct ParallelConfig:
    var num_threads: Int
    var simd_width: Int
    var chunk_size: Int
    
    fn __init__(inout self, num_threads: Int = 4, simd_width: Int = 8, chunk_size: Int = 1024):
        self.num_threads = num_threads
        self.simd_width = simd_width
        self.chunk_size = chunk_size

@always_inline
fn parallel_simd_dot_product[dtype: DType](
    v1: Tensor[dtype], 
    v2: Tensor[dtype], 
    config: ParallelConfig
) -> SIMD[dtype, 1]:
    let size = len(v1)
    let simd_width = config.simd_width
    let chunks = size // (simd_width * config.chunk_size)
    var result = SIMD[dtype, 1](0)
    
    @parameter
    fn process_chunk(chunk_idx: Int):
        let start = chunk_idx * simd_width * config.chunk_size
        let end = min(start + simd_width * config.chunk_size, size)
        var chunk_result = SIMD[dtype, 1](0)
        
        for i in range(start, end, simd_width):
            let v1_simd = SIMD[dtype, 8](v1.data + i)
            let v2_simd = SIMD[dtype, 8](v2.data + i)
            chunk_result += (v1_simd * v2_simd).reduce_add()
        
        result += chunk_result
    
    parallelize[process_chunk](chunks, config.num_threads)
    return result

@always_inline
fn parallel_vector_normalize[dtype: DType](
    vector: Tensor[dtype],
    config: ParallelConfig
) raises -> Tensor[dtype]:
    let size = len(vector)
    var normalized = Tensor[dtype](size)
    let chunks = size // config.chunk_size
    var norm = SIMD[dtype, 1](0)
    
    # Calculate norm in parallel
    @parameter
    fn compute_norm_chunk(chunk_idx: Int):
        let start = chunk_idx * config.chunk_size
        let end = min(start + config.chunk_size, size)
        var chunk_norm = SIMD[dtype, 1](0)
        
        for i in range(start, end, config.simd_width):
            let vec_simd = SIMD[dtype, 8](vector.data + i)
            chunk_norm += (vec_simd * vec_simd).reduce_add()
        
        norm += chunk_norm
    
    parallelize[compute_norm_chunk](chunks, config.num_threads)
    let norm_value = sqrt(norm[0])
    
    # Normalize in parallel
    @parameter
    fn normalize_chunk(chunk_idx: Int):
        let start = chunk_idx * config.chunk_size
        let end = min(start + config.chunk_size, size)
        
        for i in range(start, end, config.simd_width):
            let vec_simd = SIMD[dtype, 8](vector.data + i)
            let normalized_simd = vec_simd / norm_value
            normalized_simd.store_aligned(normalized.data + i)
    
    parallelize[normalize_chunk](chunks, config.num_threads)
    return normalized

@always_inline
fn parallel_vector_similarity[dtype: DType](
    vectors: DynamicVector[Tensor[dtype]],
    query: Tensor[dtype],
    config: ParallelConfig
) raises -> DynamicVector[Tuple[Int, Float32]]:
    let num_vectors = len(vectors)
    var similarities = DynamicVector[Tuple[Int, Float32]]()
    let chunks = num_vectors // config.chunk_size
    
    @parameter
    fn compute_similarities_chunk(chunk_idx: Int):
        let start = chunk_idx * config.chunk_size
        let end = min(start + config.chunk_size, num_vectors)
        var chunk_similarities = DynamicVector[Tuple[Int, Float32]]()
        
        for i in range(start, end):
            let similarity = parallel_simd_dot_product(vectors[i], query, config)[0]
            if similarity > 0.5:  # Configurable threshold
                chunk_similarities.append((i, similarity))
        
        # Thread-safe append to global similarities
        with similarities.lock():
            similarities.extend(chunk_similarities)
    
    parallelize[compute_similarities_chunk](chunks, config.num_threads)
    return similarities

@always_inline
fn parallel_sort[T: AnyType](
    data: DynamicVector[T],
    compare_fn: fn(T, T) -> Bool,
    config: ParallelConfig
) raises -> DynamicVector[T]:
    let size = len(data)
    if size <= 1:
        return data
    
    # Parallel quicksort implementation
    fn partition(start: Int, end: Int) -> Int:
        let pivot = data[end - 1]
        var i = start - 1
        
        for j in range(start, end - 1):
            if compare_fn(data[j], pivot):
                i += 1
                let temp = data[i]
                data[i] = data[j]
                data[j] = temp
        
        let temp = data[i + 1]
        data[i + 1] = data[end - 1]
        data[end - 1] = temp
        return i + 1
    
    fn parallel_quicksort(start: Int, end: Int, depth: Int):
        if end - start > 1:
            if depth > 0 and end - start > config.chunk_size:
                let pivot = partition(start, end)
                
                # Spawn parallel tasks for sub-arrays
                @parameter
                fn sort_left(): parallel_quicksort(start, pivot, depth - 1)
                @parameter
                fn sort_right(): parallel_quicksort(pivot + 1, end, depth - 1)
                
                parallelize[sort_left, sort_right](2, 2)
            else:
                # Sequential sort for small chunks
                let pivot = partition(start, end)
                parallel_quicksort(start, pivot, 0)
                parallel_quicksort(pivot + 1, end, 0)
    
    # Start parallel sorting with maximum depth based on number of threads
    let max_depth = Int(log2(Float64(config.num_threads)))
    parallel_quicksort(0, size, max_depth)
    return data 