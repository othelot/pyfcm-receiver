# FCM Receiver

A Python library for receiving Firebase Cloud Messages using the FCM protocol.

## Installation

```bash
pip install fcm-receiver
```

## Quick Start

```python
from fcm_receiver import FCMClient

# Initialize the client
client = FCMClient()

# Set your Firebase configuration
client.project_id = "shopee-ad86f"
client.api_key = "AIzaSyAPkv8NbRwcRTkNQK-xXJ1Za_IN2sPIYCg"
client.app_id = "1:808332928752:android:24633eecd863d5bd828435"

# Register the client
client.register()

# Create or load encryption keys
client.create_new_keys()

# Start listening for messages
def message_handler(message):
    print(f"Received message: {message}")

client.on_message = message_handler
client.start_listening()
```

## Firebase Configuration Example

Create a configuration file `config.py`:

```python
# config.py
FIREBASE_CONFIG = {
    "project_id": "shopee-ad86f",
    "api_key": "AIzaSyAPkv8NbRwcRTkNQK-xXJ1Za_IN2sPIYCg",
    "app_id": "1:808332928752:android:24633eecd863d5bd828435"
}

# Service account credentials (if needed)
SERVICE_ACCOUNT = {
    "type": "service_account",
    "project_id": "shopee-ad86f",
    "private_key_id": "your-private-key-id",
    "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-your-key@shopee-ad86f.iam.gserviceaccount.com",
    "client_id": "123456789",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token"
}
```

## Complete Example

```python
from fcm_receiver import FCMClient
import json
import time

def main():
    # Initialize client
    client = FCMClient()
    
    # Configure Firebase
    client.project_id = "shopee-ad86f"
    client.api_key = "AIzaSyAPkv8NbRwcRTkNQK-xXJ1Za_IN2sPIYCg"
    client.app_id = "1:808332928752:android:24633eecd863d5bd828435"
    
    # Set up status handler
    def status_handler(status):
        print(f"Status: {status}")
    
    client.on_status_change = status_handler
    
    # Set up message handler
    def message_handler(message):
        print(f"Received message:")
        print(json.dumps(message, indent=2))
    
    client.on_message = message_handler
    
    try:
        # Register with FCM
        print("Registering with FCM...")
        client.register()
        
        # Create encryption keys
        print("Creating encryption keys...")
        client.create_new_keys()
        
        # Subscribe to a topic (optional)
        print("Subscribing to topic...")
        client.subscribe_to_topic("news")
        
        # Start listening for messages
        print("Starting to listen for messages...")
        client.start_listening()
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
        client.close()
    except Exception as e:
        print(f"Error: {e}")
        client.close()

if __name__ == "__main__":
    main()
```

## Features

- Low-level FCM protocol implementation
- End-to-end encryption support
- Topic subscription/unsubscription
- Message receiving with callbacks
- Key management for encryption

## Development

Install development dependencies:

```bash
pip install -e .[dev]
```

Run tests:

```bash
pytest
```

## License

MIT License