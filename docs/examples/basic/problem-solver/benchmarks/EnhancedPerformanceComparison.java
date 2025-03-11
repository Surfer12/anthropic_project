package com.cct.solver.benchmarks;

import com.cct.solver.ProblemSolver;
import com.cct.solver.model.Problem;
import com.cct.solver.model.Solution;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

import java.util.concurrent.TimeUnit;
import java.util.Random;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@State(Scope.Thread)
@Fork(value = 2)
@Warmup(iterations = 3)
@Measurement(iterations = 5)
public class EnhancedPerformanceComparison {
    private ProblemSolver solver;
    private Problem[] testProblems;
    private Random random;
    
    @Setup
    public void setup() {
        solver = new ProblemSolver();
        random = new Random(42); // Fixed seed for reproducibility
        testProblems = createTestProblems();
    }
    
    private Problem[] createTestProblems() {
        Problem[] problems = new Problem[4];
        
        // Simple problem
        problems[0] = Problem.builder()
            .name("Simple Optimization")
            .description("Basic performance optimization")
            .constraint("memory < 1GB")
            .constraint("latency < 100ms")
            .successCriterion("10% improvement")
            .type(Problem.ProblemType.OPTIMIZATION)
            .priority(Problem.ProblemPriority.LOW)
            .build();
            
        // Complex problem
        problems[1] = Problem.builder()
            .name("Complex Analysis")
            .description("Multi-factor system analysis")
            .constraint("CPU usage < 60%")
            .constraint("memory < 2GB")
            .constraint("network latency < 50ms")
            .constraint("disk I/O < 1000 IOPS")
            .successCriterion("30% overall improvement")
            .successCriterion("99.9% availability")
            .type(Problem.ProblemType.ANALYSIS)
            .priority(Problem.ProblemPriority.HIGH)
            .build();
            
        // Design problem
        problems[2] = Problem.builder()
            .name("System Design")
            .description("Microservices architecture design")
            .constraint("scalable to 1M users")
            .constraint("multi-region deployment")
            .constraint("eventual consistency")
            .successCriterion("handles 10k TPS")
            .successCriterion("99.99% availability")
            .type(Problem.ProblemType.DESIGN)
            .priority(Problem.ProblemPriority.MEDIUM)
            .build();
            
        // Implementation problem
        problems[3] = Problem.builder()
            .name("Feature Implementation")
            .description("Real-time analytics pipeline")
            .constraint("processing latency < 10ms")
            .constraint("accuracy > 95%")
            .constraint("fault-tolerant")
            .successCriterion("processes 100k events/sec")
            .type(Problem.ProblemType.IMPLEMENTATION)
            .priority(Problem.ProblemPriority.HIGH)
            .build();
            
        return problems;
    }
    
    @Benchmark
    @BenchmarkMode(Mode.AverageTime)
    @OutputTimeUnit(TimeUnit.MILLISECONDS)
    public void benchmarkSimpleProblem(Blackhole blackhole) {
        Solution solution = solver.solve(testProblems[0]);
        blackhole.consume(solution);
    }
    
    @Benchmark
    @BenchmarkMode(Mode.AverageTime)
    @OutputTimeUnit(TimeUnit.MILLISECONDS)
    public void benchmarkComplexProblem(Blackhole blackhole) {
        Solution solution = solver.solve(testProblems[1]);
        blackhole.consume(solution);
    }
    
    @Benchmark
    @BenchmarkMode(Mode.Throughput)
    @OutputTimeUnit(TimeUnit.SECONDS)
    public void benchmarkThroughput(Blackhole blackhole) {
        Problem problem = testProblems[random.nextInt(testProblems.length)];
        Solution solution = solver.solve(problem);
        blackhole.consume(solution);
    }
    
    @Benchmark
    @BenchmarkMode(Mode.SampleTime)
    @OutputTimeUnit(TimeUnit.MICROSECONDS)
    public void benchmarkLatency(Blackhole blackhole) {
        Problem problem = testProblems[random.nextInt(testProblems.length)];
        Solution solution = solver.solve(problem);
        blackhole.consume(solution);
    }
    
    public static void main(String[] args) throws RunnerException {
        Options opt = new OptionsBuilder()
            .include(EnhancedPerformanceComparison.class.getSimpleName())
            .forks(2)
            .warmupIterations(3)
            .measurementIterations(5)
            .build();

        new Runner(opt).run();
    }
} 