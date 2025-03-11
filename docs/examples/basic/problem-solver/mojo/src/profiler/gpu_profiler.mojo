from tensor import Tensor
from time import now
from utils.vector import DynamicVector
from math import sqrt, exp

struct KernelProfile:
    var name: String
    var total_time: Int64
    var call_count: Int
    var min_time: Int64
    var max_time: Int64
    var total_bytes_processed: Int64
    
    fn __init__(inout self, name: String):
        self.name = name
        self.total_time = 0
        self.call_count = 0
        self.min_time = 9223372036854775807  # Int64.MAX_VALUE
        self.max_time = 0
        self.total_bytes_processed = 0
    
    fn add_execution(inout self, duration: Int64, bytes_processed: Int64):
        self.total_time += duration
        self.call_count += 1
        self.min_time = min(self.min_time, duration)
        self.max_time = max(self.max_time, duration)
        self.total_bytes_processed += bytes_processed
    
    fn get_average_time(self) -> Float64:
        if self.call_count == 0:
            return 0.0
        return Float64(self.total_time) / Float64(self.call_count)
    
    fn get_throughput(self) -> Float64:
        if self.total_time == 0:
            return 0.0
        return Float64(self.total_bytes_processed) / Float64(self.total_time)

struct MemoryProfile:
    var total_allocated: Int64
    var peak_allocated: Int64
    var current_allocated: Int64
    var allocation_count: Int
    var deallocation_count: Int
    
    fn __init__(inout self):
        self.total_allocated = 0
        self.peak_allocated = 0
        self.current_allocated = 0
        self.allocation_count = 0
        self.deallocation_count = 0
    
    fn record_allocation(inout self, size: Int64):
        self.total_allocated += size
        self.current_allocated += size
        self.peak_allocated = max(self.peak_allocated, self.current_allocated)
        self.allocation_count += 1
    
    fn record_deallocation(inout self, size: Int64):
        self.current_allocated -= size
        self.deallocation_count += 1

@value
struct GPUProfiler:
    var kernel_profiles: DynamicVector[KernelProfile]
    var memory_profile: MemoryProfile
    var start_times: DynamicVector[Tuple[String, Int64]]
    var enabled: Bool
    
    fn __init__(inout self):
        self.kernel_profiles = DynamicVector[KernelProfile]()
        self.memory_profile = MemoryProfile()
        self.start_times = DynamicVector[Tuple[String, Int64]]()
        self.enabled = True
    
    fn start_kernel(inout self, name: String):
        if not self.enabled:
            return
        self.start_times.append((name, now()))
    
    fn end_kernel(inout self, name: String, bytes_processed: Int64):
        if not self.enabled:
            return
            
        let end_time = now()
        var found_start = False
        var start_time: Int64 = 0
        
        # Find and remove matching start time
        for i in range(len(self.start_times) - 1, -1, -1):
            if self.start_times[i].0 == name:
                start_time = self.start_times[i].1
                self.start_times.remove_at(i)
                found_start = True
                break
        
        if not found_start:
            return
        
        let duration = end_time - start_time
        
        # Find or create kernel profile
        var found_profile = False
        for i in range(len(self.kernel_profiles)):
            if self.kernel_profiles[i].name == name:
                self.kernel_profiles[i].add_execution(duration, bytes_processed)
                found_profile = True
                break
        
        if not found_profile:
            var profile = KernelProfile(name)
            profile.add_execution(duration, bytes_processed)
            self.kernel_profiles.append(profile)
    
    fn record_allocation(inout self, size: Int64):
        if not self.enabled:
            return
        self.memory_profile.record_allocation(size)
    
    fn record_deallocation(inout self, size: Int64):
        if not self.enabled:
            return
        self.memory_profile.record_deallocation(size)
    
    fn get_kernel_stats(self) -> DynamicVector[KernelStats]:
        var stats = DynamicVector[KernelStats]()
        for profile in self.kernel_profiles:
            stats.append(KernelStats(
                name=profile.name,
                avg_time=profile.get_average_time(),
                min_time=profile.min_time,
                max_time=profile.max_time,
                call_count=profile.call_count,
                throughput=profile.get_throughput()
            ))
        return stats
    
    fn get_memory_stats(self) -> MemoryStats:
        return MemoryStats(
            total_allocated=self.memory_profile.total_allocated,
            peak_allocated=self.memory_profile.peak_allocated,
            current_allocated=self.memory_profile.current_allocated,
            allocation_count=self.memory_profile.allocation_count,
            deallocation_count=self.memory_profile.deallocation_count
        )
    
    fn reset(inout self):
        self.kernel_profiles = DynamicVector[KernelProfile]()
        self.memory_profile = MemoryProfile()
        self.start_times = DynamicVector[Tuple[String, Int64]]()
    
    fn enable(inout self):
        self.enabled = True
    
    fn disable(inout self):
        self.enabled = False

struct KernelStats:
    var name: String
    var avg_time: Float64
    var min_time: Int64
    var max_time: Int64
    var call_count: Int
    var throughput: Float64

struct MemoryStats:
    var total_allocated: Int64
    var peak_allocated: Int64
    var current_allocated: Int64
    var allocation_count: Int
    var deallocation_count: Int 