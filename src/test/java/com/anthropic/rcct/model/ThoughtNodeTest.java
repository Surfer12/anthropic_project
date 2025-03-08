package com.anthropic.rcct.model;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ThoughtNodeTest {

    @Test
    public void testGettersAndSetters() {
        // Create a ThoughtNode using the no-args constructor
        ThoughtNode node = new ThoughtNode();
        
        // Set values using Lombok-generated setters
        node.setId(1L);
        node.setContent("Test Content");
        node.setType("Question");
        node.setDepth(2);
        node.setParentId(null);
        node.setMetadata("{\"key\": \"value\"}");
        
        // Verify values using Lombok-generated getters
        assertEquals(1L, node.getId());
        assertEquals("Test Content", node.getContent());
        assertEquals("Question", node.getType());
        assertEquals(2, node.getDepth());
        assertNull(node.getParentId());
        assertEquals("{\"key\": \"value\"}", node.getMetadata());
    }
    
    @Test
    public void testAllArgsConstructor() {
        // Create a ThoughtNode using the all-args constructor
        ThoughtNode node = new ThoughtNode(
            2L, 
            "Another Content",
            "Answer",
            3,
            1L,
            "{\"author\": \"user\"}"
        );
        
        // Verify values
        assertEquals(2L, node.getId());
        assertEquals("Another Content", node.getContent());
        assertEquals("Answer", node.getType());
        assertEquals(3, node.getDepth());
        assertEquals(1L, node.getParentId());
        assertEquals("{\"author\": \"user\"}", node.getMetadata());
    }
}