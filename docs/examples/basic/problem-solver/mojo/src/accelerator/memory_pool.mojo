from tensor import Tensor
from math import min, max
from time import now
from utils.vector import DynamicVector

struct BufferBlock:
    var size: Int
    var in_use: Bool
    var last_used: Int64
    var buffer_id: Int
    
    fn __init__(inout self, size: Int, buffer_id: Int):
        self.size = size
        self.in_use = False
        self.last_used = now()
        self.buffer_id = buffer_id

struct MemoryPool:
    var total_size: Int
    var used_size: Int
    var blocks: DynamicVector[BufferBlock]
    var device: MetalDevice
    var min_block_size: Int
    var max_block_size: Int
    var next_buffer_id: Int
    
    fn __init__(inout self, device: MetalDevice, 
                total_size: Int = 1024 * 1024 * 1024,  # 1GB default
                min_block_size: Int = 1024,            # 1KB minimum
                max_block_size: Int = 128 * 1024 * 1024  # 128MB maximum
    ):
        self.device = device
        self.total_size = total_size
        self.used_size = 0
        self.blocks = DynamicVector[BufferBlock]()
        self.min_block_size = min_block_size
        self.max_block_size = max_block_size
        self.next_buffer_id = 0
    
    fn allocate(inout self, size: Int) raises -> MetalBuffer:
        # Round up size to nearest power of 2
        let aligned_size = self._align_size(size)
        
        # Try to find existing block
        for i in range(len(self.blocks)):
            if not self.blocks[i].in_use and self.blocks[i].size >= aligned_size:
                self.blocks[i].in_use = True
                self.blocks[i].last_used = now()
                self.used_size += aligned_size
                return self.device.get_buffer(self.blocks[i].buffer_id)
        
        # Create new block if space available
        if self.used_size + aligned_size <= self.total_size:
            let buffer = self.device.create_buffer(aligned_size)
            let block = BufferBlock(aligned_size, self.next_buffer_id)
            self.next_buffer_id += 1
            block.in_use = True
            self.blocks.append(block)
            self.used_size += aligned_size
            return buffer
        
        # Try to free up space
        self._cleanup()
        
        # Try allocation again
        if self.used_size + aligned_size <= self.total_size:
            let buffer = self.device.create_buffer(aligned_size)
            let block = BufferBlock(aligned_size, self.next_buffer_id)
            self.next_buffer_id += 1
            block.in_use = True
            self.blocks.append(block)
            self.used_size += aligned_size
            return buffer
        
        raise Error("Out of memory in pool")
    
    fn deallocate(inout self, buffer_id: Int):
        for i in range(len(self.blocks)):
            if self.blocks[i].buffer_id == buffer_id:
                self.blocks[i].in_use = False
                self.blocks[i].last_used = now()
                self.used_size -= self.blocks[i].size
                return
    
    fn _cleanup(inout self):
        # Sort blocks by last used time
        self._sort_blocks_by_time()
        
        # Free least recently used blocks until we have 25% free space
        let target_used = self.total_size * 3 // 4
        var i = len(self.blocks) - 1
        
        while self.used_size > target_used and i >= 0:
            if not self.blocks[i].in_use:
                self.device.release_buffer(self.blocks[i].buffer_id)
                self.used_size -= self.blocks[i].size
                self.blocks.remove_at(i)
            i -= 1
    
    fn _sort_blocks_by_time(inout self):
        let n = len(self.blocks)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.blocks[j].last_used > self.blocks[j + 1].last_used:
                    let temp = self.blocks[j]
                    self.blocks[j] = self.blocks[j + 1]
                    self.blocks[j + 1] = temp
    
    fn _align_size(self, size: Int) -> Int:
        var aligned = self.min_block_size
        while aligned < size and aligned < self.max_block_size:
            aligned *= 2
        return min(aligned, self.max_block_size)
    
    fn get_stats(self) -> PerfStats:
        return PerfStats(
            total_size=self.total_size,
            used_size=self.used_size,
            num_blocks=len(self.blocks),
            num_active_blocks=self._count_active_blocks(),
            fragmentation=self._calculate_fragmentation()
        )
    
    fn _count_active_blocks(self) -> Int:
        var count = 0
        for block in self.blocks:
            if block.in_use:
                count += 1
        return count
    
    fn _calculate_fragmentation(self) -> Float32:
        var total_free = 0
        var largest_free = 0
        
        for block in self.blocks:
            if not block.in_use:
                total_free += block.size
                largest_free = max(largest_free, block.size)
        
        if total_free == 0:
            return 0.0
        
        return 1.0 - Float32(largest_free) / Float32(total_free) 