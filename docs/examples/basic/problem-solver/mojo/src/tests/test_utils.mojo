from tensor import Tensor
from math import sqrt, exp
from utils.vector import DynamicVector

struct TestCase:
    var name: String
    var expected: Float32
    var tolerance: Float32
    
    fn __init__(inout self, name: String, expected: Float32, tolerance: Float32 = 0.001):
        self.name = name
        self.expected = expected
        self.tolerance = tolerance
    
    fn check(self, actual: Float32) -> Bool:
        return abs(actual - self.expected) <= self.tolerance

struct TestResult:
    var name: String
    var passed: Bool
    var message: String
    
    fn __init__(inout self, name: String, passed: Bool, message: String = ""):
        self.name = name
        self.passed = passed
        self.message = message

struct TestSuite:
    var name: String
    var results: DynamicVector[TestResult]
    
    fn __init__(inout self, name: String):
        self.name = name
        self.results = DynamicVector[TestResult]()
    
    fn add_result(inout self, result: TestResult):
        self.results.append(result)
    
    fn print_summary(self):
        print(f"\nTest Suite: {self.name}")
        print("=" * (len(self.name) + 12))
        
        var passed = 0
        var failed = 0
        
        for result in self.results:
            if result.passed:
                passed += 1
                print(f"✓ {result.name}")
            else:
                failed += 1
                print(f"✗ {result.name}")
                if result.message:
                    print(f"  Error: {result.message}")
        
        print("\nSummary:")
        print(f"Total Tests: {len(self.results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed * 100) / len(self.results):.1f}%")

fn generate_test_tensor(size: Int, pattern: String = "random") -> Tensor[DType.float32]:
    var tensor = Tensor[DType.float32](size)
    
    if pattern == "random":
        for i in range(size):
            tensor[i] = random_float32()
    elif pattern == "sequential":
        for i in range(size):
            tensor[i] = Float32(i)
    elif pattern == "constant":
        for i in range(size):
            tensor[i] = 1.0
    elif pattern == "alternating":
        for i in range(size):
            tensor[i] = Float32(i % 2)
    
    return tensor

fn generate_test_matrix(rows: Int, cols: Int, pattern: String = "random") -> Tensor[DType.float32]:
    var matrix = Tensor[DType.float32](rows, cols)
    
    if pattern == "random":
        for i in range(rows):
            for j in range(cols):
                matrix[i, j] = random_float32()
    elif pattern == "identity":
        for i in range(rows):
            for j in range(cols):
                matrix[i, j] = 1.0 if i == j else 0.0
    elif pattern == "sequential":
        for i in range(rows):
            for j in range(cols):
                matrix[i, j] = Float32(i * cols + j)
    
    return matrix

fn compare_tensors(t1: Tensor[DType.float32], t2: Tensor[DType.float32], tolerance: Float32 = 0.001) -> Bool:
    if len(t1) != len(t2):
        return False
    
    for i in range(len(t1)):
        if abs(t1[i] - t2[i]) > tolerance:
            return False
    
    return True

fn compare_matrices(m1: Tensor[DType.float32], m2: Tensor[DType.float32], tolerance: Float32 = 0.001) -> Bool:
    if m1.shape[0] != m2.shape[0] or m1.shape[1] != m2.shape[1]:
        return False
    
    let rows = m1.shape[0]
    let cols = m1.shape[1]
    
    for i in range(rows):
        for j in range(cols):
            if abs(m1[i, j] - m2[i, j]) > tolerance:
                return False
    
    return True

fn measure_execution_time(fn_to_measure: fn() raises -> None) raises -> Int64:
    let start_time = now()
    fn_to_measure()
    let end_time = now()
    return end_time - start_time

fn benchmark_operation(fn_to_benchmark: fn() raises -> None, num_iterations: Int = 100) raises -> Float64:
    var total_time: Int64 = 0
    
    for i in range(num_iterations):
        total_time += measure_execution_time(fn_to_benchmark)
    
    return Float64(total_time) / Float64(num_iterations * 1_000_000)  # Convert to milliseconds

fn verify_gpu_results(cpu_result: Tensor[DType.float32], 
                     gpu_result: Tensor[DType.float32],
                     tolerance: Float32 = 0.001) -> TestResult:
    let matches = compare_tensors(cpu_result, gpu_result, tolerance)
    if matches:
        return TestResult("GPU Result Verification", True)
    else:
        var message = "GPU results do not match CPU results.\n"
        message += f"Max difference: {calculate_max_difference(cpu_result, gpu_result)}"
        return TestResult("GPU Result Verification", False, message)

fn calculate_max_difference(t1: Tensor[DType.float32], t2: Tensor[DType.float32]) -> Float32:
    var max_diff: Float32 = 0.0
    for i in range(len(t1)):
        let diff = abs(t1[i] - t2[i])
        if diff > max_diff:
            max_diff = diff
    return max_diff

fn verify_performance_improvement(cpu_time: Float64, 
                               gpu_time: Float64,
                               min_speedup: Float64 = 2.0) -> TestResult:
    let speedup = cpu_time / gpu_time
    if speedup >= min_speedup:
        return TestResult(
            "Performance Improvement",
            True,
            f"Achieved {speedup:.1f}x speedup"
        )
    else:
        return TestResult(
            "Performance Improvement",
            False,
            f"Expected {min_speedup:.1f}x speedup, got {speedup:.1f}x"
        ) 