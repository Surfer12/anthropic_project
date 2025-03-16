"""
Module to load JSON model configurations.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

def load_model_config(model_name: str) -> Optional[Dict[str, Any]]:
    """Load model configuration from a JSON file.
    
    Args:
        model_name: The name of the model to load configuration for.
        
    Returns:
        A dictionary containing the model configuration or None if the file was not found.
    """
    config_locations = [
        Path(__file__).parent / f"{model_name}.json",
        Path(__file__).parent / "configs" / f"{model_name}.json",
        Path.home() / ".anthropic" / "configs" / f"{model_name}.json"
    ]
    
    for location in config_locations:
        if location.exists():
            with open(location, 'r') as f:
                return json.load(f)
                
    return None 