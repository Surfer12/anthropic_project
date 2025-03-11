from tensor import Tensor
from time import now
from utils.vector import DynamicVector
from math import sqrt, exp
from metal import MetalDevice

struct HardwareMetrics:
    var gpu_utilization: Float32
    var memory_bandwidth: Float32
    var cache_hit_rate: Float32
    var power_consumption: Float32
    var temperature: Float32
    
    fn __init__(inout self):
        self.gpu_utilization = 0.0
        self.memory_bandwidth = 0.0
        self.cache_hit_rate = 0.0
        self.power_consumption = 0.0
        self.temperature = 0.0

struct WorkloadMetrics:
    var flops: Int64
    var memory_ops: Int64
    var cache_ops: Int64
    var simd_efficiency: Float32
    var thread_occupancy: Float32
    
    fn __init__(inout self):
        self.flops = 0
        self.memory_ops = 0
        self.cache_ops = 0
        self.simd_efficiency = 0.0
        self.thread_occupancy = 0.0

struct KernelMetrics:
    var name: String
    var execution_time: Int64
    var bytes_processed: Int64
    var workload: WorkloadMetrics
    var hardware: HardwareMetrics
    var memory_footprint: Int64
    var thread_count: Int
    
    fn __init__(inout self, name: String):
        self.name = name
        self.execution_time = 0
        self.bytes_processed = 0
        self.workload = WorkloadMetrics()
        self.hardware = HardwareMetrics()
        self.memory_footprint = 0
        self.thread_count = 0
    
    fn calculate_efficiency(self) -> Float32:
        let theoretical_peak = 10.0  # TFLOPS for M4 Max
        let achieved_flops = Float32(self.workload.flops) / Float32(self.execution_time)
        return achieved_flops / (theoretical_peak * 1e12)
    
    fn calculate_memory_efficiency(self) -> Float32:
        let theoretical_bandwidth = 400.0  # GB/s for M4 Max
        let achieved_bandwidth = Float32(self.bytes_processed) / Float32(self.execution_time)
        return achieved_bandwidth / (theoretical_bandwidth * 1e9)

