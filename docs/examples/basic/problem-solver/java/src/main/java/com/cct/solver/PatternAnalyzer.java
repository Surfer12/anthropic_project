package com.cct.solver;

import com.cct.framework.patterns.Pattern;
import com.cct.framework.patterns.StructuralPattern;
import com.cct.framework.patterns.BehavioralPattern;
import com.cct.framework.patterns.PatternMatcher;
import com.cct.framework.ThoughtChain;
import lombok.extern.slf4j.Slf4j;

import java.util.List;
import java.util.ArrayList;

@Slf4j
public class PatternAnalyzer {
    private final PatternMatcher matcher;
    private final List<Pattern> patterns;

    public PatternAnalyzer() {
        this.matcher = new PatternMatcher();
        this.patterns = new ArrayList<>();
        initializePatterns();
    }

    private void initializePatterns() {
        // Problem structure pattern
        StructuralPattern problemPattern = StructuralPattern.builder()
            .name("Problem Structure")
            .addNode("problem", 1)
            .addNode("constraint", 1, Integer.MAX_VALUE)
            .addNode("success_criterion", 1, Integer.MAX_VALUE)
            .build();

        // Solution approach pattern
        BehavioralPattern solutionPattern = BehavioralPattern.builder()
            .name("Solution Approach")
            .addStep("analyze_constraints")
            .addStep("generate_solutions")
            .addStep("evaluate_solutions")
            .addStep("select_solution")
            .addTransition("analyze_constraints", "generate_solutions")
            .addTransition("generate_solutions", "evaluate_solutions")
            .addTransition("evaluate_solutions", "select_solution")
            .build();

        // Register patterns
        patterns.add(problemPattern);
        patterns.add(solutionPattern);
        patterns.forEach(matcher::addPattern);
    }

    public List<Pattern.Match> analyzeChain(ThoughtChain chain) {
        log.debug("Analyzing chain: {}", chain.getName());
        List<Pattern.Match> matches = new ArrayList<>();

        for (Pattern pattern : patterns) {
            try {
                List<Pattern.Match> patternMatches = matcher.findMatches(chain, pattern);
                matches.addAll(patternMatches);
                log.debug("Found {} matches for pattern {}", patternMatches.size(), pattern.getName());
            } catch (Exception e) {
                log.error("Error matching pattern {}: {}", pattern.getName(), e.getMessage());
            }
        }

        return matches;
    }

    public boolean validatePattern(Pattern pattern, ThoughtChain chain) {
        try {
            return matcher.validate(pattern, chain);
        } catch (Exception e) {
            log.error("Error validating pattern {}: {}", pattern.getName(), e.getMessage());
            return false;
        }
    }

    public void addCustomPattern(Pattern pattern) {
        patterns.add(pattern);
        matcher.addPattern(pattern);
        log.info("Added custom pattern: {}", pattern.getName());
    }
} 