from utils.vector import DynamicVector
from time import now
from math import log2

struct MetricTracker:
    var name: String
    var recent_values: DynamicVector[Float32]
    let window_size: Int = 100
    
    fn __init__(inout self, name: String):
        self.name = name
        self.recent_values = DynamicVector[Float32]()
    
    fn add_value(inout self, value: Float32):
        self.recent_values.append(value)
        if len(self.recent_values) > self.window_size:
            self.recent_values.pop_front()
    
    fn get_recent_average(self) -> Float32:
        if len(self.recent_values) == 0:
            return 0.0
            
        var sum: Float32 = 0.0
        for value in self.recent_values:
            sum += value
        return sum / Float32(len(self.recent_values))

struct SystemState:
    var complexity_level: Float32
    var coherence_level: Float32
    var recursion_level: Float32
    var pattern_level: Float32
    
    fn __init__(inout self):
        self.complexity_level = 0.0
        self.coherence_level = 0.0
        self.recursion_level = 0.0
        self.pattern_level = 0.0
    
    fn equals(self, other: SystemState) -> Bool:
        return (self.complexity_level == other.complexity_level and
                self.coherence_level == other.coherence_level and
                self.recursion_level == other.recursion_level and
                self.pattern_level == other.pattern_level)

@value
struct MetaCognitiveEvent:
    var event_type: EventType
    var thought_id: String
    var timestamp: Int64
    var metadata: DynamicVector[Tuple[String, Float32]]
    
    fn __init__(inout self, event_type: EventType, thought_id: String):
        self.event_type = event_type
        self.thought_id = thought_id
        self.timestamp = now()
        self.metadata = DynamicVector[Tuple[String, Float32]]()
    
    fn add_metadata(inout self, key: String, value: Float32):
        self.metadata.append((key, value))

@value
struct MetaCognitiveMonitor:
    var event_stream: DynamicVector[MetaCognitiveEvent]
    var metrics: DynamicVector[Tuple[String, MetricTracker]]
    var current_state: SystemState
    
    fn __init__(inout self):
        self.event_stream = DynamicVector[MetaCognitiveEvent]()
        self.metrics = DynamicVector[Tuple[String, MetricTracker]]()
        self.current_state = SystemState()
        self._initialize_metrics()
    
    fn _initialize_metrics(inout self):
        self.metrics.append(("complexity", MetricTracker("Thought Space Complexity")))
        self.metrics.append(("coherence", MetricTracker("Semantic Coherence")))
        self.metrics.append(("recursion_depth", MetricTracker("Recursive Processing Depth")))
        self.metrics.append(("pattern_emergence", MetricTracker("Pattern Emergence Rate")))
    
    fn record_thought_addition(inout self, thought: ThoughtVector):
        var event = MetaCognitiveEvent(EventType.THOUGHT_ADDITION, thought.id)
        event.add_metadata("vector_dimension", Float32(len(thought.vector)))
        event.add_metadata("attribute_count", Float32(len(thought.attributes)))
        event.add_metadata("tag_count", Float32(len(thought.tags)))
        
        self.event_stream.append(event)
        self._update_metrics(event)
    
    fn record_traversal(inout self, path: DynamicVector[ThoughtVector]):
        var event = MetaCognitiveEvent(EventType.SPACE_TRAVERSAL, "traversal")
        event.add_metadata("path_length", Float32(len(path)))
        
        # Count unique tags
        var unique_tags = DynamicVector[String]()
        for thought in path:
            for tag in thought.tags:
                if not self._contains(unique_tags, tag):
                    unique_tags.append(tag)
        
        event.add_metadata("unique_tags", Float32(len(unique_tags)))
        
        self.event_stream.append(event)
        self._update_metrics(event)
    
    fn _update_metrics(inout self, event: MetaCognitiveEvent):
        if event.event_type == EventType.THOUGHT_ADDITION:
            self._update_complexity_metric(event)
            self._update_coherence_metric(event)
        elif event.event_type == EventType.SPACE_TRAVERSAL:
            self._update_recursion_metric(event)
            self._update_pattern_metric(event)
        
        self._check_thresholds()
    
    fn _update_complexity_metric(inout self, event: MetaCognitiveEvent):
        let vector_dim = self._get_metadata_value(event, "vector_dimension")
        let attr_count = self._get_metadata_value(event, "attribute_count")
        
        for metric in self.metrics:
            if metric.0 == "complexity":
                metric.1.add_value((vector_dim + attr_count) / 2.0)
    
    fn _update_recursion_metric(inout self, event: MetaCognitiveEvent):
        if event.event_type == EventType.SPACE_TRAVERSAL:
            let path_length = self._get_metadata_value(event, "path_length")
            
            for metric in self.metrics:
                if metric.0 == "recursion_depth":
                    metric.1.add_value(log2(path_length))
    
    fn _check_thresholds(inout self):
        var new_state = SystemState()
        
        new_state.complexity_level = self._calculate_metric_level("complexity")
        new_state.coherence_level = self._calculate_metric_level("coherence")
        new_state.recursion_level = self._calculate_metric_level("recursion_depth")
        new_state.pattern_level = self._calculate_metric_level("pattern_emergence")
        
        if not new_state.equals(self.current_state):
            self.current_state = new_state
            # Log state change (when logging is available)
    
    fn _calculate_metric_level(self, metric_name: String) -> Float32:
        for metric in self.metrics:
            if metric.0 == metric_name:
                return metric.1.get_recent_average()
        return 0.0
    
    fn _get_metadata_value(self, event: MetaCognitiveEvent, key: String) -> Float32:
        for item in event.metadata:
            if item.0 == key:
                return item.1
        return 0.0
    
    fn _contains(self, vec: DynamicVector[String], item: String) -> Bool:
        for x in vec:
            if x == item:
                return True
        return False

enum EventType:
    THOUGHT_ADDITION = 0
    SPACE_TRAVERSAL = 1 