import unittest
from anthropic_client.narrative_isomorph.corpus import NarrativeCorpus
from anthropic_client.narrative_isomorph.representation import NarrativeRepresentation
from anthropic_client.narrative_isomorph.calculus import NarrativeIsomorphismCalculus
from anthropic_client.narrative_isomorph.temporal import MultiScaleTemporalAnalysis
from anthropic_client.narrative_isomorph.validation import IsomorphismStatisticalValidation
from anthropic_client.narrative_isomorph.ethics import NarrativeEthicsFramework
from anthropic_client.narrative_isomorph.pipeline import NarrativeAnalysisPipeline

class TestNarrativeIsomorphBasics(unittest.TestCase):
    def setUp(self):
        self.sample_narrative = "Once upon a time, a hero embarked on an epic journey."
        self.sample_output = "In a land far away, a legend was born."
        
        self.corpus = NarrativeCorpus(
            source_narratives={"n1": self.sample_narrative},
            architecture_outputs={("n1", "archA"): self.sample_output}
        )
        
    def test_corpus(self):
        """Test basic corpus functionality"""
        self.corpus.preprocess_corpus()
        self.assertTrue(self.corpus.preprocessed)
        self.assertEqual(self.corpus.get_narratives()["n1"], self.sample_narrative)
        
    def test_representation(self):
        """Test narrative representation"""
        repr_model = NarrativeRepresentation()
        result = repr_model.encode_narrative_structure(self.sample_narrative)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 4)
        
    def test_calculus(self):
        """Test isomorphism calculus"""
        calc = NarrativeIsomorphismCalculus()
        source_structure = {}
        target_structure = {}
        result = calc.compute_structural_homomorphism(source_structure, target_structure)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        
    def test_pipeline(self):
        """Test analysis pipeline"""
        pipeline = NarrativeAnalysisPipeline(self.corpus)
        results = pipeline.run_full_analysis(frameworks={"framework1": "example"})
        self.assertIsInstance(results, dict)
        self.assertIn("isomorphism_measure", results)
        self.assertIn("temporal_measures", results)
        self.assertIn("p_value", results)
        self.assertIn("effect_size", results)

if __name__ == "__main__":
    unittest.main()