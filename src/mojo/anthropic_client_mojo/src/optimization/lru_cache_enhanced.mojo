lru_cache_enhanced.mojo

from memory.unsafe import Pointer
from memory.buffer import Buffer
from time import now

@value
struct CacheEntry[V: AnyType]:
    var value: V
    var timestamp: Float64
    var access_count: Int
    
    fn __init__(inout self, value: V):
        self.value = value
        self.timestamp = now()
        self.access_count = 1
    
    fn update_access(inout self):
        self.timestamp = now()
        self.access_count += 1

@value
struct LRUCache[K: Stringable, V: AnyType]:
    // Cache configuration
    var capacity: Int
    var ttl_seconds: Float64  // Time-to-live in seconds
    
    // Primary storage
    var cache: Dictionary[K, CacheEntry[V]]
    var order: Array[K]  // Using Array instead of DynamicVector for memory efficiency
    
    // Memory management
    var memory_arena: Optional[ArenaAllocator]
    var use_arena: Bool
    
    // Statistics
    var hits: Int
    var misses: Int
    var evictions: Int
    
    fn __init__(inout self, capacity: Int, ttl_seconds: Float64 = -1, use_arena: Bool = False):
        self.capacity = capacity
        self.ttl_seconds = ttl_seconds
        self.cache = Dictionary[K, CacheEntry[V]]()
        self.order = Array[K](capacity)
        self.use_arena = use_arena
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        
        if use_arena:
            // Estimate arena size based on capacity and average entry size
            let estimated_size = capacity * (sizeof[K]() + sizeof[CacheEntry[V]]() + 64)  // 64 bytes padding
            self.memory_arena = ArenaAllocator(estimated_size)
        else:
            self.memory_arena = None
    
    fn get(inout self, key: K) -> Optional[V]:
        // Expire entries if TTL is enabled
        if self.ttl_seconds > 0:
            self._expire_old_entries()
        
        if self.cache.containsKey(key):
            var entry = self.cache[key]
            
            // Update access metadata
            entry.update_access()
            self.cache[key] = entry
            
            // Update order (move to end)
            let idx = self._find_key_index(key)
            if idx >= 0:
                self._remove_from_order(idx)
                self._append_to_order(key)
            
            self.hits += 1
            return entry.value
        
        self.misses += 1
        return None
    
    fn put(inout self, key: K, value: V):
        // Expire entries if TTL is enabled
        if self.ttl_seconds > 0:
            self._expire_old_entries()
        
        if self.cache.containsKey(key):
            // Update existing entry
            var entry = self.cache[key]
            
            // If using arena, we need to handle memory differently
            if self.use_arena and self.memory_arena:
                // For simplicity, we're not showing the detailed arena allocation here
                // In practice, you'd allocate from the arena and copy the value
                pass
            
            entry.value = value
            entry.update_access()
            self.cache[key] = entry
            
            // Update order
            let idx = self._find_key_index(key)
            if idx >= 0:
                self._remove_from_order(idx)
                self._append_to_order(key)
        else:
            // If cache is full, remove the least recently used entry
            if len(self.cache) >= self.capacity:
                self._evict_lru()
            
            // Create new entry
            var entry = CacheEntry[V](value)
            
            // If using arena, allocate from arena
            if self.use_arena and self.memory_arena:
                // For simplicity, we're not showing the detailed arena allocation here
                pass
            
            self.cache[key] = entry
            self._append_to_order(key)
    
    fn contains(self, key: K) -> Bool:
        return self.cache.containsKey(key)
    
    fn size(self) -> Int:
        return len(self.cache)
    
    fn clear(inout self):
        self.cache.clear()
        // Reset order array
        for i in range(len(self.order)):
            if i < self.order.size:
                self.order[i] = K()  // Default value
        
        // Reset statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        
        // Reset arena if using one
        if self.use_arena and self.memory_arena:
            self.memory_arena.reset()
    
    fn get_stats(self) -> Tuple[Int, Int, Int, Float64]:
        let total_requests = self.hits + self.misses
        let hit_ratio = self.hits / total_requests if total_requests > 0 else 0.0
        return (self.hits, self.misses, self.evictions, hit_ratio)
    
    // Private helper methods
    fn _find_key_index(self, key: K) -> Int:
        for i in range(len(self.order)):
            if i < self.order.size and self.order[i] == key:
                return i
        return -1
    
    fn _remove_from_order(inout self, idx: Int):
        // Shift elements to fill the gap
        for i in range(idx, len(self.order) - 1):
            if i < self.order.size - 1:
                self.order[i] = self.order[i + 1]
    
    fn _append_to_order(inout self, key: K):
        let current_size = len(self.order)
        if current_size < self.capacity:
            self.order[current_size] = key
    
    fn _evict_lru(inout self):
        if len(self.order) > 0:
            let lru_key = self.order[0]
            self._remove_from_order(0)
            self.cache.remove(lru_key)
            self.evictions += 1
    
    fn _expire_old_entries(inout self):
        let current_time = now()
        var keys_to_remove = DynamicVector[K]()
        
        // Identify expired entries
        for key in self.cache.keys():
            let entry = self.cache[key]
            if current_time - entry.timestamp > self.ttl_seconds:
                keys_to_remove.append(key)
        
        // Remove expired entries
        for key in keys_to_remove:
            self.cache.remove(key)
            let idx = self._find_key_index(key)
            if idx >= 0:
                self._remove_from_order(idx)
            self.evictions += 1

