from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import time
from datetime import datetime, timedelta
from model_loader import model_manager
from otp_service import otp_service

app = FastAPI(title="SmartFruit AI Backend")

# Enable CORS for Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for OTPs and Profiles
otp_store = {}
global_profile = {
    "name": "Farmer Raghav",
    "avatar": "person",
    "notificationsEnabled": True,
    "locationMode": "auto",
    "manualLocation": "Mylavaram, AP"
}

@app.get("/")
@app.get("/ping")
async def ping():
    return {"message": "SmartFruit AI Backend is running", "status": "online"}

@app.get("/profile")
async def get_profile():
    return global_profile

@app.post("/profile")
async def update_profile(
    name: str = Form(None),
    avatar: str = Form(None),
    notificationsEnabled: bool = Form(None),
    locationMode: str = Form(None),
    manualLocation: str = Form(None)
):
    if name is not None: global_profile["name"] = name
    if avatar is not None: global_profile["avatar"] = avatar
    if notificationsEnabled is not None: global_profile["notificationsEnabled"] = notificationsEnabled
    if locationMode is not None: global_profile["locationMode"] = locationMode
    if manualLocation is not None: global_profile["manualLocation"] = manualLocation
    return global_profile

@app.post("/send-otp")
async def send_otp(contact: str = Form(...), type: str = Form(...)):
    otp = otp_service.generate_otp()
    expiry = datetime.now() + timedelta(minutes=5)
    
    otp_store[contact] = {
        "otp": otp,
        "expiry": expiry.timestamp()
    }
    
    success = False
    if type == "email":
        success = otp_service.send_email_otp(contact, otp)
    elif type == "phone":
        success = otp_service.send_sms_otp(contact, otp)
    
    if success:
        return {
            "message": "OTP sent successfully",
            "otp": otp # Returning OTP for demo auto-fill
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to send OTP")

@app.post("/verify-otp")
async def verify_otp(contact: str = Form(...), otp: str = Form(...)):
    if contact not in otp_store:
        raise HTTPException(status_code=400, detail="OTP not requested for this contact")
    
    stored_data = otp_store[contact]
    
    if datetime.now().timestamp() > stored_data["expiry"]:
        del otp_store[contact]
        raise HTTPException(status_code=400, detail="OTP has expired")
    
    if stored_data["otp"] == otp:
        # OTP is valid, remove from store
        del otp_store[contact]
        return {"message": "OTP verified successfully", "token": "mock_session_token_123"}
    else:
        raise HTTPException(status_code=400, detail="Invalid OTP")

@app.post("/predict")
async def predict(
    image: UploadFile = File(...),
    crop_name: str = Form(...),
    lat: float = Form(None),
    long: float = Form(None)
):
    if lat and long:
        print(f"Prediction requested for {crop_name} at Location: {lat}, {long}")
    else:
        print(f"Prediction requested for {crop_name} (Location not provided)")
    try:
        # Load the selected model via manager (relative paths handled)
        model = model_manager.get_model(crop_name)
        
        # Read image
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        
        # Run inference
        results = model(img)
        
        # Process results
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Get coordinates
                b = box.xyxy[0].tolist() # [x1, y1, x2, y2]
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                name = model.names[cls]
                
                detections.append({
                    "bbox": b,
                    "confidence": conf,
                    "class": name
                })
        
        # Aggregate confidence for a high-level score
        avg_confidence = sum(d["confidence"] for d in detections) / len(detections) if detections else 0.0
        
        return {
            "crop": crop_name,
            "detections": detections,
            "count": len(detections),
            "confidence": avg_confidence,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
