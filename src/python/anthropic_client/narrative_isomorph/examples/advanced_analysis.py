# Example advanced analysis script utilizing the new modules
from anthropic_client.narrative_isomorph.corpus import NarrativeCorpus  # Assume this remains unchanged
from anthropic_client.narrative_isomorph.pipeline import NarrativeAnalysisPipeline

# Create a dummy corpus for testing purposes.
corpus = NarrativeCorpus(
    source_narratives={"n1": "Once upon a time, a hero embarked on an epic journey."},
    architecture_outputs={("n1", "archA"): "In a land far away, a legend was born."}
)
corpus.preprocess_corpus()

# Initialize the analysis pipeline.
analysis_pipeline = NarrativeAnalysisPipeline(corpus)
analysis_results = analysis_pipeline.run_full_analysis(frameworks={"framework1": "example"})

print("Advanced Analysis Report:")
print("Structural Isomorphism Measure:", analysis_results["isomorphism_measure"])
print("Temporal Measures:", analysis_results["temporal_measures"])
print("p-value:", analysis_results["p_value"], "Effect Size:", analysis_results["effect_size"])
print("Ethical Assessment:", analysis_results["ethical_assessment"])