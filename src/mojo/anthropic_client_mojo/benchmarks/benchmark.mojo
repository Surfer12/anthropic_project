"""
Benchmark Module for Anthropic Client Implementations

This module provides benchmarking tools to compare the performance
of different Anthropic client implementations.
"""

import time
from python import Python, PythonObject
from client import AnthropicClient, ClientConfig
from direct_client import DirectAnthropicClient, DirectClientConfig

# Import time module for benchmarking
var time_module = Python.import_module("time")

@value
struct BenchmarkResult:
    var implementation_name: String
    var total_time_ms: Float64
    var api_calls: Int
    var avg_time_per_call_ms: Float64
    
    fn __init__(mut self, name: String):
        self.implementation_name = name
        self.total_time_ms = 0.0
        self.api_calls = 0
        self.avg_time_per_call_ms = 0.0
    
    fn record_call(mut self, time_ms: Float64):
        self.total_time_ms += time_ms
        self.api_calls += 1
        self.avg_time_per_call_ms = self.total_time_ms / self.api_calls
    
    fn print_results(self):
        print("Benchmark Results for: " + self.implementation_name)
        print("  Total API Calls: " + str(self.api_calls))
        print("  Total Time: " + str(self.total_time_ms) + " ms")
        print("  Average Time per Call: " + str(self.avg_time_per_call_ms) + " ms")

fn benchmark_original_client(api_key: String, prompts: List[String]) raises -> BenchmarkResult:
    """
    Benchmark the original string-based client implementation.
    
    Args:
        api_key: API key for authentication
        prompts: List of prompts to test
    
    Returns:
        Benchmark results
    """
    var result = BenchmarkResult("Original String-Based Implementation")
    
    # Create original client
    var config = ClientConfig(
        api_key=api_key,
        model="claude-3-sonnet-20250219",
        temperature=0.7
    )
    var client = AnthropicClient(config)
    
    # Benchmark each prompt
    for prompt in prompts:
        # Record start time
        var start_time = time_module.time()
        
        # Call API
        var _ = client.get_response(prompt)
        
        # Record end time
        var end_time = time_module.time()
        var elapsed_ms = (end_time - start_time) * 1000.0
        
        # Record result
        result.record_call(elapsed_ms)
    
    return result

fn benchmark_direct_client(api_key: String, prompts: List[String]) raises -> BenchmarkResult:
    """
    Benchmark the direct API client implementation.
    
    Args:
        api_key: API key for authentication
        prompts: List of prompts to test
    
    Returns:
        Benchmark results
    """
    var result = BenchmarkResult("Direct API Implementation")
    
    # Create direct client
    var config = DirectClientConfig(
        api_key=api_key,
        model="claude-3-sonnet-20250219",
        temperature=0.7
    )
    var client = DirectAnthropicClient(config)
    
    # Benchmark each prompt
    for prompt in prompts:
        # Record start time
        var start_time = time_module.time()
        
        # Call API
        var _ = client.get_response(prompt)
        
        # Record end time
        var end_time = time_module.time()
        var elapsed_ms = (end_time - start_time) * 1000.0
        
        # Record result
        result.record_call(elapsed_ms)
    
    return result

fn run_benchmarks() raises:
    """Run benchmarks comparing different client implementations."""
    # Get API key
    var os_module = Python.import_module("os")
    var environ = os_module.environ
    var api_key = String(environ.get("ANTHROPIC_API_KEY", ""))
    
    if len(api_key) == 0:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        return
    
    # Define test prompts (short prompts to minimize API costs)
    var prompts = List[String]()
    prompts.append("What is 2+2?")
    prompts.append("Name a color.")
    prompts.append("Hello!")
    
    print("Running benchmarks with " + str(len(prompts)) + " prompts...")
    
    # Run benchmarks
    var original_result = benchmark_original_client(api_key, prompts)
    var direct_result = benchmark_direct_client(api_key, prompts)
    
    # Print results
    print("\nBenchmark Results:")
    print("=================")
    original_result.print_results()
    print("")
    direct_result.print_results()
    
    # Calculate improvement
    var improvement_pct = (original_result.avg_time_per_call_ms - direct_result.avg_time_per_call_ms) / original_result.avg_time_per_call_ms * 100.0
    print("\nPerformance Improvement: " + str(improvement_pct) + "%")

fn benchmark_initialization_overhead() raises:
    """Benchmark the initialization overhead of different client implementations."""
    # Get API key
    var os_module = Python.import_module("os")
    var environ = os_module.environ
    var api_key = String(environ.get("ANTHROPIC_API_KEY", ""))
    
    if len(api_key) == 0:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        return
    
    print("Benchmarking initialization overhead...")
    
    # Benchmark original client initialization
    var original_start = time_module.time()
    var _ = AnthropicClient(ClientConfig(api_key=api_key))
    var original_end = time_module.time()
    var original_init_ms = (original_end - original_start) * 1000.0
    
    # Benchmark direct client initialization
    var direct_start = time_module.time()
    var _ = DirectAnthropicClient(DirectClientConfig(api_key=api_key))
    var direct_end = time_module.time()
    var direct_init_ms = (direct_end - direct_start) * 1000.0
    
    # Print results
    print("\nInitialization Overhead:")
    print("=======================")
    print("Original Client: " + str(original_init_ms) + " ms")
    print("Direct Client: " + str(direct_init_ms) + " ms")
    
    # Calculate improvement
    var init_improvement_pct = (original_init_ms - direct_init_ms) / original_init_ms * 100.0
    print("Initialization Improvement: " + str(init_improvement_pct) + "%")

fn main() raises:
    """Main entry point for benchmarks."""
    print("Anthropic Client Benchmarks")
    print("==========================")
    
    # Run initialization benchmarks
    benchmark_initialization_overhead()
    
    # Run API call benchmarks
    run_benchmarks() 