"""
RuralGuard AI - Demo API (No AWS Required)
Runs locally without AWS credentials for demonstration
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from datetime import datetime
import base64
from uuid import uuid4

app = FastAPI(
    title="RuralGuard AI Demo API",
    description="Edge-First AI-Powered Identity Verification Platform (Demo Mode)",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class VerificationRequest(BaseModel):
    user_id: Optional[str] = None
    device_id: str
    face_image_base64: str
    id_document_base64: str
    location: Optional[dict] = None

class VerificationResponse(BaseModel):
    verification_id: str
    status: str
    confidence_score: float
    verification_method: str
    timestamp: datetime
    message: str
    fallback_required: bool = False
    fallback_options: Optional[List[str]] = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "RuralGuard AI Demo API",
        "version": "1.0.0",
        "status": "operational",
        "mode": "demo",
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0",
        "mode": "demo",
        "services": {
            "api": "operational",
            "ai_models": "simulated",
            "database": "in-memory",
            "aws_services": "simulated"
        }
    }

@app.post("/api/v1/verify", response_model=VerificationResponse)
async def verify_identity(request: VerificationRequest):
    """
    Demo identity verification endpoint
    Simulates AI verification with varied results
    """
    try:
        import random
        import time
        
        session_id = str(uuid4())
        
        # Simulate processing delay
        time.sleep(random.uniform(1.5, 2.5))
        
        # Simulate varied verification results (70% success, 30% failure)
        success_rate = random.random()
        
        if success_rate > 0.3:  # 70% success
            confidence = random.uniform(0.85, 0.98)
            status = "SUCCESS"
            
            messages = [
                "✅ Identity verified successfully! Face matches ID document with high confidence.",
                "✅ Verification complete! Biometric match confirmed with excellent quality.",
                "✅ Authentication successful! All security checks passed.",
                "✅ Identity confirmed! Face recognition and document validation successful."
            ]
            message = random.choice(messages)
            fallback_required = False
            
        else:  # 30% failure
            confidence = random.uniform(0.45, 0.75)
            status = "FAILED"
            
            failure_reasons = [
                "❌ Face quality too low. Please ensure good lighting and clear view of face.",
                "❌ Face does not match ID document photo. Please try again.",
                "❌ Liveness check failed. Please ensure you are present in person.",
                "❌ ID document unclear. Please upload a clearer image of your ID."
            ]
            message = random.choice(failure_reasons)
            fallback_required = True
        
        return VerificationResponse(
            verification_id=session_id,
            status=status,
            confidence_score=round(confidence, 3),
            verification_method="MULTI_MODAL",
            timestamp=datetime.utcnow(),
            message=message,
            fallback_required=fallback_required,
            fallback_options=["PIN", "OTP"] if fallback_required else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")

@app.post("/api/v1/verify/upload", response_model=VerificationResponse)
async def verify_identity_upload(
    face_image: UploadFile = File(...),
    id_document: UploadFile = File(...),
    device_id: str = "demo-device"
):
    """Demo verification with file upload and quality checks"""
    try:
        import random
        import time
        
        session_id = str(uuid4())
        
        # Read and check files
        face_data = await face_image.read()
        id_data = await id_document.read()
        
        # Simulate processing
        time.sleep(random.uniform(1.5, 2.5))
        
        # Check file sizes (basic quality check)
        if len(face_data) < 1000 or len(id_data) < 1000:
            return VerificationResponse(
                verification_id=session_id,
                status="FAILED",
                confidence_score=0.0,
                verification_method="QUALITY_CHECK",
                timestamp=datetime.utcnow(),
                message="❌ Image quality too low. Please upload clearer images.",
                fallback_required=True,
                fallback_options=["PIN", "OTP"]
            )
        
        # Simulate varied results
        success_rate = random.random()
        
        if success_rate > 0.3:
            confidence = random.uniform(0.85, 0.98)
            return VerificationResponse(
                verification_id=session_id,
                status="SUCCESS",
                confidence_score=round(confidence, 3),
                verification_method="MULTI_MODAL",
                timestamp=datetime.utcnow(),
                message=f"✅ Identity verified! Face recognition: {int(confidence*100)}%, ID validation: {int((confidence+0.02)*100)}%, Liveness: Confirmed",
                fallback_required=False
            )
        else:
            confidence = random.uniform(0.45, 0.75)
            return VerificationResponse(
                verification_id=session_id,
                status="FAILED",
                confidence_score=round(confidence, 3),
                verification_method="MULTI_MODAL",
                timestamp=datetime.utcnow(),
                message="❌ Verification failed. Face does not match ID document with sufficient confidence.",
                fallback_required=True,
                fallback_options=["PIN", "OTP"]
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")

@app.post("/api/v1/verify/pin")
async def verify_pin(data: dict):
    """Demo PIN verification"""
    return VerificationResponse(
        verification_id=str(uuid4()),
        status="SUCCESS",
        confidence_score=1.0,
        verification_method="PIN",
        timestamp=datetime.utcnow(),
        message="✅ PIN verified successfully!",
        fallback_required=False
    )

@app.post("/api/v1/verify/otp/request")
async def request_otp(data: dict):
    """Demo OTP request"""
    return {
        "status": "success",
        "message": "OTP sent successfully (Demo: 123456)",
        "session_id": str(uuid4()),
        "expires_in": 300
    }

@app.post("/api/v1/verify/otp/validate")
async def verify_otp(data: dict):
    """Demo OTP verification"""
    return VerificationResponse(
        verification_id=str(uuid4()),
        status="SUCCESS",
        confidence_score=1.0,
        verification_method="OTP",
        timestamp=datetime.utcnow(),
        message="✅ OTP verified successfully!",
        fallback_required=False
    )

@app.get("/api/v1/analytics/summary")
async def get_analytics():
    """Demo analytics"""
    return {
        "total_verifications": 1250,
        "success_rate": 0.94,
        "average_confidence": 0.91,
        "fallback_rate": 0.06,
        "fraud_detected": 12,
        "mode": "demo"
    }

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🌾 RuralGuard AI - Demo API Server")
    print("="*60)
    print("\n✅ Starting server in DEMO mode (no AWS required)")
    print("📍 API: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("🔍 Health: http://localhost:8000/health")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(
        "demo_api:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
