package com.anthropic.rcct.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * Controller for handling homepage and redirects.
 */
@Controller
public class HomeController {

    /**
     * Handles the root URL and redirects to the visualization interface.
     * 
     * @return A redirect to the visualization page
     */
    @GetMapping("/")
    public String home() {
        return "redirect:/api/visualization/";
    }
} 