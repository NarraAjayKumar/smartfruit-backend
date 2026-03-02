import os
from pathlib import Path
from ultralytics import YOLO

class ModelLoader:
    def __init__(self):
        self.models = {}
        # Get the directory where model_loader.py is located
        self.base_dir = Path(__file__).parent.resolve()
        self.weights_dir = self.base_dir / "Weights"
        
        self.paths = {
            "watermelon": self.weights_dir / "watermelon.pt",
            "tomato": self.weights_dir / "Tomatobest.pt",
            "cucumber": self.weights_dir / "Cucumberbest.pt"
        }

    def get_model(self, crop_name: str):
        crop_name = crop_name.lower()
        if crop_name not in self.paths:
            raise ValueError(f"Model for crop '{crop_name}' not found.")
        
        # Lazy load and cache
        if crop_name not in self.models:
            model_path = self.paths[crop_name]
            if not model_path.exists():
                raise FileNotFoundError(f"Model file not found: {model_path}")
                
            print(f"Loading {crop_name} model from {model_path}...")
            self.models[crop_name] = YOLO(str(model_path))
            
        return self.models[crop_name]

model_manager = ModelLoader()
