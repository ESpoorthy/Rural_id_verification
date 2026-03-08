# RuralGuard AI

**Edge-First AI-Powered Identity Verification Platform for Rural Welfare Systems**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![AWS](https://img.shields.io/badge/AWS-Serverless-orange.svg)](https://aws.amazon.com/)

##  Problem Statement

Rural communities face significant barriers in accessing government welfare benefits due to:

- **Limited Infrastructure**: Unreliable internet connectivity and lack of verification centers
- **Identity Fraud**: Manual verification processes vulnerable to impersonation and document forgery
- **Accessibility Challenges**: Elderly and illiterate populations struggle with complex authentication systems
- **Privacy Concerns**: Centralized biometric databases pose security and privacy risks
- **Scalability Issues**: Traditional systems cannot handle the scale of rural welfare programs

These challenges result in delayed benefit distribution, increased fraud, and exclusion of legitimate beneficiaries from essential services.

##  Solution Overview

RuralGuard AI is an **edge-first, AI-powered identity verification platform** that brings secure, accessible authentication to rural welfare systems. Our solution leverages:

### Privacy by Design
- **Edge Processing**: Biometric verification happens locally on devices, not in the cloud
- **Encrypted Storage**: All sensitive data encrypted using AES-256-GCM
- **Minimal Data Retention**: Biometric templates stored as mathematical representations, not raw images
- **Zero-Knowledge Architecture**: Cloud services never access raw biometric data

### Edge-First Architecture
- **Offline Capability**: Core verification works without internet connectivity
- **Local AI Models**: Face recognition and liveness detection run on edge devices
- **Smart Synchronization**: Transaction logs sync when connectivity is available
- **Resilient Design**: System continues operating during network outages

### AI-Powered Verification
- **Multi-Modal Authentication**: Combines facial recognition, ID document verification, and liveness detection
- **Generative AI Reasoning**: Amazon Bedrock analyzes verification patterns and detects anomalies
- **Adaptive Fallback**: Intelligent system triggers PIN/OTP when biometric fails
- **Continuous Learning**: Models improve accuracy through federated learning

##  Why AI is Required

AI is not just an enhancement—it's essential for solving rural identity verification:

1. **Biometric Matching in Challenging Conditions**
   - Rural environments have poor lighting, low-quality cameras, and varying angles
   - Deep learning models can recognize faces despite these constraints
   - Traditional rule-based systems fail in these conditions

2. **Liveness Detection Against Spoofing**
   - AI detects presentation attacks (photos, videos, masks)
   - Analyzes micro-expressions and 3D depth information
   - Prevents fraud that manual verification cannot catch

3. **Document Verification and OCR**
   - AI extracts text from damaged, faded, or handwritten ID documents
   - Validates document authenticity by detecting forgeries
   - Handles diverse regional ID formats automatically

4. **Intelligent Fallback Decision Making**
   - Generative AI (Amazon Bedrock) analyzes authentication patterns
   - Determines when to trigger alternative authentication methods
   - Provides natural language explanations for verification decisions

5. **Anomaly Detection and Fraud Prevention**
   - ML models identify suspicious access patterns
   - Detects coordinated fraud attempts across multiple locations
   - Adapts to new fraud techniques without manual rule updates

6. **Accessibility Enhancement**
   - Computer vision guides users to position face and documents correctly
   - Natural language processing provides voice instructions in local languages
   - AI adapts interface complexity based on user literacy levels

##  AWS Services Used

### Core AI Services
- **Amazon Bedrock**: Generative AI for verification reasoning, anomaly detection, and natural language explanations
- **Amazon SageMaker**: Training and deploying custom face recognition and liveness detection models
- **Amazon Rekognition**: Backup facial analysis and comparison service

### Compute & Storage
- **AWS Lambda**: Serverless API endpoints for verification requests
- **Amazon S3**: Encrypted storage for ID documents and audit logs
- **Amazon DynamoDB**: NoSQL database for user profiles and transaction records
- **AWS IoT Greengrass**: Edge runtime for local AI model execution

### Security & Networking
- **AWS KMS**: Key management for encryption operations
- **Amazon Cognito**: User authentication and authorization
- **AWS WAF**: Web application firewall for API protection
- **Amazon CloudFront**: CDN for frontend delivery

### Monitoring & Operations
- **Amazon CloudWatch**: Logging and monitoring
- **AWS X-Ray**: Distributed tracing for debugging
- **Amazon SNS**: Notifications for suspicious activities

##  AWS Architecture Details

### Amazon Bedrock for AI Explanations

In production, **Amazon Bedrock** powers the intelligent reasoning layer of RuralGuard AI:

**Verification Explanations**: Bedrock's foundation models generate natural language explanations for every verification decision, making the system transparent and auditable. Instead of just returning "approved" or "denied", the system explains why based on similarity scores, liveness detection, and document validation.

**Fraud Pattern Analysis**: Bedrock analyzes verification patterns across regions to identify coordinated fraud attempts. It can detect anomalies like multiple verification attempts from the same device or unusual geographic patterns.

**Adaptive Recommendations**: When verification fails, Bedrock suggests the most appropriate fallback method (PIN, OTP, or in-person verification) based on the failure reason and user context.

**Example Bedrock Integration**:
```python
import boto3

bedrock = boto3.client('bedrock-runtime')

def generate_verification_explanation(similarity_score, liveness_confidence, ocr_success):
    prompt = f"""
    Analyze this identity verification result and provide a clear explanation:
    - Facial similarity: {similarity_score:.2%}
    - Liveness confidence: {liveness_confidence:.2%}
    - Document extraction: {'Success' if ocr_success else 'Failed'}
    
    Provide a 2-3 sentence explanation suitable for rural users.
    """
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-v2',
        body=json.dumps({
            "prompt": prompt,
            "max_tokens": 200,
            "temperature": 0.3
        })
    )
    
    return response['completion']
```

### AWS Lambda for Serverless Workflows

**Event-Driven Architecture**: Lambda functions handle verification requests, synchronization, and admin operations without managing servers. This ensures cost-efficiency and automatic scaling.

**Key Lambda Functions**:
- `verify-identity`: Processes verification requests and coordinates AI services
- `sync-offline-transactions`: Syncs edge device data when connectivity is restored
- `fraud-analysis`: Runs periodic fraud detection across all verifications
- `generate-reports`: Creates admin dashboards and compliance reports

**Benefits**:
- Pay only for actual verification requests
- Automatic scaling during peak welfare distribution periods
- No server maintenance or capacity planning
- Sub-second response times with provisioned concurrency

### Amazon S3 for Encrypted Artifacts

**Secure Document Storage**: All ID documents and verification artifacts are encrypted at rest using AWS KMS and stored in S3 with strict access controls.

**Storage Architecture**:
```
s3://ruralguard-verifications/
├── documents/
│   ├── {user-id}/
│   │   ├── id-card-{timestamp}.jpg.encrypted
│   │   └── face-image-{timestamp}.jpg.encrypted
├── audit-logs/
│   └── {year}/{month}/{day}/
│       └── verifications-{timestamp}.json
└── ml-models/
    └── face-recognition-v2.tar.gz
```

**Lifecycle Policies**: Documents are automatically moved to S3 Glacier after 90 days and deleted after 7 years per compliance requirements.

### Amazon DynamoDB for State Storage

**High-Performance NoSQL**: DynamoDB stores user profiles, verification sessions, and transaction logs with single-digit millisecond latency.

**Table Design**:
- `Users`: User profiles with biometric templates (encrypted)
- `VerificationSessions`: Active and historical verification attempts
- `AuditLogs`: Immutable audit trail for compliance
- `FamilyAuthorizations`: Family member access permissions

**Global Tables**: Multi-region replication ensures low latency for rural areas across different geographic regions.

**DynamoDB Streams**: Triggers Lambda functions for real-time fraud detection and analytics.

### Amazon SageMaker for Model Training

**Custom Model Development**: SageMaker trains and deploys specialized models optimized for rural conditions:

**Face Recognition Model**: Fine-tuned on diverse rural populations with varying lighting conditions, ages, and image quality.

**Liveness Detection Model**: Trained to detect presentation attacks using low-quality cameras common in rural areas.

**Document OCR Model**: Specialized for regional ID formats, handwritten text, and damaged documents.

**Training Pipeline**:
1. Data collection from edge devices (privacy-preserving)
2. Federated learning aggregation
3. Model training on SageMaker
4. A/B testing with shadow deployments
5. Gradual rollout to edge devices

**Model Monitoring**: SageMaker Model Monitor tracks model performance and detects drift, triggering retraining when accuracy degrades.

### Integration Flow

```
User Verification Request
        ↓
Edge Device (Local AI)
        ↓
[If online] → API Gateway → Lambda
        ↓
Amazon Bedrock (AI Explanation)
        ↓
DynamoDB (Store Result)
        ↓
S3 (Archive Documents)
        ↓
CloudWatch (Logging)
        ↓
SNS (Alerts if fraud detected)
```

### Cost Optimization

**Edge-First Design**: By processing most verifications locally, AWS costs are minimized. Cloud services are only used for:
- Synchronization of offline transactions
- Fraud analysis across multiple verifications
- Model updates and improvements
- Admin dashboards and reporting

**Estimated Monthly Cost** (for 100,000 rural beneficiaries):
- Lambda: $50 (pay-per-request)
- DynamoDB: $100 (on-demand pricing)
- S3: $30 (with lifecycle policies)
- Bedrock: $200 (AI explanations)
- SageMaker: $150 (model training)
- **Total: ~$530/month** vs. $10,000+ for traditional infrastructure

##  Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Edge Devices (Rural)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Mobile App   │  │ Kiosk Device │  │ Tablet       │      │
│  │              │  │              │  │              │      │
│  │ • Camera     │  │ • Camera     │  │ • Camera     │      │
│  │ • Local AI   │  │ • Local AI   │  │ • Local AI   │      │
│  │ • Offline DB │  │ • Offline DB │  │ • Offline DB │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │ Sync when connected
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      AWS Cloud Services                      │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              API Gateway + Lambda                   │    │
│  │  • Verification API  • Sync API  • Admin API       │    │
│  └─────────────┬──────────────────────┬────────────────┘    │
│                │                      │                     │
│       ┌────────▼────────┐    ┌───────▼────────┐           │
│       │  Amazon Bedrock │    │  Amazon S3     │           │
│       │  (Gen AI)       │    │  (Documents)   │           │
│       └─────────────────┘    └────────────────┘           │
│                │                      │                     │
│       ┌────────▼──────────────────────▼────────┐           │
│       │         Amazon DynamoDB                 │           │
│       │  • Users  • Sessions  • Audit Logs     │           │
│       └─────────────────────────────────────────┘           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

See [architecture/system-overview.md](architecture/system-overview.md) for detailed architecture documentation.

## ✨ Key Features

###  Secure Authentication
- Multi-factor biometric verification (face + ID + liveness)
- AES-256-GCM encryption for all sensitive data
- Secure key management with AWS KMS
- Comprehensive audit logging

###  Offline-First Design
- Local biometric verification without internet
- Automatic synchronization when connected
- Resilient to network outages
- Edge AI model execution

###  Family Authorization
- Authorized family members can access benefits on behalf of primary users
- Consent management and validation
- Proxy authentication with full audit trails

###  AI-Powered Intelligence
- Generative AI reasoning with Amazon Bedrock
- Adaptive authentication based on context
- Fraud detection and anomaly identification
- Natural language explanations

###  Accessibility
- Voice guidance in local languages
- Visual aids for illiterate users
- Simple 5-step verification process
- Support for users with disabilities

###  Scalability
- Serverless architecture scales automatically
- Handles millions of rural beneficiaries
- Cost-effective pay-per-use model
- Global edge deployment

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- AWS Account with appropriate permissions
- Node.js 14+ (for frontend)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ESpoorthy/Rural_id_verification.git
cd ruralguard-ai
```

2. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env
```

4. **Run the backend API locally**
```bash
python api.py
```

5. **Open the frontend**
```bash
cd ../frontend
# Open index.html in your browser or use a local server
python -m http.server 8000
```

6. **Access the application**
```
http://localhost:8000
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=rural_identity_verification --cov-report=html
```

##  Documentation

- [Project Overview](docs/project-overview.md) - Comprehensive project documentation
- [AI Design](docs/ai-design.md) - AI model architecture and design decisions
- [System Architecture](architecture/system-overview.md) - Detailed system architecture
- [AWS Architecture](architecture/aws-architecture.md) - AWS service integration
- [Deployment Guide](infrastructure/deployment_guide.md) - Step-by-step deployment instructions
- [API Documentation](backend/README.md) - API endpoints and usage

##  Demo

- **Demo Video**: https://drive.google.com/file/d/1JjnvjehKvGaIJTjtaV1xmwkMA5wsEPLu/view?usp=sharing
- **Live MVP**: https://main.d34ttefjam3p7q.amplifyapp.com
- **Screenshots**: See [demo-assets/screenshots/](demo-assets/screenshots/)

##  Innovation Highlights

1. **Edge-First AI**: First rural welfare platform with local AI processing
2. **Privacy by Design**: Zero-knowledge architecture protects beneficiary data
3. **Generative AI Integration**: Amazon Bedrock provides intelligent reasoning
4. **Offline Resilience**: Works without internet connectivity
5. **Inclusive Design**: Accessible to elderly and illiterate populations

##  Technology Stack

**Frontend**: HTML5, CSS3, JavaScript (Vanilla)  
**Backend**: Python, FastAPI, AWS Lambda  
**AI/ML**: Amazon SageMaker, Amazon Bedrock, TensorFlow, OpenCV  
**Database**: Amazon DynamoDB, Local SQLite (edge)  
**Storage**: Amazon S3  
**Infrastructure**: AWS CDK, Terraform  
**Security**: AWS KMS, Cryptography library  

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Contributing

We welcome contributions! Please see our contributing guidelines for more information.

##  Team

RuralGuard AI - Student Innovation Project  
- Sai Spoorthy Eturu
- Katakam Sahithi Rithvika

##  Contact

For questions or support, please contact: saispoorthyeturu6@gmail.com

##  Acknowledgments

- AWS for providing cloud infrastructure and AI services
- Open source community for libraries and tools
- Rural communities for feedback and testing

---

**Built with ❤️ for rural communities**
