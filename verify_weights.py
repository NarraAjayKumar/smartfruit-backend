import os
import sys
from pathlib import Path
from ultralytics import YOLO

def verify_models():
    base_dir = Path(__file__).parent.resolve()
    weights_dir = base_dir / "Weights"
    
    models_to_check = {
        "watermelon": "watermelon.pt",
        "tomato": "Tomatobest.pt",
        "cucumber": "Cucumberbest.pt"
    }
    
    print(f"--- SmartFruit AI Model Verification ---")
    print(f"Base Directory: {base_dir}")
    print(f"Weights Directory: {weights_dir}")
    print(f"----------------------------------------")
    
    all_success = True
    for crop, filename in models_to_check.items():
        weight_path = weights_dir / filename
        print(f"Checking {crop.upper()}...")
        
        if not weight_path.exists():
            print(f"  [ERROR] File NOT FOUND: {weight_path}")
            all_success = False
            continue
            
        try:
            print(f"  [INFO] Attempting to load {filename}...")
            model = YOLO(str(weight_path))
            print(f"  [SUCCESS] {crop.upper()} model loaded successfully.")
        except Exception as e:
            print(f"  [ERROR] Failed to load {crop.upper()}: {str(e)}")
            all_success = False
            
    print(f"----------------------------------------")
    if all_success:
        print("FINAL STATUS: ALL MODELS VERIFIED SUCCESSFULLY")
    else:
        print("FINAL STATUS: VERIFICATION FAILED - CHECK ERRORS ABOVE")

if __name__ == "__main__":
    verify_models()
