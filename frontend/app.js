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
    
    resultContent.innerHTML = `
        <div class="result ${statusClass}">
            <div class="result-icon">${statusIcon}</div>
            <h3>${result.status === 'SUCCESS' ? 'Verification Successful' : 'Verification Failed'}</h3>
            <p>${result.message}</p>
            <div class="result-details">
                <p><strong>Confidence Score:</strong> ${(result.confidence_score * 100).toFixed(1)}%</p>
                <p><strong>Method:</strong> ${result.verification_method}</p>
                <p><strong>Session ID:</strong> ${result.verification_id}</p>
            </div>
        </div>
    `;
    
    resultSection.style.display = 'block';
    
    // Show fallback options if needed
    if (result.fallback_required) {
        document.getElementById('fallbackSection').style.display = 'block';
    }
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
        buttonText.style.display = 'none';
        buttonLoader.style.display = 'inline-block';
    } else {
        button.disabled = false;
        buttonText.style.display = 'inline';
        buttonLoader.style.display = 'none';
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
