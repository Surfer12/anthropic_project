import React, { useState, useEffect, useCallback, useRef } from 'react';
import { motion } from 'framer-motion';

// Define color constants for consistent styling
const COLORS = {
  background: '#f8f9fa',
  border: '#343a40',
  computational: '#4dabf7',
  cognitive: '#20c997',
  representational: '#e83e8c',
  metacognitive: '#ffc107',
  bridge: '#dc3545',
  highlight: '#6610f2',
  text: {
    primary: '#343a40',
    secondary: '#6c757d',
    light: '#ffffff'
  }
};

/**
 * Component: ProtocolVisualizer
 * 
 * A meta-cognitive visualization framework that recursively represents
 * the integration between hierarchical and dimensional thought protocols.
 */
const ProtocolVisualizer = () => {
  // Dimensional meta-state management for cross-protocol representation
  const [activeComponent, setActiveComponent] = useState(null);
  const [activeBridge, setActiveBridge] = useState(null);
  const [dimensionalMode, setDimensionalMode] = useState(false);
  const [transformationState, setTransformationState] = useState(0); // 0-100% transformation state
  
  // Refs for measurement and animation coordination
  const containerRef = useRef(null);
  const svgRef = useRef(null);
  
  // Protocol component definitions with cross-domain properties
  const protocolComponents = {
    // Original protocol components
    sensorProcessing: {
      id: 'sensorProcessing',
      title: 'Sensor Processing & Environmental Mapping',
      domain: 'computational',
      status: 'PRESERVED',
      description: 'Multi-modal sensor fusion with environmental reconstruction',
      implementation: {
        original: 'Direct stream processing with feature extraction',
        enhanced: 'Unchanged, with standardized integration interface',
      },
      position: { x: 150, y: 120, width: 250, height: 70 }
    },
    thoughtNode: {
      id: 'thoughtNode',
      title: 'Hierarchical ThoughtNode Structure',
      domain: 'representational',
      status: 'TRANSFORMED',
      description: 'Tree-based representation with explicit parent-child relationships',
      implementation: {
        original: 'Recursive data structure with pointer references',
        enhanced: 'Projection from dimensional vectors to hierarchical visualization',
      },
      position: { x: 150, y: 210, width: 250, height: 90 }
    },
    evaluation: {
      id: 'evaluation',
      title: 'Deterministic Evaluation',
      domain: 'cognitive',
      status: 'TRANSFORMED',
      description: 'Depth-first traversal with explicit memoization',
      implementation: {
        original: 'Recursion with cached results indexed by node IDs',
        enhanced: 'Special case of probabilistic evaluation with certainty = 1.0',
      },
      position: { x: 150, y: 320, width: 250, height: 90 }
    },
    metaCognitive: {
      id: 'metaCognitive',
      title: 'Post-Process Meta-Cognitive Analysis',
      domain: 'metacognitive',
      status: 'TRANSFORMED',
      description: 'Retrospective analysis of completed thought chains',
      implementation: {
        original: 'Sequential processing after evaluation completion',
        enhanced: 'Synchronization points with continuous monitoring',
      },
      position: { x: 150, y: 430, width: 250, height: 70 }
    },
    visualization: {
      id: 'visualization',
      title: 'Visualization & Accessibility Layers',
      domain: 'computational',
      status: 'BRIDGED',
      description: 'Rendering of thought structures with interaction mechanics',
      implementation: {
        original: 'Tree visualization with navigation controls',
        enhanced: 'Dimensional projection with topological navigation',
      },
      position: { x: 150, y: 520, width: 250, height: 70 }
    },
    
    // Enhanced protocol components
    dimensionalSensorProcessing: {
      id: 'dimensionalSensorProcessing',
      title: 'Sensor Processing & Environmental Mapping',
      domain: 'computational',
      status: 'UNCHANGED',
      description: 'Multi-modal sensor fusion with environmental reconstruction',
      implementation: {
        original: 'Direct stream processing with feature extraction',
        enhanced: 'Unchanged, with standardized integration interface',
      },
      position: { x: 550, y: 120, width: 250, height: 70 }
    },
    dimensionalThoughtSpace: {
      id: 'dimensionalThoughtSpace',
      title: 'Dimensional Thought Space',
      domain: 'representational',
      status: 'CORE TRANSFORMATION',
      description: 'Topological manifold with semantic distance metrics',
      implementation: {
        original: 'N/A - Fundamental paradigm shift',
        enhanced: 'Tensor representation with geometric operations',
      },
      position: { x: 550, y: 210, width: 250, height: 90 },
      dimensions: 5 // Number of dimensions visualized in example
    },
    probabilisticEvaluation: {
      id: 'probabilisticEvaluation',
      title: 'Probabilistic Evaluation',
      domain: 'cognitive',
      status: 'CORE TRANSFORMATION',
      description: 'Importance-weighted sampling with fuzzy memoization',
      implementation: {
        original: 'N/A - Fundamental paradigm shift',
        enhanced: 'Monte Carlo traversal with Bayesian updating',
      },
      position: { x: 550, y: 320, width: 250, height: 90 }
    },
    continuousMetaCognitive: {
      id: 'continuousMetaCognitive',
      title: 'Continuous Parallel Meta-Monitoring',
      domain: 'metacognitive',
      status: 'CORE TRANSFORMATION',
      description: 'Real-time analysis of ongoing cognitive processes',
      implementation: {
        original: 'N/A - Fundamental paradigm shift',
        enhanced: 'Parallel processing stream with bidirectional feedback',
      },
      position: { x: 550, y: 430, width: 250, height: 70 }
    },
    dimensionalVisualization: {
      id: 'dimensionalVisualization',
      title: 'Dimensional Visualization & Navigation',
      domain: 'computational',
      status: 'ENHANCED',
      description: 'Multi-dimensional projection with topological navigation',
      implementation: {
        original: 'N/A - Extension of original capabilities',
        enhanced: 'Manifold projection with dimensional reduction',
      },
      position: { x: 550, y: 520, width: 250, height: 70 }
    }
  };
  
  // Bridge definitions connecting original and enhanced components
  const bridges = [
    {
      id: 'thoughtBridge',
      source: 'thoughtNode',
      target: 'dimensionalThoughtSpace',
      title: 'ThoughtNode ↔ Dimensional Vector Mapping',
      description: 'Bidirectional transformation between hierarchical trees and topological manifolds',
      implementation: 'Tensor projection with structure-preserving operations',
      position: { y: 255 }
    },
    {
      id: 'evaluationBridge',
      source: 'evaluation',
      target: 'probabilisticEvaluation',
      title: 'Hybrid Evaluation Strategy',
      description: 'Integration of deterministic and probabilistic processing approaches',
      implementation: 'Confidence-weighted evaluation with adaptive strategy selection',
      position: { y: 365 }
    },
    {
      id: 'metaCognitiveBridge',
      source: 'metaCognitive',
      target: 'continuousMetaCognitive',
      title: 'Synchronization Framework',
      description: 'Coordination between episodic and continuous monitoring systems',
      implementation: 'Event-driven synchronization with state reconciliation',
      position: { y: 465 }
    },
    {
      id: 'visualizationBridge',
      source: 'visualization',
      target: 'dimensionalVisualization',
      title: 'Adaptive Rendering',
      description: 'Translation between hierarchical and dimensional representations',
      implementation: 'Context-sensitive projection with navigation adaptation',
      position: { y: 555 }
    }
  ];
  
  // Event handlers for interactive elements
  const handleComponentClick = (componentId) => {
    setActiveComponent(componentId === activeComponent ? null : componentId);
    setActiveBridge(null);
  };
  
  const handleBridgeClick = (bridgeId) => {
    setActiveBridge(bridgeId === activeBridge ? null : bridgeId);
    setActiveComponent(null);
  };
  
  const toggleDimensionalMode = () => {
    // Animate the transition between modes
    const duration = 1000; // 1 second transition
    const startTime = Date.now();
    const initialState = dimensionalMode ? 100 : 0;
    const targetState = dimensionalMode ? 0 : 100;
    
    const animateTransition = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Use easeInOut function for smooth transition
      const easedProgress = progress < 0.5
        ? 2 * progress * progress
        : 1 - Math.pow(-2 * progress + 2, 2) / 2;
      
      const newState = initialState + (targetState - initialState) * easedProgress;
      setTransformationState(newState);
      
      if (progress < 1) {
        requestAnimationFrame(animateTransition);
      } else {
        // Complete the mode switch at the end of animation
        setDimensionalMode(!dimensionalMode);
      }
    };
    
    animateTransition();
  };
  
  // Get active component or bridge data
  const getActiveElementData = () => {
    if (activeComponent) {
      return protocolComponents[activeComponent];
    }
    if (activeBridge) {
      return bridges.find(b => b.id === activeBridge);
    }
    return null;
  };
  
  // Dynamic CSS class generation for domain-specific styling
  const getDomainClass = (domain) => {
    switch(domain) {
      case 'computational': return 'computational-domain';
      case 'cognitive': return 'cognitive-domain';
      case 'representational': return 'representational-domain';
      case 'metacognitive': return 'metacognitive-domain';
      default: return '';
    }
  };
  
  // SVG rendering functions
  const renderDimensionalPoints = (component) => {
    if (!component.dimensions) return null;
    
    // Create dimensional vectors emanating from center
    const center = { 
      x: component.position.x + component.position.width / 2, 
      y: component.position.y + component.position.height / 2 
    };
    const radius = Math.min(component.position.width, component.position.height) * 0.3;
    
    return Array.from({ length: component.dimensions }).map((_, i) => {
      const angle = (i * 2 * Math.PI) / component.dimensions;
      const x = center.x + Math.cos(angle) * radius;
      const y = center.y + Math.sin(angle) * radius;
      
      return (
        <g key={`dim-${i}`}>
          <line 
            x1={center.x} 
            y1={center.y} 
            x2={x} 
            y2={y} 
            stroke={COLORS.representational} 
            strokeWidth={1} 
            opacity={0.7} 
          />
          <circle 
            cx={x} 
            cy={y} 
            r={4} 
            fill={COLORS.representational} 
          />
        </g>
      );
    });
  };
  
  // Render hierarchical node structure
  const renderHierarchicalNodes = (component) => {
    if (component.id !== 'thoughtNode') return null;
    
    const center = { 
      x: component.position.x + component.position.width / 2, 
      y: component.position.y + 20 
    };
    
    return (
      <g>
        {/* Root node */}
        <circle cx={center.x} cy={center.y} r={8} fill={COLORS.representational} />
        
        {/* Child nodes level 1 */}
        <circle cx={center.x - 40} cy={center.y + 25} r={6} fill={COLORS.representational} opacity={0.8} />
        <circle cx={center.x} cy={center.y + 25} r={6} fill={COLORS.representational} opacity={0.8} />
        <circle cx={center.x + 40} cy={center.y + 25} r={6} fill={COLORS.representational} opacity={0.8} />
        
        {/* Child nodes level 2 */}
        <circle cx={center.x - 50} cy={center.y + 45} r={4} fill={COLORS.representational} opacity={0.6} />
        <circle cx={center.x - 30} cy={center.y + 45} r={4} fill={COLORS.representational} opacity={0.6} />
        <circle cx={center.x + 30} cy={center.y + 45} r={4} fill={COLORS.representational} opacity={0.6} />
        
        {/* Connections */}
        <line x1={center.x} y1={center.y} x2={center.x - 40} y2={center.y + 25} 
              stroke={COLORS.representational} strokeWidth={1.5} />
        <line x1={center.x} y1={center.y} x2={center.x} y2={center.y + 25} 
              stroke={COLORS.representational} strokeWidth={1.5} />
        <line x1={center.x} y1={center.y} x2={center.x + 40} y2={center.y + 25} 
              stroke={COLORS.representational} strokeWidth={1.5} />
        
        <line x1={center.x - 40} y1={center.y + 25} x2={center.x - 50} y2={center.y + 45} 
              stroke={COLORS.representational} strokeWidth={1} />
        <line x1={center.x - 40} y1={center.y + 25} x2={center.x - 30} y2={center.y + 45} 
              stroke={COLORS.representational} strokeWidth={1} />
        <line x1={center.x} y1={center.y + 25} x2={center.x + 30} y2={center.y + 45} 
              stroke={COLORS.representational} strokeWidth={1} />
      </g>
    );
  };
  
  // Calculate the interpolated state for transition animations
  const getTransitionState = (originalProp, enhancedProp) => {
    // Convert transformation state (0-100) to proportion (0-1)
    const proportion = transformationState / 100;
    
    // If properties are objects, recursively interpolate
    if (typeof originalProp === 'object' && typeof enhancedProp === 'object') {
      const result = {};
      for (const key in originalProp) {
        if (key in enhancedProp) {
          result[key] = getTransitionState(originalProp[key], enhancedProp[key]);
        } else {
          result[key] = originalProp[key];
        }
      }
      return result;
    }
    
    // If properties are numbers, linearly interpolate
    if (typeof originalProp === 'number' && typeof enhancedProp === 'number') {
      return originalProp + (enhancedProp - originalProp) * proportion;
    }
    
    // Default: return appropriate value based on transition state
    return proportion < 0.5 ? originalProp : enhancedProp;
  };

  return (
    <div className="protocol-visualizer" ref={containerRef} style={{
      display: 'flex',
      flexDirection: 'column',
      width: '100%',
      height: '100%',
      padding: '16px',
      backgroundColor: COLORS.background,
      fontFamily: 'Arial, sans-serif'
    }}>
      <div className="control-panel" style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '16px'
      }}>
        <h2 style={{ margin: 0, color: COLORS.text.primary }}>
          Cross-Protocol Integration Architecture
        </h2>
        
        <div className="controls">
          <button
            onClick={toggleDimensionalMode}
            style={{
              backgroundColor: dimensionalMode ? COLORS.representational : COLORS.computational,
              color: COLORS.text.light,
              border: 'none',
              padding: '8px 16px',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold',
              transition: 'background-color 0.3s'
            }}
          >
            {dimensionalMode ? 'Hierarchical View' : 'Dimensional View'}
          </button>
        </div>
      </div>
      
      <div className="visualization-container" style={{
        display: 'flex',
        height: '100%',
        gap: '16px'
      }}>
        <div className="svg-container" style={{
          flex: '1 1 70%',
          border: `1px solid ${COLORS.border}`,
          borderRadius: '8px',
          backgroundColor: '#ffffff',
          overflow: 'hidden'
        }}>
          <svg 
            ref={svgRef}
            width="100%" 
            height="100%" 
            viewBox="0 0 900 600"
            style={{ display: 'block' }}
          >
            {/* Background */}
            <rect width="900" height="600" fill="#ffffff" />
            
            {/* Original Protocol Container */}
            <g className="original-protocol">
              <rect 
                x="50" 
                y="50" 
                width="350" 
                height="530" 
                rx="8" 
                ry="8" 
                fill="#f8f9fa" 
                stroke={COLORS.border} 
                strokeWidth="1" 
              />
              <text 
                x="225" 
                y="80" 
                textAnchor="middle" 
                fill={COLORS.text.primary} 
                fontWeight="bold" 
                fontSize="16"
              >
                Original Protocol Architecture
              </text>
              
              {/* Render original components */}
              {Object.values(protocolComponents)
                .filter(comp => !comp.id.startsWith('dimensional'))
                .map(component => {
                  const domainColor = COLORS[component.domain];
                  const isActive = component.id === activeComponent;
                  
                  return (
                    <g key={component.id} onClick={() => handleComponentClick(component.id)}>
                      <rect 
                        x={component.position.x} 
                        y={component.position.y} 
                        width={component.position.width} 
                        height={component.position.height} 
                        rx="5" 
                        ry="5" 
                        fill={`${domainColor}15`}
                        stroke={domainColor} 
                        strokeWidth={isActive ? "3" : "2"} 
                        style={{ cursor: 'pointer' }}
                      />
                      <text 
                        x={component.position.x + component.position.width/2} 
                        y={component.position.y + 20} 
                        textAnchor="middle" 
                        fill={COLORS.text.primary} 
                        fontWeight={isActive ? "bold" : "normal"} 
                        fontSize="14"
                      >
                        {component.title}
                      </text>
                      <text 
                        x={component.position.x + component.position.width/2} 
                        y={component.position.y + component.position.height - 10} 
                        textAnchor="middle" 
                        fill={COLORS.text.secondary} 
                        fontStyle="italic" 
                        fontSize="12"
                      >
                        {component.status}
                      </text>
                      
                      {/* Render hierarchical structure for ThoughtNode */}
                      {renderHierarchicalNodes(component)}
                    </g>
                  );
              })}
            </g>
            
            {/* Enhanced Protocol Container */}
            <g className="enhanced-protocol">
              <rect 
                x="500" 
                y="50" 
                width="350" 
                height="530" 
                rx="8" 
                ry="8" 
                fill="#f8f9fa" 
                stroke={COLORS.border} 
                strokeWidth="1" 
              />
              <text 
                x="675" 
                y="80" 
                textAnchor="middle" 
                fill={COLORS.text.primary} 
                fontWeight="bold" 
                fontSize="16"
              >
                Enhanced Protocol Architecture
              </text>
              
              {/* Render enhanced components */}
              {Object.values(protocolComponents)
                .filter(comp => comp.id.startsWith('dimensional'))
                .map(component => {
                  const domainColor = COLORS[component.domain];
                  const isActive = component.id === activeComponent;
                  
                  return (
                    <g key={component.id} onClick={() => handleComponentClick(component.id)}>
                      <rect 
                        x={component.position.x} 
                        y={component.position.y} 
                        width={component.position.width} 
                        height={component.position.height} 
                        rx="5" 
                        ry="5" 
                        fill={`${domainColor}15`}
                        stroke={domainColor} 
                        strokeWidth={isActive ? "3" : "2"} 
                        style={{ cursor: 'pointer' }}
                      />
                      <text 
                        x={component.position.x + component.position.width/2} 
                        y={component.position.y + 20} 
                        textAnchor="middle" 
                        fill={COLORS.text.primary} 
                        fontWeight={isActive ? "bold" : "normal"} 
                        fontSize="14"
                      >
                        {component.title}
                      </text>
                      <text 
                        x={component.position.x + component.position.width/2} 
                        y={component.position.y + component.position.height - 10} 
                        textAnchor="middle" 
                        fill={COLORS.text.secondary} 
                        fontStyle="italic" 
                        fontSize="12"
                      >
                        {component.status}
                      </text>
                      
                      {/* Render dimensional vectors for DimensionalThoughtSpace */}
                      {renderDimensionalPoints(component)}
                    </g>
                  );
              })}
            </g>
            
            {/* Render bridge connections */}
            {bridges.map(bridge => {
              const source = protocolComponents[bridge.source];
              const target = protocolComponents[bridge.target];
              const isActive = bridge.id === activeBridge;
              
              // Calculate connection points
              const sourceX = source.position.x + source.position.width;
              const targetX = target.position.x;
              const y = bridge.position.y;
              
              return (
                <g key={bridge.id} onClick={() => handleBridgeClick(bridge.id)}>
                  <path 
                    d={`M ${sourceX} ${y} H ${targetX}`}
                    stroke={COLORS.bridge} 
                    strokeWidth={isActive ? "4" : "2"} 
                    strokeDasharray="5,5"
                    fill="none"
                    style={{ cursor: 'pointer' }}
                  />
                  <circle 
                    cx={(sourceX + targetX) / 2} 
                    cy={y} 
                    r={isActive ? "20" : "15"} 
                    fill="#ffffff" 
                    stroke={COLORS.bridge} 
                    strokeWidth="2"
                    style={{ cursor: 'pointer' }}
                  />
                  <text 
                    x={(sourceX + targetX) / 2} 
                    y={y + 5} 
                    textAnchor="middle" 
                    fill={COLORS.bridge} 
                    fontWeight="bold" 
                    fontSize={isActive ? "14" : "12"}
                    style={{ cursor: 'pointer' }}
                  >
                    {bridges.indexOf(bridge) + 1}
                  </text>
                </g>
              );
            })}
            
            {/* Bridge Legend */}
            <rect 
              x="250" 
              y="590" 
              width="400" 
              height="30" 
              rx="5" 
              ry="5" 
              fill="#ffffff" 
              stroke={COLORS.border} 
              strokeWidth="1"
            />
            {bridges.map((bridge, index) => (
              <g key={`legend-${bridge.id}`}>
                <text 
                  x={280 + index * 100} 
                  y={610} 
                  textAnchor="middle" 
                  fill={COLORS.bridge} 
                  fontWeight="bold" 
                  fontSize="14"
                >
                  {index + 1}
                </text>
                <text 
                  x={320 + index * 100} 
                  y={610} 
                  textAnchor="start" 
                  fill={COLORS.text.primary} 
                  fontSize="12"
                >
                  {bridge.title.split(' ')[0]}
                </text>
              </g>
            ))}
          </svg>
        </div>
        
        <div className="detail-panel" style={{
          flex: '1 1 30%',
          border: `1px solid ${COLORS.border}`,
          borderRadius: '8px',
          backgroundColor: '#ffffff',
          padding: '16px',
          overflowY: 'auto'
        }}>
          {getActiveElementData() ? (
            <div>
              <h3 style={{ 
                margin: '0 0 12px 0', 
                color: activeComponent 
                  ? COLORS[protocolComponents[activeComponent]?.domain] 
                  : COLORS.bridge
              }}>
                {getActiveElementData().title}
              </h3>
              
              {activeComponent && (
                <div className="component-details">
                  <div className="detail-section">
                    <h4 style={{ color: COLORS.text.secondary }}>Domain</h4>
                    <p>{getActiveElementData().domain.charAt(0).toUpperCase() + getActiveElementData().domain.slice(1)}</p>
                  </div>
                  
                  <div className="detail-section">
                    <h4 style={{ color: COLORS.text.secondary }}>Description</h4>
                    <p>{getActiveElementData().description}</p>
                  </div>
                  
                  <div className="implementation-comparison" style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '12px',
                    marginTop: '16px'
                  }}>
                    <h4 style={{ color: COLORS.text.secondary, margin: '0 0 4px 0' }}>Implementation</h4>
                    
                    <div className="implementation-item" style={{
                      backgroundColor: `${COLORS.computational}10`,
                      padding: '12px',
                      borderRadius: '4px',
                      borderLeft: `4px solid ${COLORS.computational}`
                    }}>
                      <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>Original Protocol</div>
                      <div>{getActiveElementData().implementation.original}</div>
                    </div>
                    
                    <div className="implementation-item" style={{
                      backgroundColor: `${COLORS.representational}10`,
                      padding: '12px',
                      borderRadius: '4px',
                      borderLeft: `4px solid ${COLORS.representational}`
                    }}>
                      <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>Enhanced Protocol</div>
                      <div>{getActiveElementData().implementation.enhanced}</div>
                    </div>
                  </div>
                </div>
              )}
              
              {activeBridge && (
                <div className="bridge-details">
                  <div className="detail-section">
                    <h4 style={{ color: COLORS.text.secondary }}>Description</h4>
                    <p>{getActiveElementData().description}</p>
                  </div>
                  
                  <div className="detail-section">
                    <h4 style={{ color: COLORS.text.secondary }}>Implementation Approach</h4>
                    <p>{getActiveElementData().implementation}</p>
                  </div>
                  
                  <div className="detail-section">
                    <h4 style={{ color: COLORS.text.secondary }}>Connected Components</h4>
                    <div style={{ display: 'flex', justifyContent: 'space-between', gap: '12px' }}>
                      <div style={{
                        backgroundColor: `${COLORS.computational}10`,
                        padding: '8px',
                        borderRadius: '4px',
                        flex: 1
                      }}>
                        <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>Original</div>
                        <div>{protocolComponents[getActiveElementData().source].title}</div>
                      </div>
                      
                      <div style={{
                        backgroundColor: `${COLORS.representational}10`,
                        padding: '8px',
                        borderRadius: '4px',
                        flex: 1
                      }}>
                        <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>Enhanced</div>
                        <div>{protocolComponents[getActiveElementData().target].title}</div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="empty-state" style={{ textAlign: 'center', color: COLORS.text.secondary }}>
              <h3>Interactive Visualization</h3>
              <p>Click on a component or bridge to see detailed information.</p>
              <p>Toggle between hierarchical and dimensional views using the button above.</p>
              <p>The visualization demonstrates both protocols and their integration points.</p>
              
              <div style={{ 
                marginTop: '20px', 
                padding: '16px', 
                backgroundColor: '#f8f9fa', 
                borderRadius: '8px', 
                textAlign: 'left' 
              }}>
                <h4 style={{ color: COLORS.text.primary, margin: '0 0 8px 0' }}>Core Transformations</h4>
                <ul style={{ margin: 0, paddingLeft: '20px' }}>
                  <li style={{ marginBottom: '8px' }}>
                    <span style={{ color: COLORS.representational, fontWeight: 'bold' }}>
                      Thought Representation:
                    </span> Hierarchical tree → Dimensional manifold
                  </li>
                  <li style={{ marginBottom: '8px' }}>
                    <span style={{ color: COLORS.cognitive, fontWeight: 'bold' }}>
                      Evaluation Strategy:
                    </span> Deterministic → Probabilistic
                  </li>
                  <li style={{ marginBottom: '8px' }}>
                    <span style={{ color: COLORS.metacognitive, fontWeight: 'bold' }}>
                      Meta-Cognitive Processing:
                    </span> Post-process → Continuous
                  </li>
                  <li>
                    <span style={{ color: COLORS.computational, fontWeight: 'bold' }}>
                      Visualization Approach:
                    </span> Hierarchical → Topological
                  </li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProtocolVisualizer;