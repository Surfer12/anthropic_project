package com.anthropic.rcct;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/**
 * Main application class for the Recursive Chain of Thought (RCCT) framework.
 * This Spring Boot application implements a cross-domain integration between
 * computational, cognitive, and representational systems.
 */
@SpringBootApplication
@EntityScan(basePackages = "com.anthropic.rcct.model")
@EnableJpaRepositories(basePackages = "com.anthropic.rcct.repository")
public class RCCTApplication {

    /**
     * Main entry point for the RCCT application.
     * 
     * @param args Command line arguments passed to the application
     */
    public static void main(String[] args) {
        SpringApplication.run(RCCTApplication.class, args);
    }
}