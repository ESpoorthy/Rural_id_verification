"""
RuralGuard AI - AWS Lambda Handler
Serverless function for identity verification
"""

import json
import base64
from typing import Dict, Any
from verification_service import VerificationService

# Initialize service (reused across invocations)
verification_service = VerificationService()


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for verification requests
    
    Supports API Gateway integration with proxy mode
    """
    
    try:
        # Parse request
        http_method = event.get('httpMethod', 'POST')
        path = event.get('path', '')
        body = json.loads(event.get('body', '{}'))
        
        # Route to appropriate handler
        if path == '/api/v1/verify' and http_method == 'POST':
            return handle_verification(body)
        
        elif path == '/api/v1/verify/pin' and http_method == 'POST':
            return handle_pin_verification(body)
        
        elif path == '/api/v1/verify/otp/request' and http_method == 'POST':
            return handle_otp_request(body)
        
        elif path == '/api/v1/verify/otp/validate' and http_method == 'POST':
            return handle_otp_verification(body)
        
        elif path.startswith('/api/v1/session/') and http_method == 'GET':
            session_id = path.split('/')[-1]
            return handle_get_session(session_id)
        
        elif path == '/api/v1/sync/offline-transactions' and http_method == 'POST':
            return handle_sync(body)
        
        elif path == '/health' and http_method == 'GET':
            return create_response(200, {
                'status': 'healthy',
                'service': 'RuralGuard AI Lambda'
            })
        
        else:
            return create_response(404, {
                'error': 'Not Found',
                'message': f'Path {path} not found'
            })
    
    except Exception as e:
        return create_response(500, {
            'error': 'Internal Server Error',
            'message': str(e)
        })


def handle_verification(body: Dict) -> Dict:
    """Handle identity verification request"""
    try:
        # Extract data
        face_image = base64.b64decode(body['face_image_base64'])
        id_document = base64.b64decode(body['id_document_base64'])
        user_id = body.get('user_id')
        device_id = body.get('device_id', 'unknown')
        location = body.get('location')
        
        # Perform verification (synchronous for Lambda)
        import asyncio
        result = asyncio.run(verification_service.verify_identity(
            face_image=face_image,
            id_document=id_document,
            user_id=user_id,
            device_id=device_id,
            location=location
        ))
        
        return create_response(200, result)
    
    except KeyError as e:
        return create_response(400, {
            'error': 'Bad Request',
            'message': f'Missing required field: {str(e)}'
        })
    except Exception as e:
        return create_response(500, {
            'error': 'Verification Failed',
            'message': str(e)
        })


def handle_pin_verification(body: Dict) -> Dict:
    """Handle PIN verification request"""
    try:
        import asyncio
        result = asyncio.run(verification_service.verify_pin(
            user_id=body['user_id'],
            pin=body['pin'],
            session_id=body['session_id']
        ))
        
        return create_response(200, result)
    
    except Exception as e:
        return create_response(400, {
            'error': 'PIN Verification Failed',
            'message': str(e)
        })


def handle_otp_request(body: Dict) -> Dict:
    """Handle OTP request"""
    try:
        import asyncio
        result = asyncio.run(verification_service.request_otp(
            user_id=body['user_id'],
            phone_number=body['phone_number']
        ))
        
        return create_response(200, {
            'status': 'success',
            'message': 'OTP sent successfully',
            'session_id': result['session_id']
        })
    
    except Exception as e:
        return create_response(500, {
            'error': 'OTP Request Failed',
            'message': str(e)
        })


def handle_otp_verification(body: Dict) -> Dict:
    """Handle OTP verification"""
    try:
        import asyncio
        result = asyncio.run(verification_service.verify_otp(
            user_id=body['user_id'],
            otp=body['otp'],
            session_id=body['session_id']
        ))
        
        return create_response(200, result)
    
    except Exception as e:
        return create_response(400, {
            'error': 'OTP Verification Failed',
            'message': str(e)
        })


def handle_get_session(session_id: str) -> Dict:
    """Handle get session request"""
    try:
        import asyncio
        session = asyncio.run(verification_service.get_session(session_id))
        
        if not session:
            return create_response(404, {
                'error': 'Not Found',
                'message': 'Session not found'
            })
        
        return create_response(200, session)
    
    except Exception as e:
        return create_response(500, {
            'error': 'Failed to Retrieve Session',
            'message': str(e)
        })


def handle_sync(body: Dict) -> Dict:
    """Handle offline transaction sync"""
    try:
        transactions = body.get('transactions', [])
        
        import asyncio
        result = asyncio.run(verification_service.sync_offline_transactions(transactions))
        
        return create_response(200, {
            'status': 'success',
            'synced_count': result['synced_count'],
            'failed_count': result['failed_count']
        })
    
    except Exception as e:
        return create_response(500, {
            'error': 'Sync Failed',
            'message': str(e)
        })


def create_response(status_code: int, body: Dict) -> Dict:
    """Create API Gateway response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(body, default=str)
    }


# For local testing
if __name__ == "__main__":
    # Test event
    test_event = {
        'httpMethod': 'GET',
        'path': '/health',
        'body': '{}'
    }
    
    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))
