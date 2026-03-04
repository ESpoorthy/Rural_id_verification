// RuralGuard AI - Frontend Application
// Handles user interactions and API communication

const API_BASE_URL = 'http://localhost:8000/api/v1';
let currentSessionId = null;

// Generate device ID
function getDeviceId() {
    let deviceId = localStorage.getItem('deviceId');
    if (!deviceId) {
        deviceId = 'device_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('deviceId', deviceId);
    }
    return deviceId;
}

document.getElementById('deviceId').value = getDeviceId();

// Image preview handlers
document.getElementById('faceImage').addEventListener('change', function(e) {
    previewImage(e.target.files[0], 'facePreview');
    updateStep(1);
});

document.getElementById('idDocument').addEventListener('change', function(e) {
    previewImage(e.target.files[0], 'idPreview');
    updateStep(2);
});

function previewImage(file, previewId) {
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById(previewId);
            preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

function updateStep(step) {
    for (let i = 1; i <= 3; i++) {
        const stepEl = document.getElementById(`step${i}`);
        if (i <= step) {
            stepEl.classList.add('active');
        }
    }
}

// Form submission
document.getElementById('verificationForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const faceImage = document.getElementById('faceImage').files[0];
    const idDocument = document.getElementById('idDocument').files[0];
    
    if (!faceImage || !idDocument) {
        showError('Please upload both face image and ID document');
        return;
    }
    
    // Show loading
    setLoading(true);
    updateStep(3);
    
    // Show progress bar
    const progressBar = document.getElementById('progressBar');
    const resultSection = document.getElementById('resultSection');
    resultSection.style.display = 'block';
    progressBar.style.display = 'block';
    document.getElementById('resultContent').style.display = 'none';
    
    try {
        // Convert images to base64
        const faceBase64 = await fileToBase64(faceImage);
        const idBase64 = await fileToBase64(idDocument);
        
        // Call verification API
        const response = await fetch(`${API_BASE_URL}/verify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                face_image_base64: faceBase64.split(',')[1],
                id_document_base64: idBase64.split(',')[1],
                device_id: getDeviceId(),
                location: await getLocation()
            })
        });
        
        const result = await response.json();
        currentSessionId = result.verification_id;
        
        // Hide progress bar and show result
        progressBar.style.display = 'none';
        document.getElementById('resultContent').style.display = 'block';
        
        // Display result
        displayResult(result);
        
    } catch (error) {
        showError('Verification failed: ' + error.message);
    } finally {
        setLoading(false);
    }
});

function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

async function getLocation() {
    return new Promise((resolve) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => resolve({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                }),
                () => resolve(null)
            );
        } else {
            resolve(null);
        }
    });
}

function displayResult(result) {
    const resultSection = document.getElementById('resultSection');
    const resultContent = document.getElementById('resultContent');
    
    const statusClass = result.status === 'SUCCESS' ? 'success' : 'failure';
    const statusIcon = result.status === 'SUCCESS' ? '✅' : '❌';
    const statusText = result.status === 'SUCCESS' ? 'Verification Successful' : 'Verification Failed';
    
    // Determine confidence level
    let confidenceLevel = 'Low';
    let confidenceColor = '#dc3545';
    if (result.confidence_score >= 0.85) {
        confidenceLevel = 'High';
        confidenceColor = '#28a745';
    } else if (result.confidence_score >= 0.70) {
        confidenceLevel = 'Medium';
        confidenceColor = '#ffc107';
    }
    
    // Determine risk level color
    let riskColor = '#28a745'; // Low = green
    if (result.risk_level === 'Medium') {
        riskColor = '#ffc107'; // Medium = yellow
    } else if (result.risk_level === 'High') {
        riskColor = '#dc3545'; // High = red
    }
    
    // Build verification timeline HTML
    let timelineHTML = '<div class="verification-timeline"><h4>Verification Timeline</h4><ul>';
    result.verification_timeline.forEach((step, index) => {
        timelineHTML += `<li><span class="timeline-step">${index + 1}.</span> ${step}</li>`;
    });
    timelineHTML += '</ul></div>';
    
    resultContent.innerHTML = `
        <div class="result ${statusClass}" style="animation: slideIn 0.5s ease-out;">
            <div class="result-icon">${statusIcon}</div>
            <h3>${statusText}</h3>
            <p class="result-message">${result.message}</p>
            
            <div class="result-details">
                <div class="detail-row">
                    <strong>Confidence Score:</strong> 
                    <span style="color: ${confidenceColor}; font-weight: bold;">
                        ${(result.confidence_score * 100).toFixed(1)}% (${confidenceLevel})
                    </span>
                </div>
                <div class="detail-row">
                    <strong>Fraud Risk Score:</strong> 
                    <span style="color: ${riskColor}; font-weight: bold;">
                        ${(result.fraud_risk_score * 100).toFixed(1)}%
                    </span>
                </div>
                <div class="detail-row">
                    <strong>Risk Level:</strong> 
                    <span style="color: ${riskColor}; font-weight: bold;">
                        ${result.risk_level}
                    </span>
                </div>
                <div class="detail-row">
                    <strong>Similarity Score:</strong> ${(result.similarity_score * 100).toFixed(1)}%
                </div>
                <div class="detail-row">
                    <strong>Liveness Confidence:</strong> ${(result.liveness_confidence * 100).toFixed(1)}%
                </div>
                <div class="detail-row">
                    <strong>OCR Extraction:</strong> ${result.ocr_success ? '✓ Success' : '✗ Failed'}
                </div>
                <div class="detail-row">
                    <strong>Method:</strong> ${result.verification_method}
                </div>
                <div class="detail-row">
                    <strong>Session ID:</strong> 
                    <code>${result.verification_id.substring(0, 8)}...</code>
                </div>
                <div class="detail-row">
                    <strong>Timestamp:</strong> ${new Date(result.timestamp).toLocaleString()}
                </div>
            </div>
            
            <div class="ai-explanation">
                <h4>🤖 AI Verification Explanation</h4>
                <p>${result.ai_explanation}</p>
                <p class="ai-note"><em>Note: In production, Amazon Bedrock would generate more sophisticated explanations based on comprehensive analysis.</em></p>
            </div>
            
            ${timelineHTML}
            
            ${result.status === 'SUCCESS' ? `
                <div class="success-actions" style="margin-top: 20px;">
                    <button onclick="location.reload()" class="action-button">
                        ✓ Complete & Start New
                    </button>
                </div>
            ` : ''}
        </div>
    `;
    
    resultSection.style.display = 'block';
    
    // Show fallback options if needed
    if (result.fallback_required) {
        document.getElementById('fallbackSection').style.display = 'block';
        // Scroll to fallback section
        setTimeout(() => {
            document.getElementById('fallbackSection').scrollIntoView({ behavior: 'smooth' });
        }, 500);
    } else {
        document.getElementById('fallbackSection').style.display = 'none';
    }
    
    // Load admin stats
    loadAdminStats();
}

function showError(message) {
    const resultSection = document.getElementById('resultSection');
    const resultContent = document.getElementById('resultContent');
    
    resultContent.innerHTML = `
        <div class="result failure">
            <div class="result-icon">⚠️</div>
            <h3>Error</h3>
            <p>${message}</p>
        </div>
    `;
    
    resultSection.style.display = 'block';
}

function setLoading(loading) {
    const button = document.getElementById('verifyButton');
    const buttonText = document.getElementById('buttonText');
    const buttonLoader = document.getElementById('buttonLoader');
    
    if (loading) {
        button.disabled = true;
        button.style.opacity = '0.7';
        buttonText.textContent = 'Verifying...';
        buttonLoader.style.display = 'inline-block';
        
        // Add processing animation
        button.style.animation = 'pulse 1.5s infinite';
    } else {
        button.disabled = false;
        button.style.opacity = '1';
        buttonText.textContent = 'Verify Identity';
        buttonLoader.style.display = 'none';
        button.style.animation = 'none';
    }
}

// Fallback authentication functions
function showPINVerification() {
    document.getElementById('pinModal').style.display = 'block';
}

function closePINModal() {
    document.getElementById('pinModal').style.display = 'none';
}

async function verifyPIN() {
    const pin = document.getElementById('pinInput').value;
    
    if (pin.length !== 6) {
        alert('Please enter a 6-digit PIN');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/verify/pin`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: 'demo-user',
                pin: pin,
                session_id: currentSessionId
            })
        });
        
        const result = await response.json();
        closePINModal();
        displayResult(result);
        
    } catch (error) {
        alert('PIN verification failed: ' + error.message);
    }
}

