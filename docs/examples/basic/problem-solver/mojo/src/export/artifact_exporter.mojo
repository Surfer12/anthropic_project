from utils.vector import DynamicVector
from time import now
from math import log2
from memory.buffer import Buffer
from memory.unsafe import Pointer

struct RetentionPolicy:
    var policy_type: Int  # 0: CIRCULAR_BUFFER, 1: COMPLETE, 2: HIERARCHICAL
    var duration: Int64   # -1 for indefinite
    var compression_ratio: Float32
    var indexing: Bool
    
    fn __init__(inout self, policy_type: Int, duration: Int64 = -1, 
                compression_ratio: Float32 = 1.0, indexing: Bool = False):
        self.policy_type = policy_type
        self.duration = duration
        self.compression_ratio = compression_ratio
        self.indexing = indexing

struct Artifact:
    var id: String
    var timestamp: Int64
    var artifact_type: Int  # 0: SENSORY, 1: FEATURE, 2: COGNITIVE, 3: META_COGNITIVE
    var content: DynamicVector[Tuple[String, Buffer]]
    var retention_policy: RetentionPolicy
    
    fn __init__(inout self, id: String, artifact_type: Int, policy: RetentionPolicy):
        self.id = id
        self.timestamp = now()
        self.artifact_type = artifact_type
        self.content = DynamicVector[Tuple[String, Buffer]]()
        self.retention_policy = policy
    
    fn add_content(inout self, key: String, data: Pointer[UInt8], size: Int):
        var buffer = Buffer(size)
        buffer.copy_from(data, size)
        self.content.append((key, buffer))
    
    fn get_content(self, key: String) -> Optional[Buffer]:
        for item in self.content:
            if item.0 == key:
                return item.1
        return None

struct CircularBuffer[T: AnyType]:
    var data: DynamicVector[T]
    var capacity: Int
    var head: Int
    var tail: Int
    var size: Int
    
    fn __init__(inout self, capacity: Int):
        self.data = DynamicVector[T]()
        self.capacity = capacity
        self.head = 0
        self.tail = 0
        self.size = 0
    
    fn push(inout self, item: T):
        if self.size == self.capacity:
            self.data[self.head] = item
            self.head = (self.head + 1) % self.capacity
            self.tail = (self.tail + 1) % self.capacity
        else:
            self.data.append(item)
            self.size += 1
            self.head = (self.head + 1) % self.capacity
    
    fn get(self, index: Int) -> Optional[T]:
        if index >= self.size:
            return None
        let actual_index = (self.tail + index) % self.capacity
        return self.data[actual_index]

@value
struct ArtifactExporter:
    var sensory_buffer: CircularBuffer[Artifact]
    var feature_store: DynamicVector[Artifact]
    var cognitive_store: DynamicVector[Artifact]
    var meta_store: DynamicVector[Artifact]
    
    fn __init__(inout self):
        self.sensory_buffer = CircularBuffer[Artifact](1000)  # Keep last 1000 sensory artifacts
        self.feature_store = DynamicVector[Artifact]()
        self.cognitive_store = DynamicVector[Artifact]()
        self.meta_store = DynamicVector[Artifact]()
    
    fn export_thought(inout self, thought: ThoughtVector, context: DynamicVector[Tuple[String, String]]):
        if self._is_interesting(thought, context):
            let artifact = self._create_artifact(thought, context)
            self._store_artifact(artifact)
    
    fn _create_artifact(self, thought: ThoughtVector, 
                       context: DynamicVector[Tuple[String, String]]) -> Artifact:
        let artifact_type = self._determine_type(thought)
        let policy = self._select_policy(artifact_type)
        var artifact = Artifact(thought.id, artifact_type, policy)
        
        # Add thought vector data
        let vector_size = len(thought.vector) * sizeof[Float32]()
        artifact.add_content("vector", Pointer[UInt8](thought.vector.data), vector_size)
        
        # Add attributes
        for attr in thought.attributes:
            artifact.add_content(attr.0, Pointer[UInt8](attr.1.data), len(attr.1))
        
        # Add context
        for ctx in context:
            artifact.add_content("ctx_" + ctx.0, Pointer[UInt8](ctx.1.data), len(ctx.1))
        
        return artifact
    
    fn _store_artifact(inout self, artifact: Artifact):
        match artifact.artifact_type:
            case 0:  # SENSORY
                self.sensory_buffer.push(artifact)
            case 1:  # FEATURE
                self.feature_store.append(artifact)
            case 2:  # COGNITIVE
                if len(self.cognitive_store) > 10000:  # Limit cognitive store size
                    self._compress_cognitive_store()
                self.cognitive_store.append(artifact)
            case 3:  # META_COGNITIVE
                self.meta_store.append(artifact)
    
    fn _compress_cognitive_store(inout self):
        # Implement hierarchical compression
        # This is a placeholder for actual compression logic
        let compression_ratio = 0.5
        let new_size = Int(Float32(len(self.cognitive_store)) * compression_ratio)
        
        var compressed_store = DynamicVector[Artifact]()
        for i in range(new_size):
            compressed_store.append(self.cognitive_store[i * 2])
        
        self.cognitive_store = compressed_store
    
    fn _determine_type(self, thought: ThoughtVector) -> Int:
        if thought.has_tag("sensory"):
            return 0
        elif thought.has_tag("feature"):
            return 1
        elif thought.has_tag("meta"):
            return 3
        else:
            return 2
    
    fn _select_policy(self, artifact_type: Int) -> RetentionPolicy:
        match artifact_type:
            case 0:  # SENSORY
                return RetentionPolicy(0, 2000)  # Circular buffer, 2 second retention
            case 1:  # FEATURE
                return RetentionPolicy(1)  # Complete retention
            case 2:  # COGNITIVE
                return RetentionPolicy(2, -1, 0.5)  # Hierarchical with compression
            case 3:  # META_COGNITIVE
                return RetentionPolicy(1, -1, 1.0, True)  # Complete with indexing
            default:
                return RetentionPolicy(1)  # Default to complete retention
    
    fn _is_interesting(self, thought: ThoughtVector, 
                      context: DynamicVector[Tuple[String, String]]) -> Bool:
        # Check attention-driven interest
        for ctx in context:
            if ctx.0 == "attention_duration":
                if Int(ctx.1) > 300:
                    return True
        
        # Check anomaly-driven interest
        if thought.has_tag("anomaly"):
            return True
        
        # Check pattern completion
        if thought.has_tag("pattern_match"):
            return True
        
        # Check meta-cognitive aspects
        if thought.has_tag("meta") or thought.has_tag("recursive"):
            return True
        
        return False 