@value
struct EnhancedProfiler:
    var kernel_metrics: DynamicVector[KernelMetrics]
    var current_kernel: String
    var start_time: Int64
    var device: MetalDevice
    var enabled: Bool
    
    fn __init__(inout self, device: MetalDevice):
        self.kernel_metrics = DynamicVector[KernelMetrics]()
        self.current_kernel = ""
        self.start_time = 0
        self.device = device
        self.enabled = True
    
    fn start_profiling(inout self, kernel_name: String, thread_count: Int):
        if not self.enabled:
            return
            
        self.current_kernel = kernel_name
        self.start_time = now()
        
        # Create or update kernel metrics
        var found = False
        for i in range(len(self.kernel_metrics)):
            if self.kernel_metrics[i].name == kernel_name:
                self.kernel_metrics[i].thread_count = thread_count
                found = True
                break
        
        if not found:
            var metrics = KernelMetrics(kernel_name)
            metrics.thread_count = thread_count
            self.kernel_metrics.append(metrics)
    
    fn end_profiling(inout self, bytes_processed: Int64):
        if not self.enabled or self.current_kernel == "":
            return
            
        let end_time = now()
        let duration = end_time - self.start_time
        
        # Update metrics
        for i in range(len(self.kernel_metrics)):
            if self.kernel_metrics[i].name == self.current_kernel:
                self.kernel_metrics[i].execution_time += duration
                self.kernel_metrics[i].bytes_processed += bytes_processed
                self._update_hardware_metrics(i)
                self._update_workload_metrics(i, bytes_processed)
                break
        
        self.current_kernel = ""
    
    fn _update_hardware_metrics(inout self, index: Int):
        # Get hardware metrics from Metal
        let counters = self.device.get_counters()
        
        self.kernel_metrics[index].hardware.gpu_utilization = counters.gpu_utilization
        self.kernel_metrics[index].hardware.memory_bandwidth = counters.memory_bandwidth
        self.kernel_metrics[index].hardware.cache_hit_rate = counters.cache_hit_rate
        self.kernel_metrics[index].hardware.power_consumption = counters.power_consumption
        self.kernel_metrics[index].hardware.temperature = counters.temperature
    
    fn _update_workload_metrics(inout self, index: Int, bytes_processed: Int64):
        let metrics = self.kernel_metrics[index]
        let duration = Float32(metrics.execution_time)
        
        # Calculate FLOPS
        metrics.workload.flops = Int64(Float32(bytes_processed) * 2.0 / duration)  # Assuming 2 FLOPs per byte
        
        # Calculate memory operations
        metrics.workload.memory_ops = bytes_processed // 4  # Assuming 4 bytes per operation
        
        # Calculate cache operations (estimate)
        metrics.workload.cache_ops = metrics.workload.memory_ops // 2
        
        # Calculate SIMD efficiency
        metrics.workload.simd_efficiency = self._calculate_simd_efficiency(metrics)
        
        # Calculate thread occupancy
        metrics.workload.thread_occupancy = self._calculate_thread_occupancy(metrics)
    
    fn _calculate_simd_efficiency(self, metrics: KernelMetrics) -> Float32:
        let theoretical_simd_ops = Float32(metrics.thread_count) * 8.0  # 8-wide SIMD
        let actual_simd_ops = Float32(metrics.workload.flops) / Float32(metrics.execution_time)
        return min(1.0, actual_simd_ops / theoretical_simd_ops)
    
    fn _calculate_thread_occupancy(self, metrics: KernelMetrics) -> Float32:
        let max_threads = 2048  # M4 Max theoretical max threads
        return min(1.0, Float32(metrics.thread_count) / Float32(max_threads))
    
    fn get_kernel_report(self) -> String:
        var report = "Kernel Performance Report\n"
        report += "=======================\n\n"
        
        for metrics in self.kernel_metrics:
            report += f"Kernel: {metrics.name}\n"
            report += f"  Execution Time: {metrics.execution_time / 1000000.0:.2f}ms\n"
            report += f"  Data Processed: {metrics.bytes_processed / 1024.0 / 1024.0:.2f}MB\n"
            report += f"  Compute Efficiency: {metrics.calculate_efficiency() * 100:.1f}%\n"
            report += f"  Memory Efficiency: {metrics.calculate_memory_efficiency() * 100:.1f}%\n"
            report += f"  SIMD Efficiency: {metrics.workload.simd_efficiency * 100:.1f}%\n"
            report += f"  Thread Occupancy: {metrics.workload.thread_occupancy * 100:.1f}%\n"
            report += f"  GPU Utilization: {metrics.hardware.gpu_utilization * 100:.1f}%\n"
            report += f"  Memory Bandwidth: {metrics.hardware.memory_bandwidth / 1e9:.1f}GB/s\n"
            report += f"  Cache Hit Rate: {metrics.hardware.cache_hit_rate * 100:.1f}%\n"
            report += f"  Power Consumption: {metrics.hardware.power_consumption:.1f}W\n"
            report += f"  Temperature: {metrics.hardware.temperature:.1f}°C\n\n"
        
        return report
    
    fn get_optimization_suggestions(self) -> String:
        var suggestions = "Optimization Suggestions\n"
        suggestions += "=======================\n\n"
        
        for metrics in self.kernel_metrics:
            suggestions += f"Kernel: {metrics.name}\n"
            
            # Check compute efficiency
            if metrics.calculate_efficiency() < 0.3:
                suggestions += "- Low compute efficiency. Consider:\n"
                suggestions += "  * Increasing workgroup size\n"
                suggestions += "  * Reducing thread divergence\n"
                suggestions += "  * Using vectorized operations\n"
            
            # Check memory efficiency
            if metrics.calculate_memory_efficiency() < 0.4:
                suggestions += "- Suboptimal memory performance. Consider:\n"
                suggestions += "  * Coalescing memory accesses\n"
                suggestions += "  * Using shared memory\n"
                suggestions += "  * Improving memory access patterns\n"
            
            # Check SIMD efficiency
            if metrics.workload.simd_efficiency < 0.6:
                suggestions += "- Low SIMD utilization. Consider:\n"
                suggestions += "  * Aligning data access\n"
                suggestions += "  * Reducing control flow divergence\n"
                suggestions += "  * Using SIMD-friendly data layouts\n"
            
            # Check thread occupancy
            if metrics.workload.thread_occupancy < 0.7:
                suggestions += "- Low thread occupancy. Consider:\n"
                suggestions += "  * Reducing shared memory usage\n"
                suggestions += "  * Adjusting workgroup size\n"
                suggestions += "  * Splitting kernel into multiple passes\n"
            
            suggestions += "\n"
        
        return suggestions 