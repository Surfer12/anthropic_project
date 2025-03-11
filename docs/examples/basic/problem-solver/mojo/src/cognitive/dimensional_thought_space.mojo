from tensor import Tensor
from utils.vector import DynamicVector
from utils.static_tuple import StaticTuple
from memory.unsafe import Pointer
from math import sqrt, exp
from time import now
from utils.parallel import ParallelConfig, parallel_simd_dot_product, parallel_vector_normalize, parallel_vector_similarity, parallel_sort
from accelerator.metal_compute import MetalAccelerator

struct ThoughtVector:
    var id: String
    var vector: Tensor[DType.float32]
    var attributes: DynamicVector[Tuple[String, String]]
    var tags: DynamicVector[String]
    var timestamp: Int64
    
    fn __init__(inout self, id: String, vector_dim: Int):
        self.id = id
        self.vector = Tensor[DType.float32](vector_dim)
        self.attributes = DynamicVector[Tuple[String, String]]()
        self.tags = DynamicVector[String]()
        self.timestamp = now()
    
    fn add_attribute(inout self, key: String, value: String):
        self.attributes.append((key, value))
    
    fn add_tag(inout self, tag: String):
        self.tags.append(tag)
    
    fn has_tag(self, tag: String) -> Bool:
        for t in self.tags:
            if t == tag:
                return True
        return False

struct SemanticRelation:
    var source_id: String
    var target_id: String
    var strength: Float32
    var properties: DynamicVector[Tuple[String, Float32]]
    
    fn __init__(inout self, source: String, target: String, strength: Float32):
        self.source_id = source
        self.target_id = target
        self.strength = strength
        self.properties = DynamicVector[Tuple[String, Float32]]()
    
    fn add_property(inout self, key: String, value: Float32):
        self.properties.append((key, value))

@value
struct DimensionalThoughtSpace:
    var thought_vectors: DynamicVector[ThoughtVector]
    var relations: DynamicVector[SemanticRelation]
    var vector_dim: Int
    var parallel_config: ParallelConfig
    var metal_accelerator: MetalAccelerator
    
    fn __init__(inout self, vector_dim: Int = 128, num_threads: Int = 4):
        self.thought_vectors = DynamicVector[ThoughtVector]()
        self.relations = DynamicVector[SemanticRelation]()
        self.vector_dim = vector_dim
        self.parallel_config = ParallelConfig(num_threads)
        self.metal_accelerator = MetalAccelerator()
    
    fn add_thought(inout self, thought: ThoughtVector) raises:
        # Normalize thought vector using GPU
        thought.vector = self.metal_accelerator.normalize(thought.vector)
        self.thought_vectors.append(thought)
        self._update_semantic_relations_gpu(thought)
    
    fn find_similar_thoughts(self, query: ThoughtVector, threshold: Float32) raises -> DynamicVector[Tuple[ThoughtVector, Float32]]:
        # Normalize query vector using GPU
        let normalized_query = self.metal_accelerator.normalize(query.vector)
        
        # Find similarities using GPU batch processing
        let similarities = self.metal_accelerator.batch_similarity(
            self._get_thought_vectors(),
            normalized_query
        )
        
        # Convert results
        var results = DynamicVector[Tuple[ThoughtVector, Float32]]()
        for i in range(len(similarities)):
            if similarities[i] > threshold:
                results.append((self.thought_vectors[i], similarities[i]))
        
        # Sort results in parallel
        fn compare(a: Tuple[ThoughtVector, Float32], b: Tuple[ThoughtVector, Float32]) -> Bool:
            return a.1 > b.1
        
        return parallel_sort(results, compare, self.parallel_config)
    
    fn traverse_thought_space(self, 
                            start: ThoughtVector, 
                            importance_fn: fn(ThoughtVector) -> Float32) raises -> DynamicVector[ThoughtVector]:
        var path = DynamicVector[ThoughtVector]()
        var visited = DynamicVector[String]()
        
        self._traverse_recursive_parallel(start, importance_fn, path, visited)
        return path
    
    fn _traverse_recursive_parallel(inout self,
                                  current: ThoughtVector,
                                  importance_fn: fn(ThoughtVector) -> Float32,
                                  inout path: DynamicVector[ThoughtVector],
                                  inout visited: DynamicVector[String]) raises:
        visited.append(current.id)
        path.append(current)
        
        # Find candidates in parallel
        let candidates = self._find_candidates_parallel(current, visited, importance_fn)
        
        # Take top 3 candidates (beam search)
        for i in range(min(3, len(candidates))):
            let next_thought = candidates[i].0
            self._traverse_recursive_parallel(next_thought, importance_fn, path, visited)
    
    fn _find_candidates_parallel(self,
                               current: ThoughtVector,
                               visited: DynamicVector[String],
                               importance_fn: fn(ThoughtVector) -> Float32) raises -> DynamicVector[Tuple[ThoughtVector, Float32]]:
        var candidates = DynamicVector[Tuple[ThoughtVector, Float32]]()
        let chunks = len(self.thought_vectors) // self.parallel_config.chunk_size
        
        @parameter
        fn process_chunk(chunk_idx: Int):
            let start = chunk_idx * self.parallel_config.chunk_size
            let end = min(start + self.parallel_config.chunk_size, len(self.thought_vectors))
            var chunk_candidates = DynamicVector[Tuple[ThoughtVector, Float32]]()
            
            for i in range(start, end):
                let thought = self.thought_vectors[i]
                if not self._is_visited(thought.id, visited):
                    if self._has_strong_relation(current, thought):
                        let importance = importance_fn(thought)
                        chunk_candidates.append((thought, importance))
            
            # Thread-safe append to global candidates
            with candidates.lock():
                candidates.extend(chunk_candidates)
        
        parallelize[process_chunk](chunks, self.parallel_config.num_threads)
        
        # Sort candidates by importance
        fn compare(a: Tuple[ThoughtVector, Float32], b: Tuple[ThoughtVector, Float32]) -> Bool:
            return a.1 > b.1
        
        return parallel_sort(candidates, compare, self.parallel_config)
    
    fn _update_semantic_relations_gpu(inout self, new_thought: ThoughtVector) raises:
        let vectors = self._get_thought_vectors()
        let similarities = self.metal_accelerator.batch_similarity(
            vectors,
            new_thought.vector
        )
        
        # Create new relations for strong similarities
        for i in range(len(similarities)):
            let similarity = similarities[i]
            if similarity > 0.5 and i < len(self.thought_vectors):
                let thought = self.thought_vectors[i]
                if thought.id != new_thought.id:
                    self.relations.append(
                        SemanticRelation(thought.id, new_thought.id, similarity)
                    )
    
    fn _get_thought_vectors(self) -> DynamicVector[Tensor[DType.float32]]:
        var vectors = DynamicVector[Tensor[DType.float32]]()
        for thought in self.thought_vectors:
            vectors.append(thought.vector)
        return vectors
    
    fn _is_visited(self, id: String, visited: DynamicVector[String]) -> Bool:
        for v in visited:
            if v == id:
                return True
        return False
    
    fn _has_strong_relation(self, t1: ThoughtVector, t2: ThoughtVector) -> Bool:
        for relation in self.relations:
            if (relation.source_id == t1.id and relation.target_id == t2.id) or \
               (relation.source_id == t2.id and relation.target_id == t1.id):
                return relation.strength > 0.7
        return False 