function showOTPVerification() {
    document.getElementById('otpModal').style.display = 'block';
}

function closeOTPModal() {
    document.getElementById('otpModal').style.display = 'none';
}

async function requestOTP() {
    const phone = document.getElementById('phoneInput').value;
    
    if (!phone) {
        alert('Please enter your phone number');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/verify/otp/request`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: 'demo-user',
                phone_number: phone
            })
        });
        
        const result = await response.json();
        currentSessionId = result.session_id;
        
        document.getElementById('otpInputSection').style.display = 'block';
        alert('OTP sent successfully!');
        
    } catch (error) {
        alert('Failed to send OTP: ' + error.message);
    }
}

async function verifyOTP() {
    const otp = document.getElementById('otpInput').value;
    
    if (otp.length !== 6) {
        alert('Please enter a 6-digit OTP');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/verify/otp/validate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: 'demo-user',
                otp: otp,
                session_id: currentSessionId
            })
        });
        
        const result = await response.json();
        closeOTPModal();
        displayResult(result);
        
    } catch (error) {
        alert('OTP verification failed: ' + error.message);
    }
}

// Load admin statistics
async function loadAdminStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/analytics/admin`);
        const stats = await response.json();
        
        const adminPanel = document.getElementById('adminPanel');
        if (adminPanel) {
            document.getElementById('totalVerifications').textContent = stats.total_verifications;
            document.getElementById('approvedVerifications').textContent = stats.approved_verifications;
            document.getElementById('flaggedVerifications').textContent = stats.flagged_verifications;
            document.getElementById('avgConfidence').textContent = (stats.average_confidence_score * 100).toFixed(1) + '%';
            
            adminPanel.style.display = 'block';
        }
    } catch (error) {
        console.error('Failed to load admin stats:', error);
    }
}

// Load admin stats on page load
window.addEventListener('load', loadAdminStats);
