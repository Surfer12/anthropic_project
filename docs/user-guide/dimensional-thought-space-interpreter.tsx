import React, { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';

/**
 * DimensionalThoughtInterpreter Component
 * 
 * A meta-cognitive visualization system that demonstrates the transformation
 * between hierarchical ThoughtNode structures and dimensional thought space
 * representations, implementing the core cross-protocol bridge mechanisms.
 * 
 * The component renders both representations simultaneously and visualizes
 * the isomorphic mapping between them, with interactive capabilities for
 * exploring the transformation process and emergent properties.
 */
const DimensionalThoughtInterpreter = () => {
  // =========================================================================
  // Meta-cognitive state management (dimensional representation layer)
  // =========================================================================
  const [transformationState, setTransformationState] = useState(0); // 0-100%
  const [selectedNode, setSelectedNode] = useState(null);
  const [evaluationMethod, setEvaluationMethod] = useState('deterministic');
  const [metaCognitiveMode, setMetaCognitiveMode] = useState('episodic');
  const [thoughtMetrics, setThoughtMetrics] = useState({
    complexityScore: 0,
    coherenceRatio: 0,
    dimensionalEntropy: 0,
    recursiveDepth: 0
  });
  
  // References for visualization elements
  const hierarchicalRef = useRef(null);
  const dimensionalRef = useRef(null);
  const metricsCanvasRef = useRef(null);
  
  // =========================================================================
  // ThoughtNode Data Structure Definition (Hierarchical Protocol)
  // =========================================================================
  const hierarchicalThoughtData = {
    id: 'root',
    name: 'Core Concept',
    description: 'The central organizing principle of the thought structure',
    children: [
      {
        id: 'node1',
        name: 'Theoretical Foundation',
        description: 'Foundational principles and constructs',
        children: [
          {
            id: 'node1-1',
            name: 'Mathematical Models',
            description: 'Formal representations of conceptual structures',
            children: []
          },
          {
            id: 'node1-2',
            name: 'Cognitive Framework',
            description: 'Mental processing mechanisms and constraints',
            children: []
          }
        ]
      },
      {
        id: 'node2',
        name: 'Implementation Patterns',
        description: 'Patterns for practical realization',
        children: [
          {
            id: 'node2-1',
            name: 'Computational Architecture',
            description: 'System design and processing flow',
            children: []
          },
          {
            id: 'node2-2',
            name: 'Data Structures',
            description: 'Information organization and retrieval mechanisms',
            children: [
              {
                id: 'node2-2-1',
                name: 'Hierarchical Structures',
                description: 'Tree-based organizational patterns',
                children: []
              },
              {
                id: 'node2-2-2',
                name: 'Dimensional Structures',
                description: 'Vector space and manifold representations',
                children: []
              }
            ]
          }
        ]
      },
      {
        id: 'node3',
        name: 'Meta-Cognitive Layer',
        description: 'System for thought observation and analysis',
        children: [
          {
            id: 'node3-1',
            name: 'Evaluation Mechanisms',
            description: 'Methods for thought assessment and comparison',
            children: []
          },
          {
            id: 'node3-2',
            name: 'Reflection Capabilities',
            description: 'Self-observation and insight generation',
            children: []
          }
        ]
      }
    ]
  };
  
  // =========================================================================
  // Dimensional Thought Space Definition (Enhanced Protocol)
  // =========================================================================
  const generateDimensionalVectors = () => {
    // Convert hierarchical structure to dimensional vectors
    // This is a simplified representation of the dimensional thought space
    const dimensions = 5; // Number of conceptual dimensions
    const vectors = [];
    
    // Recursive function to process nodes
    const processNode = (node, depth = 0, path = []) => {
      // Create a vector for this node
      // In a real implementation, this would use more sophisticated embedding techniques
      const vector = Array(dimensions).fill(0).map((_, i) => {
        // Create a deterministic but varied vector based on node properties
        const baseValue = (node.id.charCodeAt(0) + i) % 10 / 10;
        const pathFactor = path.length > 0 ? path.reduce((sum, p, idx) => sum + p * (idx + 1), 0) / 100 : 0;
        const depthFactor = depth * 0.1;
        
        // Apply transformation based on current transformation state
        const transformFactor = transformationState / 100;
        const randomVariation = transformFactor * (Math.random() * 0.2 - 0.1);
        
        return baseValue + pathFactor + depthFactor + randomVariation;
      });
      
      vectors.push({
        id: node.id,
        name: node.name,
        description: node.description,
        vector,
        originalPath: [...path, node.id],
        depth
      });
      
      // Process children
      if (node.children && node.children.length > 0) {
        node.children.forEach((child, i) => {
          processNode(child, depth + 1, [...path, i]);
        });
      }
    };
    
    processNode(hierarchicalThoughtData);
    return vectors;
  };
  
  // Generate initial dimensional data
  const [dimensionalVectors, setDimensionalVectors] = useState(generateDimensionalVectors());
  
  // Update dimensional vectors when transformation state changes
  useEffect(() => {
    setDimensionalVectors(generateDimensionalVectors());
    
    // Update metrics based on transformation state
    const newMetrics = {
      complexityScore: 0.5 + transformationState / 200, // Increases with transformation
      coherenceRatio: 0.9 - transformationState / 500, // Slightly decreases with transformation
      dimensionalEntropy: 0.2 + transformationState / 200, // Increases with transformation
      recursiveDepth: Math.floor(3 + transformationState / 25) // Increases with transformation
    };
    setThoughtMetrics(newMetrics);
  }, [transformationState]);
  
  // =========================================================================
  // Evaluation Mechanism Implementation (Cross-Protocol Bridge)
  // =========================================================================
  const evaluateThought = (nodeId) => {
    // This simulates the bridge between deterministic and probabilistic evaluation
    const node = findNodeById(hierarchicalThoughtData, nodeId);
    const vector = dimensionalVectors.find(v => v.id === nodeId);
    
    if (!node || !vector) return null;
    
    // Calculate insights based on node properties and evaluation method
    let insights = [];
    
    if (evaluationMethod === 'deterministic') {
      // Deterministic evaluation based on hierarchical structure
      insights = [
        `Structural position: Depth level ${vector.depth}`,
        `Connectivity: ${countChildren(node)} direct connections`,
        `Hierarchical importance: ${5 - vector.depth}/5`,
        `Conceptual clarity: High`,
      ];
    } else {
      // Probabilistic evaluation based on dimensional space
      const dimensionalCentrality = calculateCentrality(vector.vector, dimensionalVectors);
      const nearestConcepts = findNearestConcepts(vector, dimensionalVectors, 3);
      
      insights = [
        `Dimensional centrality: ${dimensionalCentrality.toFixed(2)}`,
        `Conceptual neighborhood density: ${(nearestConcepts.avgDistance * 10).toFixed(2)}`,
        `Semantic distinctiveness: ${(1 - nearestConcepts.avgDistance).toFixed(2)}`,
        `Probabilistic importance: ${(dimensionalCentrality * (1 - nearestConcepts.avgDistance)).toFixed(2)}`,
        `Related concepts: ${nearestConcepts.nodes.map(n => n.name).join(', ')}`
      ];
    }
    
    return {
      node,
      vector,
      insights
    };
  };
  
  // Helper functions for evaluation
  const findNodeById = (rootNode, id) => {
    if (rootNode.id === id) return rootNode;
    
    if (rootNode.children && rootNode.children.length > 0) {
      for (const child of rootNode.children) {
        const found = findNodeById(child, id);
        if (found) return found;
      }
    }
    
    return null;
  };
  
  const countChildren = (node) => {
    return node.children ? node.children.length : 0;
  };
  
  const calculateCentrality = (vector, allVectors) => {
    // Calculate how central this vector is in the dimensional space
    const allDistances = allVectors
      .filter(v => v.id !== vector.id)
      .map(v => calculateVectorDistance(vector, v.vector));
    
    const avgDistance = allDistances.reduce((sum, d) => sum + d, 0) / allDistances.length;
    return 1 - avgDistance; // Higher centrality = lower average distance
  };
  
  const calculateVectorDistance = (v1, v2) => {
    // Euclidean distance between vectors
    if (!Array.isArray(v1) || !Array.isArray(v2)) return 1;
    
    return Math.sqrt(
      v1.reduce((sum, val, i) => sum + Math.pow(val - (v2[i] || 0), 2), 0)
    ) / Math.sqrt(v1.length); // Normalize by vector dimension
  };
  
  const findNearestConcepts = (targetVector, allVectors, count) => {
    const others = allVectors.filter(v => v.id !== targetVector.id);
    const withDistances = others.map(v => ({
      ...v,
      distance: calculateVectorDistance(targetVector.vector, v.vector)
    }));
    
    const sorted = withDistances.sort((a, b) => a.distance - b.distance);
    const nearest = sorted.slice(0, count);
    
    return {
      nodes: nearest,
      avgDistance: nearest.reduce((sum, n) => sum + n.distance, 0) / nearest.length
    };
  };
  
  // =========================================================================
  // Visualization Implementation
  // =========================================================================
  useEffect(() => {
    if (!hierarchicalRef.current || !dimensionalRef.current) return;
    
    // Clear previous visualizations
    d3.select(hierarchicalRef.current).selectAll("*").remove();
    d3.select(dimensionalRef.current).selectAll("*").remove();
    
    // Define dimensions
    const width = hierarchicalRef.current.clientWidth;
    const height = hierarchicalRef.current.clientHeight;
    
    // Create hierarchical tree visualization
    const hierarchicalViz = d3.select(hierarchicalRef.current)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", `translate(${width / 2}, 50)`);
    
    // Create tree layout
    const treeLayout = d3.tree().size([width - 100, height - 100]);
    
    // Convert data to hierarchy
    const root = d3.hierarchy(hierarchicalThoughtData);
    const treeData = treeLayout(root);
    
    // Add links
    hierarchicalViz.selectAll(".link")
      .data(treeData.links())
      .enter()
      .append("path")
      .attr("class", "link")
      .attr("d", d3.linkVertical()
        .x(d => d.x - width / 2)
        .y(d => d.y))
      .attr("fill", "none")
      .attr("stroke", "#6c757d")
      .attr("stroke-width", 1.5);
      
    // Add nodes
    const nodes = hierarchicalViz.selectAll(".node")
      .data(treeData.descendants())
      .enter()
      .append("g")
      .attr("class", d => `node ${d.data.id === selectedNode ? "selected" : ""}`)
      .attr("transform", d => `translate(${d.x - width / 2}, ${d.y})`)
      .on("click", (event, d) => {
        setSelectedNode(d.data.id);
      })
      .style("cursor", "pointer");
    
    // Add node circles
    nodes.append("circle")
      .attr("r", d => d.data.id === selectedNode ? 10 : 6)
      .attr("fill", d => {
        if (d.data.id === selectedNode) return "#e83e8c";
        if (d.depth === 0) return "#6610f2";
        if (d.depth === 1) return "#007bff";
        return "#20c997";
      })
      .attr("stroke", "#fff")
      .attr("stroke-width", 2);
    
    // Add node labels
    nodes.append("text")
      .attr("dy", d => d.children ? -12 : 18)
      .attr("text-anchor", "middle")
      .text(d => d.data.name)
      .attr("font-size", "12px")
      .attr("font-weight", d => d.data.id === selectedNode ? "bold" : "normal")
      .attr("fill", "#343a40");
    
    // Create dimensional space visualization using force-directed layout
    const dimensionalViz = d3.select(dimensionalRef.current)
      .append("svg")
      .attr("width", width)
      .attr("height", height);
    
    // Function to project n-dimensional vectors to 2D
    const projectToSurface = (vector, xDim = 0, yDim = 1) => {
      // Simple projection using two dimensions as x,y
      // In a real implementation, this would use more sophisticated techniques like t-SNE or UMAP
      const projectionX = (vector[xDim] || 0) * width * 0.8 + width * 0.1;
      const projectionY = (vector[yDim] || 0) * height * 0.8 + height * 0.1;
      return { x: projectionX, y: projectionY };
    };
    
    // Project vectors to 2D
    const projectedVectors = dimensionalVectors.map(v => ({
      ...v,
      ...projectToSurface(v.vector)
    }));
    
    // Create force simulation
    const simulation = d3.forceSimulation(projectedVectors)
      .force("charge", d3.forceManyBody().strength(-50))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(15))
      .force("x", d3.forceX(d => d.x).strength(0.5))
      .force("y", d3.forceY(d => d.y).strength(0.5));
    
    // Draw dimensional connections
    // This creates lines between related concepts in the dimensional space
    const connections = [];
    
    projectedVectors.forEach((v, i) => {
      const nearest = findNearestConcepts(v, projectedVectors, 2);
      nearest.nodes.forEach(target => {
        connections.push({
          source: v,
          target,
          strength: 1 - target.distance
        });
      });
    });
    
    const links = dimensionalViz.selectAll(".d-link")
      .data(connections)
      .enter()
      .append("line")
      .attr("class", "d-link")
      .attr("stroke", d => {
        const alpha = Math.min(1, d.strength * 2);
        return `rgba(102, 16, 242, ${alpha})`;
      })
      .attr("stroke-width", d => d.strength * 3);
    
    // Add dimensional nodes
    const dimNodes = dimensionalViz.selectAll(".d-node")
      .data(projectedVectors)
      .enter()
      .append("g")
      .attr("class", d => `d-node ${d.id === selectedNode ? "selected" : ""}`)
      .on("click", (event, d) => {
        setSelectedNode(d.id);
      })
      .style("cursor", "pointer");
    
    dimNodes.append("circle")
      .attr("r", d => d.id === selectedNode ? 10 : 6)
      .attr("fill", d => {
        if (d.id === selectedNode) return "#e83e8c";
        // Color by conceptual dimension (represented by first vector element)
        const dimValue = d.vector[0] * 5;
        if (dimValue < 1) return "#007bff";
        if (dimValue < 2) return "#6610f2";
        if (dimValue < 3) return "#6f42c1"; 
        if (dimValue < 4) return "#20c997";
        return "#fd7e14";
      })
      .attr("stroke", "#fff")
      .attr("stroke-width", 2);
    
    dimNodes.append("text")
      .attr("dy", 20)
      .attr("text-anchor", "middle")
      .text(d => d.name)
      .attr("font-size", "12px")
      .attr("font-weight", d => d.id === selectedNode ? "bold" : "normal")
      .attr("fill", "#343a40");
    
    // Update positions during simulation
    simulation.on("tick", () => {
      links
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
      
      dimNodes.attr("transform", d => `translate(${d.x}, ${d.y})`);
    });
    
    // Draw connection between selected node in both visualizations
    if (selectedNode) {
      const selectedHierarchicalNode = nodes.filter(d => d.data.id === selectedNode);
      const selectedDimNode = dimNodes.filter(d => d.id === selectedNode);
      
      if (!selectedHierarchicalNode.empty() && !selectedDimNode.empty()) {
        // Get positions
        const hierarchicalData = selectedHierarchicalNode.datum();
        const hierarchicalX = hierarchicalData.x - width / 2 + width / 2; // Adjust for the translation
        const hierarchicalY = hierarchicalData.y + 50; // Adjust for the translation
        
        const dimensionalData = selectedDimNode.datum();
        const dimensionalX = dimensionalData.x;
        const dimensionalY = dimensionalData.y;
        
        // Draw connection line between visualizations
        const bridgeSvg = d3.select(metricsCanvasRef.current)
          .append("svg")
          .attr("width", width)
          .attr("height", 100)
          .style("position", "absolute")
          .style("top", `${hierarchicalRef.current.clientHeight}px`)
          .style("left", "0")
          .style("pointer-events", "none");
        
        // Curved path between the two points
        const curvePoints = [
          { x: hierarchicalX, y: 0 },
          { x: (hierarchicalX + dimensionalX) / 2, y: 50 },
          { x: dimensionalX, y: 100 }
        ];
        
        const linePath = d3.line()
          .x(d => d.x)
          .y(d => d.y)
          .curve(d3.curveBasis);
        
        bridgeSvg.append("path")
          .attr("d", linePath(curvePoints))
          .attr("fill", "none")
          .attr("stroke", "#e83e8c")
          .attr("stroke-width", 2)
          .attr("stroke-dasharray", "5,5");
      }
    }
    
    // Cleanup function
    return () => {
      if (simulation) simulation.stop();
    };
  }, [hierarchicalThoughtData, dimensionalVectors, selectedNode]);
  
  // =========================================================================
  // Meta-Cognitive Analysis Visualization
  // =========================================================================
  useEffect(() => {
    if (!metricsCanvasRef.current) return;
    
    // Clear previous metrics visualization
    const previousSvg = d3.select(metricsCanvasRef.current).select("svg.metrics-viz");
    if (!previousSvg.empty()) previousSvg.remove();
    
    const width = metricsCanvasRef.current.clientWidth;
    const height = 100;
    const padding = 30;
    
    const metricsSvg = d3.select(metricsCanvasRef.current)
      .append("svg")
      .attr("class", "metrics-viz")
      .attr("width", width)
      .attr("height", height);
    
    // Metrics to display
    const metrics = [
      { name: "Complexity", value: thoughtMetrics.complexityScore, color: "#007bff" },
      { name: "Coherence", value: thoughtMetrics.coherenceRatio, color: "#20c997" },
      { name: "Entropy", value: thoughtMetrics.dimensionalEntropy, color: "#fd7e14" },
      { name: "Depth", value: thoughtMetrics.recursiveDepth / 10, color: "#6f42c1" } // Normalize to 0-1
    ];
    
    // Create scales
    const xScale = d3.scaleBand()
      .domain(metrics.map(d => d.name))
      .range([padding, width - padding])
      .padding(0.2);
    
    const yScale = d3.scaleLinear()
      .domain([0, 1])
      .range([height - padding, padding]);
    
    // Draw bars
    metricsSvg.selectAll(".metric-bar")
      .data(metrics)
      .enter()
      .append("rect")
      .attr("class", "metric-bar")
      .attr("x", d => xScale(d.name))
      .attr("y", d => yScale(d.value))
      .attr("width", xScale.bandwidth())
      .attr("height", d => height - padding - yScale(d.value))
      .attr("fill", d => d.color)
      .attr("rx", 3)
      .attr("ry", 3);
    
    // Add labels
    metricsSvg.selectAll(".metric-label")
      .data(metrics)
      .enter()
      .append("text")
      .attr("class", "metric-label")
      .attr("x", d => xScale(d.name) + xScale.bandwidth() / 2)
      .attr("y", height - padding / 2)
      .attr("text-anchor", "middle")
      .attr("font-size", "12px")
      .attr("fill", "#343a40")
      .text(d => d.name);
    
    // Add value labels
    metricsSvg.selectAll(".value-label")
      .data(metrics)
      .enter()
      .append("text")
      .attr("class", "value-label")
      .attr("x", d => xScale(d.name) + xScale.bandwidth() / 2)
      .attr("y", d => yScale(d.value) - 5)
      .attr("text-anchor", "middle")
      .attr("font-size", "10px")
      .attr("fill", "#343a40")
      .text(d => d.name === "Depth" ? Math.round(d.value * 10) : d.value.toFixed(2));
    
  }, [thoughtMetrics]);
  
  // =========================================================================
  // Component rendering
  // =========================================================================
  // Get evaluation results for selected node
  const evaluationResults = selectedNode ? evaluateThought(selectedNode) : null;

  return (
    <div className="dimensional-thought-interpreter" style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      fontFamily: 'Arial, sans-serif',
      color: '#343a40',
      backgroundColor: '#f8f9fa',
      padding: '16px'
    }}>
      <div className="interpreter-header" style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '16px'
      }}>
        <h2 style={{ margin: 0 }}>Dimensional Thought Space Interpreter</h2>
        
        <div className="controls" style={{
          display: 'flex',
          gap: '16px'
        }}>
          <div className="control-group">
            <label htmlFor="transformation-slider" style={{ marginRight: '8px' }}>
              Transformation: {transformationState}%
            </label>
            <input
              id="transformation-slider"
              type="range"
              min="0"
              max="100"
              value={transformationState}
              onChange={(e) => setTransformationState(parseInt(e.target.value))}
              style={{ width: '150px' }}
            />
          </div>
          
          <div className="control-group">
            <label htmlFor="evaluation-method" style={{ marginRight: '8px' }}>
              Evaluation:
            </label>
            <select
              id="evaluation-method"
              value={evaluationMethod}
              onChange={(e) => setEvaluationMethod(e.target.value)}
            >
              <option value="deterministic">Deterministic</option>
              <option value="probabilistic">Probabilistic</option>
            </select>
          </div>
          
          <div className="control-group">
            <label htmlFor="metacognitive-mode" style={{ marginRight: '8px' }}>
              Meta-Cognitive:
            </label>
            <select
              id="metacognitive-mode"
              value={metaCognitiveMode}
              onChange={(e) => setMetaCognitiveMode(e.target.value)}
            >
              <option value="episodic">Episodic</option>
              <option value="continuous">Continuous</option>
            </select>
          </div>
        </div>
      </div>
      
      <div className="visualization-container" style={{
        display: 'flex',
        flexDirection: 'column',
        flex: 1,
        gap: '16px'
      }}>
        <div className="visualization-row" style={{
          display: 'flex',
          height: '300px',
          gap: '16px'
        }}>
          <div className="hierarchical-view" style={{
            flex: 1,
            position: 'relative',
            border: '1px solid #dee2e6',
            borderRadius: '8px',
            backgroundColor: '#ffffff',
            overflow: 'hidden'
          }}>
            <div className="view-header" style={{
              padding: '8px 16px',
              borderBottom: '1px solid #dee2e6',
              backgroundColor: '#f8f9fa',
              fontWeight: 'bold'
            }}>
              Hierarchical Thought Structure
            </div>
            <div 
              ref={hierarchicalRef} 
              style={{ width: '100%', height: 'calc(100% - 37px)' }}
            ></div>
          </div>
          
          <div className="dimensional-view" style={{
            flex: 1,
            position: 'relative',
            border: '1px solid #dee2e6',
            borderRadius: '8px',
            backgroundColor: '#ffffff',
            overflow: 'hidden'
          }}>
            <div className="view-header" style={{
              padding: '8px 16px',
              borderBottom: '1px solid #dee2e6',
              backgroundColor: '#f8f9fa',
              fontWeight: 'bold'
            }}>
              Dimensional Thought Space
            </div>
            <div 
              ref={dimensionalRef} 
              style={{ width: '100%', height: 'calc(100% - 37px)' }}
            ></div>
          </div>
        </div>
        
        <div className="metrics-visualization" style={{
          border: '1px solid #dee2e6',
          borderRadius: '8px',
          backgroundColor: '#ffffff',
          padding: '16px',
          position: 'relative'
        }}>
          <h3 style={{ margin: '0 0 16px 0' }}>Meta-Cognitive Metrics</h3>
          <div ref={metricsCanvasRef} style={{ width: '100%', height: '100px' }}></div>
        </div>
        
        <div className="evaluation-results" style={{
          flex: 1,
          display: 'flex',
          gap: '16px'
        }}>
          <div className="evaluation-panel" style={{
            flex: 1,
            border: '1px solid #dee2e6',
            borderRadius: '8px',
            backgroundColor: '#ffffff',
            padding: '16px',
            minHeight: '200px'
          }}>
            <h3 style={{ margin: '0 0 16px 0' }}>
              {evaluationMethod === 'deterministic' ? 'Deterministic' : 'Probabilistic'} Evaluation
            </h3>
            
            {evaluationResults ? (
              <div>
                <div style={{ marginBottom: '16px' }}>
                  <h4 style={{ margin: '0 0 8px 0', color: '#007bff' }}>{evaluationResults.node.name}</h4>
                  <p style={{ margin: '0 0 8px 0', color: '#6c757d' }}>{evaluationResults.node.description}</p>
                </div>
                
                <div className="insights-container" style={{
                  backgroundColor: evaluationMethod === 'deterministic' ? '#4dabf715' : '#e83e8c15',
                  padding: '12px',
                  borderRadius: '4px',
                  borderLeft: `4px solid ${evaluationMethod === 'deterministic' ? '#4dabf7' : '#e83e8c'}`
                }}>
                  <h5 style={{ margin: '0 0 8px 0', color: evaluationMethod === 'deterministic' ? '#4dabf7' : '#e83e8c' }}>
                    Insights
                  </h5>
                  <ul style={{ margin: '0', paddingLeft: '20px' }}>
                    {evaluationResults.insights.map((insight, index) => (
                      <li key={index}>{insight}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ) : (
              <div style={{ color: '#6c757d', fontStyle: 'italic' }}>
                Select a node to view evaluation results
              </div>
            )}
          </div>
          
          <div className="meta-cognitive-panel" style={{
            flex: 1,
            border: '1px solid #dee2e6',
            borderRadius: '8px',
            backgroundColor: '#ffffff',
            padding: '16px',
            minHeight: '200px'
          }}>
            <h3 style={{ margin: '0 0 16px 0' }}>
              {metaCognitiveMode === 'episodic' ? 'Episodic' : 'Continuous'} Meta-Cognition
            </h3>
            
            <div style={{
              backgroundColor: metaCognitiveMode === 'episodic' ? '#ffc10715' : '#6f42c115',
              padding: '12px',
              borderRadius: '4px',
              borderLeft: `4px solid ${metaCognitiveMode === 'episodic' ? '#ffc107' : '#6f42c1'}`
            }}>
              <h5 style={{ margin: '0 0 8px 0', color: metaCognitiveMode === 'episodic' ? '#ffc107' : '#6f42c1' }}>
                System Self-Assessment
              </h5>
              
              {metaCognitiveMode === 'episodic' ? (
                <div>
                  <p>Processing completed evaluation with {transformationState}% transformation applied.</p>
                  <p>Thought structure contains {dimensionalVectors.length} nodes across {thoughtMetrics.recursiveDepth} recursive levels.</p>
                  <p>Overall coherence assessment: {thoughtMetrics.coherenceRatio.toFixed(2)} out of 1.0</p>
                </div>
              ) : (
                <div>
                  <p>Continuous monitoring active. Current state metrics:</p>
                  <ul style={{ margin: '8px 0', paddingLeft: '20px' }}>
                    <li>Transformation progression: {transformationState}% complete</li>
                    <li>Dimensional entropy: {thoughtMetrics.dimensionalEntropy.toFixed(3)} (increasing)</li>
                    <li>Vector space stability: {(1 - thoughtMetrics.dimensionalEntropy).toFixed(3)} (decreasing)</li>
                    <li>Recursive path integrity: {(thoughtMetrics.coherenceRatio * 100).toFixed(1)}%</li>
                  </ul>
                  <p style={{ fontStyle: 'italic' }}>
                    {transformationState < 30 
                      ? "Early transformation phase. Hierarchical structure dominant."
                      : transformationState < 70 
                        ? "Intermediate transformation. Hybrid representation active."
                        : "Advanced transformation. Dimensional structure emerging."}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DimensionalThoughtInterpreter;