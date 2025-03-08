package com.anthropic.rcct;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import com.anthropic.rcct.model.CCTModel;

/**
 * Main application class for the Recursive Cognitive Chain of Thought (RCCT) system.
 * 
 * This Spring Boot application provides a platform for creating, analyzing, and visualizing
 * cognitive chains of thought through recursive processing and meta-cognitive operations.
 */
@SpringBootApplication
public class RCCTApplication {

    /**
     * Main entry point for the RCCT application.
     * 
     * @param args Command line arguments passed to the application
     */
    public static void main(String[] args) {
        SpringApplication.run(RCCTApplication.class, args);
    }
    
    /**
     * Creates and configures the main CCT model bean for the application.
     * 
     * @return A new instance of CCTModel to be used throughout the application
     */
    @Bean
    public CCTModel cctModel() {
        return new CCTModel();
    }
}