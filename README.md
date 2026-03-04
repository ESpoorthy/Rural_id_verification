# RuralGuard AI

**Edge-First AI-Powered Identity Verification Platform for Rural Welfare Systems**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![AWS](https://img.shields.io/badge/AWS-Serverless-orange.svg)](https://aws.amazon.com/)

## 🌾 Problem Statement

Rural communities face significant barriers in accessing government welfare benefits due to:

- **Limited Infrastructure**: Unreliable internet connectivity and lack of verification centers
- **Identity Fraud**: Manual verification processes vulnerable to impersonation and document forgery
- **Accessibility Challenges**: Elderly and illiterate populations struggle with complex authentication systems
- **Privacy Concerns**: Centralized biometric databases pose security and privacy risks
- **Scalability Issues**: Traditional systems cannot handle the scale of rural welfare programs

These challenges result in delayed benefit distribution, increased fraud, and exclusion of legitimate beneficiaries from essential services.

## 💡 Solution Overview

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

## 🤖 Why AI is Required

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

## ☁️ AWS Services Used

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

## 🏗️ Architecture Overview

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

### 🔐 Secure Authentication
- Multi-factor biometric verification (face + ID + liveness)
- AES-256-GCM encryption for all sensitive data
- Secure key management with AWS KMS
- Comprehensive audit logging

### 🌐 Offline-First Design
- Local biometric verification without internet
- Automatic synchronization when connected
- Resilient to network outages
- Edge AI model execution

### 👨‍👩‍👧‍👦 Family Authorization
- Authorized family members can access benefits on behalf of primary users
- Consent management and validation
- Proxy authentication with full audit trails

### 🤖 AI-Powered Intelligence
- Generative AI reasoning with Amazon Bedrock
- Adaptive authentication based on context
- Fraud detection and anomaly identification
- Natural language explanations

### ♿ Accessibility
- Voice guidance in local languages
- Visual aids for illiterate users
- Simple 5-step verification process
- Support for users with disabilities

### 📊 Scalability
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
git clone https://github.com/yourusername/ruralguard-ai.git
cd ruralguard-ai
```

2. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your AWS credentials and configuration
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

## 📚 Documentation

- [Project Overview](docs/project-overview.md) - Comprehensive project documentation
- [AI Design](docs/ai-design.md) - AI model architecture and design decisions
- [System Architecture](architecture/system-overview.md) - Detailed system architecture
- [AWS Architecture](architecture/aws-architecture.md) - AWS service integration
- [Deployment Guide](infrastructure/deployment_guide.md) - Step-by-step deployment instructions
- [API Documentation](backend/README.md) - API endpoints and usage

## 🎥 Demo

- **Demo Video**: [Watch on YouTube](#) *(Coming Soon)*
- **Live MVP**: [https://ruralguard-ai-demo.aws.com](#) *(Coming Soon)*
- **Screenshots**: See [demo-assets/screenshots/](demo-assets/screenshots/)

## 🏆 Innovation Highlights

1. **Edge-First AI**: First rural welfare platform with local AI processing
2. **Privacy by Design**: Zero-knowledge architecture protects beneficiary data
3. **Generative AI Integration**: Amazon Bedrock provides intelligent reasoning
4. **Offline Resilience**: Works without internet connectivity
5. **Inclusive Design**: Accessible to elderly and illiterate populations

## 🛠️ Technology Stack

**Frontend**: HTML5, CSS3, JavaScript (Vanilla)  
**Backend**: Python, FastAPI, AWS Lambda  
**AI/ML**: Amazon SageMaker, Amazon Bedrock, TensorFlow, OpenCV  
**Database**: Amazon DynamoDB, Local SQLite (edge)  
**Storage**: Amazon S3  
**Infrastructure**: AWS CDK, Terraform  
**Security**: AWS KMS, Cryptography library  

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for more information.

## 👥 Team

RuralGuard AI - Student Innovation Project  
[Your University Name]  
[Your Team Members]

## 📧 Contact

For questions or support, please contact: [your-email@example.com]

## 🙏 Acknowledgments

- AWS for providing cloud infrastructure and AI services
- Open source community for libraries and tools
- Rural communities for feedback and testing

---

**Built with ❤️ for rural communities**
