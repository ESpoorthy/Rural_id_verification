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

# In-memory analytics storage
verification_stats = {
    "total": 0,
    "approved": 0,
    "flagged": 0,
    "total_confidence": 0.0
}

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
    # Enhanced fields for hackathon demo
    fraud_risk_score: float = 0.0
    risk_level: str = "Low"
    ai_explanation: str = ""
    verification_timeline: List[str] = []
    ocr_success: bool = True
    liveness_confidence: float = 0.0
    similarity_score: float = 0.0

# Helper functions for AI reasoning and fraud detection
def calculate_fraud_risk(similarity_score: float, liveness_confidence: float, ocr_success: bool) -> float:
    """
    Calculate fraud risk score based on verification metrics
    Lower score = lower risk
    """
    risk = 0.0
    
    # Similarity score contribution (0-0.4 risk)
    if similarity_score < 0.7:
        risk += 0.4
    elif similarity_score < 0.85:
        risk += 0.2
    
    # Liveness confidence contribution (0-0.3 risk)
    if liveness_confidence < 0.7:
        risk += 0.3
    elif liveness_confidence < 0.85:
        risk += 0.15
    
    # OCR success contribution (0-0.3 risk)
    if not ocr_success:
        risk += 0.3
    
    return min(risk, 1.0)

def get_risk_level(fraud_risk: float) -> str:
    """Determine risk level from fraud risk score"""
    if fraud_risk < 0.3:
        return "Low"
    elif fraud_risk < 0.6:
        return "Medium"
    else:
        return "High"

def generate_ai_explanation(status: str, similarity_score: float, liveness_confidence: float, 
                           ocr_success: bool, fraud_risk: float) -> str:
    """
    Generate natural language explanation for verification result
    
    NOTE: In production, this would use Amazon Bedrock's generative AI capabilities
    to create more sophisticated, context-aware explanations. The Bedrock API would
    analyze all verification metrics and generate human-readable explanations.
    """
    if status == "SUCCESS":
        explanation = f"The verification was successful because the facial similarity score ({similarity_score:.2%}) exceeded the required threshold "
        explanation += f"and liveness detection confirmed authenticity ({liveness_confidence:.2%}). "
        
        if ocr_success:
            explanation += "Identity document fields were successfully extracted and validated. "
        
        if fraud_risk < 0.2:
            explanation += "No anomalies or suspicious patterns were detected during the verification process."
        else:
            explanation += "Minor inconsistencies were noted but within acceptable parameters."
    else:
        explanation = f"The verification failed because "
        reasons = []
        
        if similarity_score < 0.7:
            reasons.append(f"the facial similarity score ({similarity_score:.2%}) was below the required threshold")
        
        if liveness_confidence < 0.7:
            reasons.append(f"liveness detection confidence ({liveness_confidence:.2%}) was insufficient")
        
        if not ocr_success:
            reasons.append("identity document fields could not be reliably extracted")
        
        explanation += ", ".join(reasons) + ". "
        
        if fraud_risk > 0.6:
            explanation += "Multiple risk indicators suggest potential fraud or data quality issues."
        else:
            explanation += "Please ensure good lighting and clear images for better results."
    
    return explanation

