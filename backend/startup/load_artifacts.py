import joblib
import json
import os

from typing import Any, Dict

class ArtifactStore:
    preprocessor: Any = None
    encoder: Any = None
    model: Any = None
    explainer: Any = None
    metadata: Dict[str, Any] = {}
    metrics: Dict[str, Any] = {}

def load_all_artifacts():
    try:
        base_dir = os.path.join(os.getcwd(), 'models', 'artifacts')
        ArtifactStore.preprocessor = joblib.load(os.path.join(base_dir, 'preprocessor.pkl'))
        ArtifactStore.encoder = joblib.load(os.path.join(base_dir, 'encoder.pkl'))
        ArtifactStore.model = joblib.load(os.path.join(base_dir, 'model.pkl'))
        ArtifactStore.explainer = joblib.load(os.path.join(base_dir, 'explainer.pkl'))
        
        with open(os.path.join(base_dir, 'metadata.json'), 'r') as f:
            ArtifactStore.metadata = json.load(f)
            
        with open(os.path.join(base_dir, 'metrics.json'), 'r') as f:
            ArtifactStore.metrics = json.load(f)
            
        print("Successfully loaded all ML artifacts.")
    except Exception as e:
        print(f"Failed to load ML artifacts: {e}")
        import sys
        sys.exit(1)
