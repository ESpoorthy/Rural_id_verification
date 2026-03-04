"""
Demo script to show the Rural Identity Verification System in action
"""
from datetime import datetime, UTC
from uuid import uuid4

from rural_identity_verification.models.user import User, PersonalInfo, ContactInfo
from rural_identity_verification.models.authentication_session import (
    AuthenticationSession, AuthenticationMethod
)
from rural_identity_verification.models.family_member import FamilyMember, Relationship
from rural_identity_verification.config.encryption import get_encryption_config

print("=" * 60)
print("Rural Identity Verification System - Demo")
print("=" * 60)

# 1. Show encryption configuration
print("\n1. Encryption Configuration:")
config = get_encryption_config()
print(f"   Algorithm: {config.algorithm}")
print(f"   Key Size: {config.key_size} bytes")
print(f"   Biometric Key: {config.biometric_key[:8].hex()}... (truncated)")

# 2. Create a user
print("\n2. Creating a User:")
personal_info = PersonalInfo(
    first_name="John",
    last_name="Doe",
    date_of_birth=datetime(1980, 5, 15),
    government_id="GOV123456"
)
contact_info = ContactInfo(
    phone_number="+1234567890",
    alternate_contact="+0987654321"
)
user = User(personal_info=personal_info, contact_info=contact_info)
print(f"   User ID: {user.user_id}")
print(f"   Name: {user.personal_info.first_name} {user.personal_info.last_name}")
print(f"   Status: {user.status.value}")
print(f"   Created: {user.created_at}")

# 3. Create an authentication session
print("\n3. Creating Authentication Session:")
session = AuthenticationSession(
    user_id=user.user_id,
    device_id="DEVICE_001"
)
print(f"   Session ID: {session.session_id}")
print(f"   Status: {session.status.value}")
print(f"   Expires: {session.expires_at}")

# 4. Add authentication attempts
print("\n4. Simulating Authentication Attempts:")
session.add_attempt(AuthenticationMethod.FACE_ID, success=False, failure_reason="Poor lighting")
session.add_attempt(AuthenticationMethod.FACE_ID, success=False, failure_reason="Face not detected")
session.add_attempt(AuthenticationMethod.FACE_ID, success=False, failure_reason="Low confidence")
print(f"   Failed attempts: {session.get_failed_attempts_count()}")
print(f"   Should trigger fallback: {session.should_trigger_fallback()}")

# 5. Use fallback authentication
print("\n5. Using Fallback Authentication (PIN):")
session.add_attempt(AuthenticationMethod.PIN, success=True)
session.complete_session(success=True)
print(f"   Session Status: {session.status.value}")
print(f"   Completed At: {session.completed_at}")

# 6. Add a family member
print("\n6. Adding Family Member:")
family_member = FamilyMember(
    primary_user_id=user.user_id,
    relationship=Relationship.SPOUSE
)
family_member.grant_consent()
family_member.activate()
user.add_family_member(family_member)
print(f"   Family Member ID: {family_member.family_member_id}")
print(f"   Relationship: {family_member.relationship.value}")
print(f"   Has Valid Authorization: {family_member.has_valid_authorization()}")

# 7. Summary
print("\n" + "=" * 60)
print("Demo Complete!")
print("=" * 60)
print(f"\nTotal Users: 1")
print(f"Total Sessions: 1")
print(f"Total Family Members: {len(user.family_members)}")
print(f"Authentication Success: {session.status.value == 'SUCCESS'}")
print("\nThis is a backend library - no UI to display.")
print("To build a full application, you would need to add:")
print("  - Web frontend (React, Vue, etc.)")
print("  - API server (Flask, FastAPI, Django)")
print("  - Mobile app (React Native, Flutter)")
print("=" * 60)
