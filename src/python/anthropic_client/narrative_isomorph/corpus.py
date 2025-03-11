# This module handles the corpus management for narrative analysis
class NarrativeCorpus:
    def __init__(self, source_narratives=None, architecture_outputs=None):
        """
        Initialize a narrative corpus with source texts and architecture outputs.
        
        Args:
            source_narratives: Dict mapping narrative IDs to source text.
            architecture_outputs: Dict mapping (narrative_id, architecture_id) tuples to outputs.
        """
        self.source_narratives = source_narratives or {}
        self.architecture_outputs = architecture_outputs or {}
        self.preprocessed = False
        
    def preprocess_corpus(self):
        """
        Preprocess the corpus for analysis.
        """
        # PLACEHOLDER: Add actual preprocessing logic here
        self.preprocessed = True
        return self
        
    def add_narrative(self, narrative_id, text):
        """
        Add a narrative to the corpus.
        """
        self.source_narratives[narrative_id] = text
        self.preprocessed = False
        
    def add_architecture_output(self, narrative_id, architecture_id, output):
        """
        Add an architecture's output for a specific narrative.
        """
        self.architecture_outputs[(narrative_id, architecture_id)] = output
        self.preprocessed = False
        
    def get_narratives(self):
        """
        Get all narratives in the corpus.
        """
        return self.source_narratives
        
    def get_architecture_outputs(self, narrative_id=None, architecture_id=None):
        """
        Get architecture outputs, optionally filtered by narrative or architecture.
        """
        if narrative_id and architecture_id:
            return {k: v for k, v in self.architecture_outputs.items() 
                    if k[0] == narrative_id and k[1] == architecture_id}
        elif narrative_id:
            return {k: v for k, v in self.architecture_outputs.items() 
                    if k[0] == narrative_id}
        elif architecture_id:
            return {k: v for k, v in self.architecture_outputs.items() 
                    if k[1] == architecture_id}
        else:
            return self.architecture_outputs