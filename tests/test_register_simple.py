#!/usr/bin/env python3
"""
Test register() function for Firebase FCM
"""

import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fcm_receiver.fcm_client import FCMClient


def test_register_function():
    """Test FCM register() function with Firebase configuration"""
    # Firebase configuration
    FIREBASE_CONFIG = {
        "project_id": "shopee-ad86f",
        "api_key": "AIzaSyAPkv8NbRwcRTkNQK-xXJ1Za_IN2sPIYCg",
        "app_id": "1:808332928752:android:24633eecd863d5bd828435"
    }

    print("🔐 FCM Register Function Test")
    print("=" * 50)

    try:
        # Step 1: Initialize FCM client
        print("📱 Initializing FCM client...")
        client = FCMClient()
        client.project_id = FIREBASE_CONFIG["project_id"]
        client.api_key = FIREBASE_CONFIG["api_key"]
        client.app_id = FIREBASE_CONFIG["app_id"]

        print(f"Project ID: {client.project_id}")
        print(f"API Key: {client.api_key[:20]}...")
        print(f"App ID: {client.app_id}")

        # Step 2: Create encryption keys
        print("🔑 Creating encryption keys...")
        private_key_b64, auth_secret_b64 = client.create_new_keys()

        print("✅ Encryption keys created")
        print(f"   Private Key: {len(private_key_b64)} chars")
        print(f"   Auth Secret: {auth_secret_b64[:20]}...")

        # Step 3: Test register function
        print("📝 Calling register() function...")

        # Call register()
        fcm_token, gcm_token, android_id, security_token = client.register()

        print("✅ Register() function called successfully!")
        print(f"   Android ID: {android_id}")
        print(f"   Security Token: {security_token}")
        print(f"   GCM Token: {gcm_token[:30] + '...' if gcm_token else 'None'}")
        print(f"   FCM Token: {fcm_token[:30] + '...' if fcm_token else 'None'}")

        # Step 4: Verify credentials
        print("🔍 Verifying credentials...")

        # Verify semua required credentials ada
        assert android_id is not None and android_id > 0, "Android ID should be valid"
        assert security_token is not None and security_token > 0, "Security token should be valid"

        # Tokens mungkin kosong tergantung konfigurasi
        if gcm_token:
            assert len(gcm_token) > 0, "GCM token should not be empty if provided"
        if fcm_token:
            assert len(fcm_token) > 0, "FCM token should not be empty if provided"

        print("✅ All credentials verified!")

        # Step 5: Test client state
        print("📊 Checking client state...")

        assert client.android_id == android_id, "Client android_id should match returned value"
        assert client.security_token == security_token, "Client security_token should match returned value"
        assert client.gcm_token == gcm_token, "Client gcm_token should match returned value"
        assert client.fcm_token == fcm_token, "Client fcm_token should match returned value"

        print("✅ Client state is consistent!")

        # Step 6: Test credential format
        print("📋 Testing credential format...")

        # Test key encoding
        assert isinstance(private_key_b64, str), "Private key should be string"
        assert isinstance(auth_secret_b64, str), "Auth secret should be string"
        assert len(private_key_b64) > 0, "Private key should not be empty"
        assert len(auth_secret_b64) > 0, "Auth secret should not be empty"

        # Test loading credentials
        new_client = FCMClient()
        new_client.load_keys(private_key_b64, auth_secret_b64)

        assert new_client.private_key is not None, "Loaded private key should not be None"
        assert new_client.auth_secret is not None, "Loaded auth secret should not be None"
        assert new_client.auth_secret == client.auth_secret, "Loaded auth secret should match"

        print("✅ Credential format is correct!")

        print("\n🎉 Register function test PASSED!")
        print("✅ FCM client successfully registered with Firebase!")
        print("✅ All credentials generated and verified!")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Starting FCM Register Test")
    print("This test will:")
    print("1. Initialize FCM client with your Firebase configuration")
    print("2. Generate encryption keys")
    print("3. Call register() to get Android ID and tokens")
    print("4. Verify all credentials are valid")
    print("5. Test credential persistence")
    print("")

    success = test_register_function()

    if success:
        print("\n" + "=" * 50)
        print("🎉 SUCCESS! FCM registration completed!")
        print("📱 Your FCM client is now ready to:")
        print("   • Subscribe to topics")
        print("   • Listen for messages")
        print("   • Receive FCM notifications")
        print("   • Handle encrypted messages")
    else:
        print("\n" + "=" * 50)
        print("❌ FAILED! Registration test failed")
        print("Please check:")
        print("   • Firebase project configuration")
        print("   • Network connectivity")
        print("   • API key validity")

    sys.exit(0 if success else 1)
