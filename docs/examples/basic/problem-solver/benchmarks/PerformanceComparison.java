package com.cct.solver.benchmarks;

import com.cct.solver.ProblemSolver;
import com.cct.solver.model.Problem;
import com.cct.solver.model.Solution;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@State(Scope.Thread)
@Fork(value = 2)
@Warmup(iterations = 3)
@Measurement(iterations = 5)
public class PerformanceComparison {
    private ProblemSolver javaSolver;
    private Problem testProblem;

    @Setup
    public void setup() {
        javaSolver = new ProblemSolver();
        testProblem = createTestProblem();
    }

    private Problem createTestProblem() {
        return Problem.builder()
            .name("Performance Test Problem")
            .description("Testing solver performance")
            .constraint("memory < 1GB")
            .constraint("latency < 100ms")
            .successCriterion("30% performance improvement")
            .type(Problem.ProblemType.OPTIMIZATION)
            .priority(Problem.ProblemPriority.HIGH)
            .build();
    }

    @Benchmark
    public Solution benchmarkJavaSolver() {
        return javaSolver.solve(testProblem);
    }

    public static void main(String[] args) throws RunnerException {
        Options opt = new OptionsBuilder()
            .include(PerformanceComparison.class.getSimpleName())
            .build();

        new Runner(opt).run();
    }
} 