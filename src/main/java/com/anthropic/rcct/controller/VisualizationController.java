package com.anthropic.rcct.controller;

import com.anthropic.rcct.model.CCTModel;
import com.anthropic.rcct.model.ThoughtNode;
import com.anthropic.rcct.service.ThoughtProcessingService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * REST controller for managing the visualization of cognitive chains of thought.
 * 
 * This controller provides endpoints for viewing and manipulating thought visualizations,
 * including creating new thoughts, retrieving existing thoughts, and displaying
 * visual representations of thought chains.
 */
@Controller
@RequestMapping("/api/visualization")
public class VisualizationController {

    private final ThoughtProcessingService thoughtProcessingService;
    
    /**
     * Constructs a new VisualizationController with the specified thought processing service.
     * 
     * @param thoughtProcessingService The service to be used for thought processing operations
     */
    @Autowired
    public VisualizationController(ThoughtProcessingService thoughtProcessingService) {
        this.thoughtProcessingService = thoughtProcessingService;
    }
    
    /**
     * Displays the main visualization interface.
     * 
     * @return The name of the visualization view template
     */
    @GetMapping("/")
    public String showVisualization() {
        return "interactive-integration-explorer";
    }
    
    /**
     * Retrieves all thoughts for visualization.
     * 
     * @return ResponseEntity containing a list of thought data mapped as key-value pairs
     */
    @GetMapping("/thoughts")
    @ResponseBody
    public ResponseEntity<List<Map<String, Object>>> getThoughts() {
        // In a real implementation, this would fetch data from a repository
        // For now, let's create some sample data
        CCTModel model = new CCTModel();
        ThoughtNode thought = thoughtProcessingService.createThought(model, "Sample thought", "core", 0, null);
        
        // Create a serializable representation
        Map<String, Object> thoughtMap = new HashMap<>();
        thoughtMap.put("id", thought.getId());
        thoughtMap.put("content", thought.getContent());
        thoughtMap.put("type", thought.getType());
        thoughtMap.put("depth", thought.getDepth());
        thoughtMap.put("parentId", thought.getParentId());
        
        return ResponseEntity.ok(List.of(thoughtMap));
    }
    
    /**
     * Creates a new thought and adds it to the visualization.
     * 
     * @param thoughtData Map containing the thought data including content, type, depth, and parentId
     * @return ResponseEntity containing the created thought data
     */
    @PostMapping("/thoughts")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> createThought(@RequestBody Map<String, Object> thoughtData) {
        // This would create a new thought in a real implementation
        // For now, just echo back the input
        return ResponseEntity.ok(thoughtData);
    }
}