def increment_verification_stats(status: str, confidence: float):
    """Track verification statistics for admin panel"""
    verification_stats["total"] += 1
    verification_stats["total_confidence"] += confidence
    
    if status == "SUCCESS":
        verification_stats["approved"] += 1
    else:
        verification_stats["flagged"] += 1

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
    Demo identity verification endpoint with AI reasoning and fraud detection
    Simulates AI verification with varied results
    """
    try:
        import random
        import time
        
        session_id = str(uuid4())
        
        # Build verification timeline
        timeline = [
            "Face image received and validated",
            "ID document received and validated",
            "OCR extraction initiated",
        ]
        
        # Simulate processing delay
        time.sleep(random.uniform(1.5, 2.5))
        
        # Simulate varied verification results (50% success, 50% failure)
        success_rate = random.random()
        
        # Generate realistic metrics
        similarity_score = random.uniform(0.85, 0.98) if success_rate > 0.5 else random.uniform(0.45, 0.75)
        liveness_confidence = random.uniform(0.88, 0.99) if success_rate > 0.5 else random.uniform(0.50, 0.80)
        ocr_success = random.random() > 0.1  # 90% OCR success rate
        
        timeline.append("OCR extraction completed" if ocr_success else "OCR extraction failed")
        timeline.append("Face similarity analysis completed")
        timeline.append("Liveness detection completed")
        
        # Calculate fraud risk
        fraud_risk = calculate_fraud_risk(similarity_score, liveness_confidence, ocr_success)
        risk_level = get_risk_level(fraud_risk)
        
        timeline.append("Fraud risk analysis completed")
        
        if success_rate > 0.5:  # 50% success
            status = "SUCCESS"
            confidence = similarity_score
            
            messages = [
                "✅ Identity verified successfully! Face matches ID document with high confidence.",
                "✅ Verification complete! Biometric match confirmed with excellent quality.",
                "✅ Authentication successful! All security checks passed.",
                "✅ Identity confirmed! Face recognition and document validation successful."
            ]
            message = random.choice(messages)
            fallback_required = False
            
        else:  # 50% failure
            status = "FAILED"
            confidence = similarity_score
            
            failure_reasons = [
                "❌ Face quality too low. Please ensure good lighting and clear view of face.",
                "❌ Face does not match ID document photo. Please try again.",
                "❌ Liveness check failed. Please ensure you are present in person.",
                "❌ ID document unclear. Please upload a clearer image of your ID."
            ]
            message = random.choice(failure_reasons)
            fallback_required = True
        
        # Generate AI explanation
        ai_explanation = generate_ai_explanation(status, similarity_score, liveness_confidence, ocr_success, fraud_risk)
        
        timeline.append("Verification result generated")
        
        # Update statistics
        increment_verification_stats(status, confidence)
        
        return VerificationResponse(
            verification_id=session_id,
            status=status,
            confidence_score=round(confidence, 3),
            verification_method="MULTI_MODAL",
            timestamp=datetime.utcnow(),
            message=message,
            fallback_required=fallback_required,
            fallback_options=["PIN", "OTP"] if fallback_required else None,
            fraud_risk_score=round(fraud_risk, 3),
            risk_level=risk_level,
            ai_explanation=ai_explanation,
            verification_timeline=timeline,
            ocr_success=ocr_success,
            liveness_confidence=round(liveness_confidence, 3),
            similarity_score=round(similarity_score, 3)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")

@app.post("/api/v1/verify/upload", response_model=VerificationResponse)
async def verify_identity_upload(
    face_image: UploadFile = File(...),
    id_document: UploadFile = File(...),
    device_id: str = "demo-device"
):
    """Demo verification with file upload, quality checks, and AI reasoning"""
    try:
        import random
        import time
        
        session_id = str(uuid4())
        
        # Build verification timeline
        timeline = [
            "Face image received and validated",
            "ID document received and validated",
        ]
        
        # Read and check files
        face_data = await face_image.read()
        id_data = await id_document.read()
        
        # Simulate processing
        time.sleep(random.uniform(1.5, 2.5))
        
        # Check file sizes (basic quality check)
        if len(face_data) < 1000 or len(id_data) < 1000:
            timeline.append("Image quality check failed")
            timeline.append("Verification terminated")
            
            return VerificationResponse(
                verification_id=session_id,
                status="FAILED",
                confidence_score=0.0,
                verification_method="QUALITY_CHECK",
                timestamp=datetime.utcnow(),
                message="❌ Image quality too low. Please upload clearer images.",
                fallback_required=True,
                fallback_options=["PIN", "OTP"],
                fraud_risk_score=0.0,
                risk_level="Low",
                ai_explanation="Verification could not proceed due to insufficient image quality. Both face and ID images must be clear and well-lit for accurate analysis.",
                verification_timeline=timeline,
                ocr_success=False,
                liveness_confidence=0.0,
                similarity_score=0.0
            )
        
        timeline.append("Image quality check passed")
        timeline.append("OCR extraction initiated")
        
        # Simulate varied results
        success_rate = random.random()
        
        # Generate realistic metrics
        similarity_score = random.uniform(0.85, 0.98) if success_rate > 0.5 else random.uniform(0.45, 0.75)
        liveness_confidence = random.uniform(0.88, 0.99) if success_rate > 0.5 else random.uniform(0.50, 0.80)
        ocr_success = random.random() > 0.1
        
        timeline.append("OCR extraction completed" if ocr_success else "OCR extraction failed")
        timeline.append("Face similarity analysis completed")
        timeline.append("Liveness detection completed")
        
        # Calculate fraud risk
        fraud_risk = calculate_fraud_risk(similarity_score, liveness_confidence, ocr_success)
        risk_level = get_risk_level(fraud_risk)
        
        timeline.append("Fraud risk analysis completed")
        
        if success_rate > 0.5:  # 50% success
            status = "SUCCESS"
            confidence = similarity_score
            message = f"✅ Identity verified! Face recognition: {int(similarity_score*100)}%, ID validation: {int((similarity_score+0.02)*100)}%, Liveness: Confirmed"
            fallback_required = False
            
            ai_explanation = generate_ai_explanation(status, similarity_score, liveness_confidence, ocr_success, fraud_risk)
            
        else:  # 50% failure
            status = "FAILED"
            confidence = similarity_score
            message = "❌ Verification failed. Face does not match ID document with sufficient confidence."
            fallback_required = True
            
            ai_explanation = generate_ai_explanation(status, similarity_score, liveness_confidence, ocr_success, fraud_risk)
        
        timeline.append("Verification result generated")
        
        # Update statistics
        increment_verification_stats(status, confidence)
        
        return VerificationResponse(
            verification_id=session_id,
            status=status,
            confidence_score=round(confidence, 3),
            verification_method="MULTI_MODAL",
            timestamp=datetime.utcnow(),
            message=message,
            fallback_required=fallback_required,
            fallback_options=["PIN", "OTP"] if fallback_required else None,
            fraud_risk_score=round(fraud_risk, 3),
            risk_level=risk_level,
            ai_explanation=ai_explanation,
            verification_timeline=timeline,
            ocr_success=ocr_success,
            liveness_confidence=round(liveness_confidence, 3),
            similarity_score=round(similarity_score, 3)
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

@app.get("/api/v1/analytics/admin")
async def get_admin_analytics():
    """
    Admin summary panel showing real-time verification statistics
    Displays metrics from current session
    """
    avg_confidence = (
        verification_stats["total_confidence"] / verification_stats["total"]
        if verification_stats["total"] > 0
        else 0.0
    )
    
    return {
        "total_verifications": verification_stats["total"],
        "approved_verifications": verification_stats["approved"],
        "flagged_verifications": verification_stats["flagged"],
        "average_confidence_score": round(avg_confidence, 3),
        "success_rate": round(
            verification_stats["approved"] / verification_stats["total"]
            if verification_stats["total"] > 0
            else 0.0,
            3
        ),
        "mode": "demo",
        "note": "Statistics are from current session only"
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
