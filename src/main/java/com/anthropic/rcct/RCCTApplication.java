package com.anthropic.rcct;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import com.anthropic.rcct.model.CCTModel;

@SpringBootApplication
public class RCCTApplication {

    public static void main(String[] args) {
        SpringApplication.run(RCCTApplication.class, args);
    }
    
    @Bean
    public CCTModel cctModel() {
        return new CCTModel();
    }
}