package com.anthropic.rcct.service;

import com.anthropic.rcct.model.CCTModel;
import com.anthropic.rcct.model.ThoughtNode;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class ThoughtProcessingService {
    
    public CCTModel createNewModel(String name, String description) {
        CCTModel model = new CCTModel();
        model.setName(name);
        model.setDescription(description);
        return model;
    }
    
    public ThoughtNode addThought(CCTModel model, String content, String type, Integer depth, String parentId) {
        ThoughtNode thought = new ThoughtNode();
        thought.setContent(content);
        thought.setType(type);
        thought.setDepth(depth);
        thought.setParentId(parentId);
        
        if (model.getThoughts() == null) {
            model.setThoughts(List.of(thought));
        } else {
            model.getThoughts().add(thought);
        }
        
        return thought;
    }
    
    public Optional<ThoughtNode> findThoughtById(CCTModel model, Long thoughtId) {
        return model.getThoughts().stream()
                .filter(t -> t.getId().equals(thoughtId))
                .findFirst();
    }
    
    public List<ThoughtNode> findThoughtsByType(CCTModel model, String type) {
        return model.getThoughts().stream()
                .filter(t -> t.getType().equals(type))
                .toList();
    }
    
    public List<ThoughtNode> findThoughtsByDepth(CCTModel model, Integer depth) {
        return model.getThoughts().stream()
                .filter(t -> t.getDepth().equals(depth))
                .toList();
    }
} 