import requests
import os
from pathlib import Path

def test_inference():
    url = "http://172.23.132.237:8000/predict"
    # Find any image to test
    weights_dir = Path("backend/Weights")
    
    # We'll just create a tiny blank dummy image for testing the pipeline flow
    from PIL import Image
    dummy_img_path = "test_dummy.jpg"
    Image.new('RGB', (640, 640), color='white').save(dummy_img_path)
    
    crops = ["watermelon", "tomato", "cucumber"]
    
    print(f"--- SmartFruit AI Inference Validation ---")
    for crop in crops:
        print(f"Testing {crop.upper()} inference...")
        with open(dummy_img_path, 'rb') as f:
            files = {'image': (dummy_img_path, f, 'image/jpeg')}
            data = {'crop_name': crop, 'lat': 16.5, 'long': 80.6}
            try:
                r = requests.post(url, files=files, data=data)
                if r.status_code == 200:
                    res = r.json()
                    print(f"  [SUCCESS] Count: {res.get('count')}, Confidence: {res.get('confidence')}")
                else:
                    print(f"  [ERROR] Status {r.status_code}: {r.text}")
            except Exception as e:
                print(f"  [ERROR] Request failed: {str(e)}")
    
    if os.path.exists(dummy_img_path):
        os.remove(dummy_img_path)

if __name__ == "__main__":
    test_inference()
