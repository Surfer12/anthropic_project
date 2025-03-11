from tensor import Tensor
from utils.vector import DynamicVector
from profiler.enhanced_profiler import KernelMetrics, HardwareMetrics, WorkloadMetrics
from math import sqrt, exp
from metal import MetalDevice

struct OptimizationParameters:
    var workgroup_size: Int
    var simd_width: Int
    var shared_memory_size: Int
    var cache_strategy: Int  # 0: None, 1: L1, 2: L2
    var prefetch_distance: Int
    var thread_coarsening: Int
    
    fn __init__(inout self):
        self.workgroup_size = 256
        self.simd_width = 8
        self.shared_memory_size = 32 * 1024
        self.cache_strategy = 1
        self.prefetch_distance = 2
        self.thread_coarsening = 1
    
    fn to_string(self) -> String:
        return f"""
        Optimization Parameters:
        - Workgroup Size: {self.workgroup_size}
        - SIMD Width: {self.simd_width}
        - Shared Memory: {self.shared_memory_size / 1024}KB
        - Cache Strategy: {self.cache_strategy}
        - Prefetch Distance: {self.prefetch_distance}
        - Thread Coarsening: {self.thread_coarsening}
        """

struct OptimizationResult:
    var parameters: OptimizationParameters
    var performance_gain: Float32
    var power_efficiency: Float32
    var memory_efficiency: Float32
    var overall_score: Float32
    
    fn __init__(inout self, params: OptimizationParameters):
        self.parameters = params
        self.performance_gain = 0.0
        self.power_efficiency = 0.0
        self.memory_efficiency = 0.0
        self.overall_score = 0.0
    
    fn to_string(self) -> String:
        return f"""
        Optimization Results:
        {self.parameters.to_string()}
        - Performance Gain: {self.performance_gain * 100:.1f}%
        - Power Efficiency: {self.power_efficiency * 100:.1f}%
        - Memory Efficiency: {self.memory_efficiency * 100:.1f}%
        - Overall Score: {self.overall_score * 100:.1f}%
        """

