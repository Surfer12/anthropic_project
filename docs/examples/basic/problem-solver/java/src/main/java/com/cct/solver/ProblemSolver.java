package com.cct.solver;

import com.cct.framework.patterns.Pattern;
import com.cct.framework.ThoughtChain;
import com.cct.solver.model.Problem;
import com.cct.solver.model.Solution;
import com.cct.solver.model.Result;
import lombok.extern.slf4j.Slf4j;

import java.util.List;
import java.util.Map;

@Slf4j
public class ProblemSolver {
    private final ThoughtManager thoughtManager;
    private final PatternAnalyzer patternAnalyzer;
    private final DomainProcessor domainProcessor;

    public ProblemSolver() {
        this.thoughtManager = new ThoughtManager();
        this.patternAnalyzer = new PatternAnalyzer();
        this.domainProcessor = new DomainProcessor();
    }

    public Solution solve(Problem problem) {
        log.info("Starting problem solving process for: {}", problem.getName());
        validateProblem(problem);

        try {
            // Create thought chain
            ThoughtChain chain = thoughtManager.analyzeProblem(problem);
            log.debug("Created thought chain with {} thoughts", chain.getSize());

            // Analyze patterns
            List<Pattern.Match> patterns = patternAnalyzer.analyzeChain(chain);
            log.debug("Found {} pattern matches", patterns.size());

            // Process in domains
            Map<String, Object> analysisResult = domainProcessor.processAnalysis(
                Map.of(
                    "chain", chain,
                    "patterns", patterns,
                    "problem", problem
                )
            );
            log.debug("Analysis completed with confidence: {}", 
                     analysisResult.get("metrics.confidence"));

            Map<String, Object> solutionResult = domainProcessor.generateSolution(analysisResult);
            log.debug("Solution generated with type: {}", 
                     solutionResult.get("solution.type"));

            return createSolution(solutionResult);
        } catch (Exception e) {
            log.error("Error solving problem: {}", e.getMessage());
            throw new RuntimeException("Failed to solve problem", e);
        }
    }

    public Result applySolution(Solution solution) {
        log.info("Applying solution: {}", solution.getId());

        try {
            Map<String, Object> implementationResult = 
                domainProcessor.implementSolution(solution.toMap());

            return Result.builder()
                .success((Boolean) implementationResult.get("implemented"))
                .status((String) implementationResult.get("status"))
                .metrics((Map<String, Double>) implementationResult.get("metrics"))
                .build();
        } catch (Exception e) {
            log.error("Error applying solution: {}", e.getMessage());
            return Result.builder()
                .success(false)
                .status("error")
                .error(e.getMessage())
                .build();
        }
    }

    private void validateProblem(Problem problem) {
        if (!problem.isValid()) {
            throw new IllegalArgumentException("Invalid problem specification");
        }

        if (problem.isHighPriority()) {
            log.warn("Processing high priority problem: {}", problem.getName());
        }

        if (problem.requiresOptimization()) {
            log.info("Problem requires optimization strategies");
        }
    }

    private Solution createSolution(Map<String, Object> solutionResult) {
        return Solution.builder()
            .type((String) solutionResult.get("solution.type"))
            .steps((List<String>) solutionResult.get("solution.steps"))
            .parameters((Map<String, String>) solutionResult.get("solution.parameters"))
            .confidence((Double) solutionResult.get("confidence"))
            .build();
    }

    public void clearCache() {
        domainProcessor.clearCache();
        log.info("Solver cache cleared");
    }
} 