"""
RuralGuard AI - FastAPI Backend
Main API server for identity verification
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, UUID4
from typing import Optional, List
import uvicorn
from datetime import datetime
import base64
import io

from verification_service import VerificationService

app = FastAPI(
    title="RuralGuard AI API",
    description="Edge-First AI-Powered Identity Verification Platform",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize verification service
verification_service = VerificationService()


# Request/Response Models
class VerificationRequest(BaseModel):
    user_id: Optional[UUID4] = None
    device_id: str
    face_image_base64: str
    id_document_base64: str
    location: Optional[dict] = None


class VerificationResponse(BaseModel):
    verification_id: str
    status: str  # SUCCESS, FAILED, PENDING
    confidence_score: float
    verification_method: str
    timestamp: datetime
    message: str
    fallback_required: bool = False
    fallback_options: Optional[List[str]] = None


class PINVerificationRequest(BaseModel):
    user_id: UUID4
    pin: str
    session_id: str


class OTPRequest(BaseModel):
    user_id: UUID4
    phone_number: str


class OTPVerificationRequest(BaseModel):
    user_id: UUID4
    otp: str
    session_id: str


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    services: dict


# API Endpoints

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "name": "RuralGuard AI API",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        services={
            "api": "operational",
            "ai_models": "operational",
            "database": "operational",
            "aws_services": "operational"
        }
    )


@app.post("/api/v1/verify", response_model=VerificationResponse)
async def verify_identity(request: VerificationRequest):
    """
    Primary identity verification endpoint
    
    Performs multi-modal verification:
    1. Face recognition
    2. Liveness detection
    3. ID document verification
    4. AI reasoning with Amazon Bedrock
    
    Returns verification result with confidence score
    """
    try:
        # Decode base64 images
        face_image = base64.b64decode(request.face_image_base64)
        id_document = base64.b64decode(request.id_document_base64)
        
        # Perform verification
        result = await verification_service.verify_identity(
            face_image=face_image,
            id_document=id_document,
            user_id=request.user_id,
            device_id=request.device_id,
            location=request.location
        )
        
        return VerificationResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")


@app.post("/api/v1/verify/upload", response_model=VerificationResponse)
async def verify_identity_upload(
    face_image: UploadFile = File(...),
    id_document: UploadFile = File(...),
    device_id: str = "unknown"
):
    """
    Identity verification with file upload
    
    Alternative endpoint that accepts multipart form data
    Useful for direct file uploads from frontend
    """
    try:
        # Read uploaded files
        face_data = await face_image.read()
        id_data = await id_document.read()
        
        # Perform verification
        result = await verification_service.verify_identity(
            face_image=face_data,
            id_document=id_data,
            user_id=None,
            device_id=device_id,
            location=None
        )
        
        return VerificationResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")


@app.post("/api/v1/verify/pin", response_model=VerificationResponse)
async def verify_pin(request: PINVerificationRequest):
    """
    PIN-based fallback authentication
    
    Used when biometric verification fails
    Validates 6-digit PIN against stored credentials
    """
    try:
        result = await verification_service.verify_pin(
            user_id=request.user_id,
            pin=request.pin,
            session_id=request.session_id
        )
        
        return VerificationResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PIN verification failed: {str(e)}")


@app.post("/api/v1/verify/otp/request")
async def request_otp(request: OTPRequest):
    """
    Request OTP for fallback authentication
    
    Generates and sends OTP to registered phone number
    """
    try:
        result = await verification_service.request_otp(
            user_id=request.user_id,
            phone_number=request.phone_number
        )
        
        return {
            "status": "success",
            "message": "OTP sent successfully",
            "session_id": result["session_id"],
            "expires_in": 300  # 5 minutes
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OTP request failed: {str(e)}")


@app.post("/api/v1/verify/otp/validate", response_model=VerificationResponse)
async def verify_otp(request: OTPVerificationRequest):
    """
    Validate OTP for fallback authentication
    
    Verifies OTP code against generated value
    """
    try:
        result = await verification_service.verify_otp(
            user_id=request.user_id,
            otp=request.otp,
            session_id=request.session_id
        )
        
        return VerificationResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OTP verification failed: {str(e)}")


@app.get("/api/v1/session/{session_id}")
async def get_session_status(session_id: str):
    """
    Get authentication session status
    
    Returns current status and details of verification session
    """
    try:
        session = await verification_service.get_session(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return session
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve session: {str(e)}")


@app.post("/api/v1/sync/offline-transactions")
async def sync_offline_transactions(transactions: List[dict]):
    """
    Sync offline transactions from edge devices
    
    Accepts batch of transactions completed while offline
    Processes and stores them in cloud database
    """
    try:
        result = await verification_service.sync_offline_transactions(transactions)
        
        return {
            "status": "success",
            "synced_count": result["synced_count"],
            "failed_count": result["failed_count"],
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")


@app.get("/api/v1/analytics/summary")
async def get_analytics_summary():
    """
    Get verification analytics summary
    
    Returns aggregated statistics for monitoring
    """
    try:
        analytics = await verification_service.get_analytics()
        
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analytics: {str(e)}")


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Not Found",
        "message": "The requested resource was not found",
        "status_code": 404
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "status_code": 500
    }


if __name__ == "__main__":
    # Run the API server
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