@value
struct AutoOptimizer:
    var device: MetalDevice
    var search_iterations: Int
    var population_size: Int
    var mutation_rate: Float32
    
    fn __init__(inout self, device: MetalDevice, 
                search_iterations: Int = 10,
                population_size: Int = 20,
                mutation_rate: Float32 = 0.1):
        self.device = device
        self.search_iterations = search_iterations
        self.population_size = population_size
        self.mutation_rate = mutation_rate
    
    fn optimize_kernel(self, metrics: KernelMetrics) raises -> OptimizationResult:
        var population = self._initialize_population()
        var best_result = OptimizationResult(population[0])
        
        for iteration in range(self.search_iterations):
            # Evaluate population
            var results = DynamicVector[OptimizationResult]()
            for params in population:
                let result = self._evaluate_parameters(params, metrics)
                results.append(result)
                
                if result.overall_score > best_result.overall_score:
                    best_result = result
            
            # Create next generation
            population = self._evolve_population(population, results)
        
        return best_result
    
    fn _initialize_population(self) -> DynamicVector[OptimizationParameters]:
        var population = DynamicVector[OptimizationParameters]()
        
        for i in range(self.population_size):
            var params = OptimizationParameters()
            
            # Randomize parameters
            params.workgroup_size = self._random_power_of_2(32, 1024)
            params.simd_width = self._random_power_of_2(4, 32)
            params.shared_memory_size = self._random_power_of_2(16 * 1024, 64 * 1024)
            params.cache_strategy = Int(random_float32() * 3)
            params.prefetch_distance = Int(random_float32() * 4) + 1
            params.thread_coarsening = Int(random_float32() * 4) + 1
            
            population.append(params)
        
        return population
    
    fn _evaluate_parameters(self, params: OptimizationParameters, 
                          metrics: KernelMetrics) -> OptimizationResult:
        var result = OptimizationResult(params)
        
        # Simulate performance with given parameters
        let theoretical_performance = self._estimate_performance(params, metrics)
        let theoretical_power = self._estimate_power_usage(params, metrics)
        let theoretical_memory = self._estimate_memory_efficiency(params, metrics)
        
        # Calculate relative gains
        result.performance_gain = theoretical_performance / metrics.calculate_efficiency() - 1.0
        result.power_efficiency = theoretical_power / metrics.hardware.power_consumption
        result.memory_efficiency = theoretical_memory / metrics.calculate_memory_efficiency()
        
        # Calculate overall score (weighted average)
        result.overall_score = (
            result.performance_gain * 0.5 +
            result.power_efficiency * 0.3 +
            result.memory_efficiency * 0.2
        )
        
        return result
    
    fn _evolve_population(self, 
                         population: DynamicVector[OptimizationParameters],
                         results: DynamicVector[OptimizationResult]
    ) -> DynamicVector[OptimizationParameters]:
        var new_population = DynamicVector[OptimizationParameters]()
        
        # Sort by score
        let sorted_indices = self._argsort(results, lambda x: x.overall_score)
        
        # Keep best performers
        let elite_count = self.population_size // 4
        for i in range(elite_count):
            new_population.append(population[sorted_indices[i]])
        
        # Create offspring through crossover and mutation
        while len(new_population) < self.population_size:
            let parent1 = self._select_parent(population, results)
            let parent2 = self._select_parent(population, results)
            let child = self._crossover(parent1, parent2)
            
            if random_float32() < self.mutation_rate:
                self._mutate(child)
            
            new_population.append(child)
        
        return new_population
    
    fn _estimate_performance(self, params: OptimizationParameters,
                           metrics: KernelMetrics) -> Float32:
        # Simplified performance model
        let base_performance = metrics.calculate_efficiency()
        var multiplier: Float32 = 1.0
        
        # Workgroup size impact
        multiplier *= min(1.0, Float32(params.workgroup_size) / 256.0)
        
        # SIMD efficiency
        multiplier *= min(1.0, Float32(params.simd_width) / 8.0)
        
        # Cache impact
        if params.cache_strategy > 0:
            multiplier *= 1.2
        
        # Thread coarsening impact
        multiplier *= min(1.0, sqrt(Float32(params.thread_coarsening)))
        
        return base_performance * multiplier
    
    fn _estimate_power_usage(self, params: OptimizationParameters,
                           metrics: KernelMetrics) -> Float32:
        # Simplified power model
        let base_power = metrics.hardware.power_consumption
        var multiplier: Float32 = 1.0
        
        # Workgroup size impact
        multiplier *= Float32(params.workgroup_size) / 256.0
        
        # SIMD impact
        multiplier *= Float32(params.simd_width) / 8.0
        
        # Cache impact
        multiplier *= 1.0 + Float32(params.cache_strategy) * 0.1
        
        # Thread coarsening impact
        multiplier *= Float32(params.thread_coarsening)
        
        return base_power * multiplier
    
    fn _estimate_memory_efficiency(self, params: OptimizationParameters,
                                 metrics: KernelMetrics) -> Float32:
        # Simplified memory model
        let base_efficiency = metrics.calculate_memory_efficiency()
        var multiplier: Float32 = 1.0
        
        # Cache impact
        if params.cache_strategy > 0:
            multiplier *= 1.3
        
        # Prefetch impact
        multiplier *= 1.0 + Float32(params.prefetch_distance) * 0.1
        
        # Shared memory impact
        multiplier *= min(1.0, Float32(params.shared_memory_size) / (32.0 * 1024.0))
        
        return base_efficiency * multiplier
    
    fn _random_power_of_2(self, min_val: Int, max_val: Int) -> Int:
        var val = min_val
        while val * 2 <= max_val and random_float32() < 0.5:
            val *= 2
        return val
    
    fn _select_parent(self, population: DynamicVector[OptimizationParameters],
                     results: DynamicVector[OptimizationResult]) -> OptimizationParameters:
        # Tournament selection
        let tournament_size = 3
        var best_idx = Int(random_float32() * len(population))
        var best_score = results[best_idx].overall_score
        
        for i in range(tournament_size - 1):
            let idx = Int(random_float32() * len(population))
            let score = results[idx].overall_score
            if score > best_score:
                best_idx = idx
                best_score = score
        
        return population[best_idx]
    
    fn _crossover(self, parent1: OptimizationParameters,
                  parent2: OptimizationParameters) -> OptimizationParameters:
        var child = OptimizationParameters()
        
        # Randomly select parameters from either parent
        if random_float32() < 0.5:
            child.workgroup_size = parent1.workgroup_size
        else:
            child.workgroup_size = parent2.workgroup_size
            
        if random_float32() < 0.5:
            child.simd_width = parent1.simd_width
        else:
            child.simd_width = parent2.simd_width
            
        if random_float32() < 0.5:
            child.shared_memory_size = parent1.shared_memory_size
        else:
            child.shared_memory_size = parent2.shared_memory_size
            
        if random_float32() < 0.5:
            child.cache_strategy = parent1.cache_strategy
        else:
            child.cache_strategy = parent2.cache_strategy
            
        if random_float32() < 0.5:
            child.prefetch_distance = parent1.prefetch_distance
        else:
            child.prefetch_distance = parent2.prefetch_distance
            
        if random_float32() < 0.5:
            child.thread_coarsening = parent1.thread_coarsening
        else:
            child.thread_coarsening = parent2.thread_coarsening
        
        return child
    
    fn _mutate(inout self, params: OptimizationParameters):
        # Randomly modify one parameter
        let mutation_type = Int(random_float32() * 6)
        
        if mutation_type == 0:
            params.workgroup_size = self._random_power_of_2(32, 1024)
        elif mutation_type == 1:
            params.simd_width = self._random_power_of_2(4, 32)
        elif mutation_type == 2:
            params.shared_memory_size = self._random_power_of_2(16 * 1024, 64 * 1024)
        elif mutation_type == 3:
            params.cache_strategy = Int(random_float32() * 3)
        elif mutation_type == 4:
            params.prefetch_distance = Int(random_float32() * 4) + 1
        else:
            params.thread_coarsening = Int(random_float32() * 4) + 1
    
    fn _argsort[T: AnyType](self, values: DynamicVector[T], 
                           key_fn: fn(T) -> Float32) -> DynamicVector[Int]:
        var indices = DynamicVector[Int]()
        for i in range(len(values)):
            indices.append(i)
        
        # Simple bubble sort
        let n = len(indices)
        for i in range(n):
            for j in range(0, n - i - 1):
                if key_fn(values[indices[j]]) < key_fn(values[indices[j + 1]]):
                    let temp = indices[j]
                    indices[j] = indices[j + 1]
                    indices[j + 1] = temp
        
        return indices 