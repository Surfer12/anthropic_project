package com.anthropic.rcct.controller;

import com.anthropic.rcct.model.CCTModel;
import com.anthropic.rcct.model.ThoughtNode;
import com.anthropic.rcct.service.ThoughtProcessingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping("/visualize")
public class VisualizationController {
    
    private final ThoughtProcessingService thoughtService;
    
    @Autowired
    public VisualizationController(ThoughtProcessingService thoughtService) {
        this.thoughtService = thoughtService;
    }
    
    @GetMapping
    public String visualizationHome(Model model) {
        CCTModel cctModel = thoughtService.createNewModel("Example Model", "A demonstration of the CCT visualization");
        model.addAttribute("cctModel", cctModel);
        return "visualization";
    }
    
    @PostMapping("/thought")
    @ResponseBody
    public ThoughtNode addThought(@RequestBody ThoughtNode thought) {
        CCTModel currentModel = thoughtService.createNewModel("Current Model", "Active visualization model");
        return thoughtService.addThought(
            currentModel,
            thought.getContent(),
            thought.getType(),
            thought.getDepth(),
            thought.getParentId()
        );
    }
    
    @GetMapping("/thoughts/{type}")
    @ResponseBody
    public List<ThoughtNode> getThoughtsByType(@PathVariable String type) {
        CCTModel currentModel = thoughtService.createNewModel("Current Model", "Active visualization model");
        return thoughtService.findThoughtsByType(currentModel, type);
    }
} 