import React, { useMemo } from 'react';
import d3 from 'd3';
import { interpolateStates } from '../utils/interpolateStates';
import { RecursiveThoughtVisualizer } from '../visualization/RecursiveThoughtVisualizer';

const TemporalProcessVisualization: React.FC<{
  evaluationSteps: EvaluationStep[];
}> = ({ evaluationSteps }) => {
  // ... existing code ...
  
  const interpolatedState = useMemo(() => {
    if (!playbackActive) return evaluationSteps[currentStep];
    
    const progress = d3.easeCubic(playbackProgress);
    return interpolateStates(
      evaluationSteps[currentStep],
      evaluationSteps[currentStep + 1],
      progress
    );
  }, [currentStep, playbackActive, playbackProgress]);

  return (
    // ... existing code ...
    <RecursiveThoughtVisualizer 
      model={interpolatedState.modelState}
      highlightedNodeId={interpolatedState.activeNodeId}
      memoizationState={interpolatedState.memoizationCache}
      transitionProgress={playbackActive ? playbackProgress : 1}
    />
  );
};

export default TemporalProcessVisualization; 