// Example integration with AnthropicClient
struct CachedAnthropicClient:
    var client: AnthropicClient
    var response_cache: LRUCache[String, String]
    var embedding_cache: LRUCache[String, Array[Float32]]
    
    fn __init__(inout self, client: AnthropicClient, response_cache_size: Int = 100, embedding_cache_size: Int = 500):
        self.client = client
        self.response_cache = LRUCache[String, String](response_cache_size, ttl_seconds=3600)  // 1 hour TTL
        self.embedding_cache = LRUCache[String, Array[Float32]](embedding_cache_size, ttl_seconds=86400)  // 24 hour TTL
    
    fn get_response(inout self, prompt: String) raises -> String:
        // Check cache first
        let cached_response = self.response_cache.get(prompt)
        if cached_response:
            return cached_response.value()
        
        // If not in cache, call API
        let response = self.client.get_response(prompt)
        
        // Cache the result
        self.response_cache.put(prompt, response)
        
        return response
    
    fn get_embedding(inout self, text: String) raises -> Array[Float32]:
        // Check cache first
        let cached_embedding = self.embedding_cache.get(text)
        if cached_embedding:
            return cached_embedding.value()
        
        // If not in cache, compute embedding
        let embedding = self.client.get_embedding(text)
        
        // Cache the result
        self.embedding_cache.put(text, embedding)
        
        return embedding
    
    fn get_cache_stats(self) -> Tuple[Tuple[Int, Int, Int, Float64], Tuple[Int, Int, Int, Float64]]:
        return (self.response_cache.get_stats(), self.embedding_cache.get_stats())

// Example usage
fn main() raises:
    var client = AnthropicClient(ClientConfig(api_key="YOUR_API_KEY"))
    var cached_client = CachedAnthropicClient(client)
    
    // First request - will miss cache
    let response1 = cached_client.get_response("Tell me about quantum computing")
    print("Response 1:", response1)
    
    // Second request with same prompt - will hit cache
    let response2 = cached_client.get_response("Tell me about quantum computing")
    print("Response 2 (from cache):", response2)
    
    // Get cache statistics
    let stats = cached_client.get_cache_stats()
    print("Response cache stats - Hits:", stats.0.0, "Misses:", stats.0.1, "Hit ratio:", stats.0.3)
    print("Embedding cache stats - Hits:", stats.1.0, "Misses:", stats.1.1, "Hit ratio:", stats.1.3)