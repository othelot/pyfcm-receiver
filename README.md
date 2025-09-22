<div align="center">
  <h1>🔥 FCM Receiver</h1>
  <p>Powerful Python library for receiving Firebase Cloud Messages with end-to-end encryption support</p>

  [![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
  [![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)

  <p>
    <a href="#-installation">Installation</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-features">Features</a> •
    <a href="#-examples">Examples</a> •
    <a href="#-advanced-usage">Advanced Usage</a>
  </p>
</div>

---

## 🚀 What is FCM Receiver?

FCM Receiver is a robust Python library that implements low-level Firebase Cloud Messaging protocol for receiving push notifications with full end-to-end encryption support. Unlike official Firebase SDKs, this library gives you complete control over the FCM protocol while maintaining security and reliability.

### ✨ Key Highlights

- 🔐 **End-to-End Encryption** - Full E2EE support with elliptic curve cryptography
- 📱 **Multi-Project Support** - Connect to multiple Firebase projects simultaneously
- 🔄 **Auto-Reconnection** - Automatic reconnection with exponential backoff
- 💾 **Credential Management** - Persistent credential storage and loading
- 🎯 **Topic Subscription** - Subscribe/unsubscribe from FCM topics dynamically
- 📊 **Real-time Monitoring** - Comprehensive status callbacks and logging
- 🔧 **No Firebase SDK Dependency** - Direct protocol implementation

---

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install fcm-receiver
```

### From Source

```bash
git clone https://github.com/agusibrahim/pyfcm-receiver.git
cd pyfcm-receiver
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/agusibrahim/pyfcm-receiver.git
cd pyfcm-receiver
pip install -e .[dev]
```

---

## 🎯 Quick Start

### Basic Usage - Single Project

```python
from fcm_receiver import FCMClient
import json
import time

def main():
    # Initialize client
    client = FCMClient()

    # Configure Firebase
    client.project_id = "your-project-id"
    client.api_key = "your-api-key"
    client.app_id = "your-app-id"

    # Set up message handler
    def message_handler(msg: bytes):
        print("📨 Received:", msg.decode('utf-8'))

    def status_handler(status: str):
        print(f"📡 Status: {status}")

    client.on_data_message = message_handler
    client.on_connection_status = status_handler

    # Generate keys and register
    private_key_b64, auth_secret_b64 = client.create_new_keys()
    fcm_token, gcm_token, android_id, security_token = client.register()

    print(f"✅ Registered! Android ID: {android_id}")

    # Subscribe to topic
    result = client.subscribe_to_topic("news")
    print(f"📡 Subscribed to: {result['topic']}")

    # Start listening
    client.start_listening()

    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.close()

if __name__ == "__main__":
    main()
```

### Running the Example

```bash
# Create your credentials file first
echo '{
  "project_id": "shopee-ad86f",
  "api_key": "AIzaSyAPkv8NbRwcRTkNQK-xXJ1Za_IN2sPIYCg",
  "app_id": "1:808332928752:android:24633eecd863d5bd828435"
}' > config.json

# Run the example
python basic_example.py
```

---

## 🌟 Features

### 🔐 Security & Encryption
- **Elliptic Curve Cryptography** - P-256 curve for key exchange
- **ECDH Key Agreement** - Secure shared secret generation
- **AES-GCM Encryption** - Message payload encryption
- **Authentication** - Firebase authentication tokens
- **Key Persistence** - Secure credential storage

### 📡 Protocol Features
- **FCM Protocol Implementation** - Complete low-level protocol
- **GCM Registration** - Google Cloud Messaging registration
- **Topic Management** - Dynamic topic subscription
- **Heartbeat Support** - Connection keep-alive
- **Auto-Reconnection** - Automatic connection recovery
- **Message Types** - Data, notification, and raw messages

### 🏗️ Architecture
- **Multi-Project Support** - Connect to multiple Firebase projects
- **Async Callbacks** - Non-blocking message processing
- **Thread-Safe** - Safe for concurrent use
- **Memory Efficient** - Optimized for long-running processes
- **Cross-Platform** - Works on Windows, macOS, and Linux

---

## 📚 Advanced Usage

### Multi-Project Management

```python
from fcm_receiver import FCMClient
import json
import time

# Multiple Firebase projects configuration
firebase_projects = [
    {
        "api_key": "AIzaSyCCGuy1kzATV1Ju3TRLq3s1vOwI-feQYwg",
        "app_id": "1:1097968069254:android:e6c01d44c6789e69f23f07",
        "project_id": "testingmachine-agus",
        "topics": ["news", "updates"],
    },
    {
        "api_key": "AIzaSyBTzZdhl5TzFlggYx6bNEn-TxYVp5MUKNQ",
        "app_id": "1:468081959538:android:9c4b4135f08773f50498eb",
        "project_id": "belajarfirebase-395f8",
        "topics": ["news"],
    },
    {
        "api_key": "AIzaSyC23PJFvsGcPV-mxk-OOc0d3o9uCuiVZX4",
        "app_id": "1:640680687175:android:8df68c2a7a979c1c",
        "project_id": "authexample-ffdf9",
        "topics": ["announcements"],
    }
]

clients = []

def setup_client(config):
    """Setup FCM client for a single project"""
    client = FCMClient()
    client.api_key = config["api_key"]
    client.app_id = config["app_id"]
    client.project_id = config["project_id"]
    client.heartbeat_interval_sec = 60

    # Setup project-specific callbacks
    def on_data(msg: bytes, project_id: str):
        print(f"[{project_id}] 📨 Message:", msg.decode('utf-8'))

    def on_raw(obj, project_id: str):
        print(f"[{project_id}] 📦 Raw:", json.dumps(obj, indent=2))

    def on_notif(obj: dict, project_id: str):
        print(f"[{project_id}] 🔔 Notification:", json.dumps(obj, ensure_ascii=False))

    def on_status(status: str, project_id: str):
        print(f"[{project_id}] 📡 Status: {status}")

    def on_tag(tag: int, name: str, project_id: str):
        print(f"[{project_id}] 🏷️ Tag {tag} ({name})")

    # Bind callbacks
    client.on_data_message = lambda msg: on_data(msg, config["project_id"])
    client.on_raw_message = lambda obj: on_raw(obj, config["project_id"])
    client.on_notification_message = lambda obj: on_notif(obj, config["project_id"])
    client.on_connection_status = lambda status: on_status(status, config["project_id"])
    client.on_tag = lambda tag, name: on_tag(tag, name, config["project_id"])

    return client

def setup_credentials(client, config):
    """Setup or load credentials for a project"""
    cred_path = f"./credentials.{config['project_id']}.json"

    if os.path.exists(cred_path):
        # Load existing credentials
        with open(cred_path, 'r') as f:
            cred = json.load(f)

        client.gcm_token = cred.get("gcmToken", "")
        client.fcm_token = cred.get("fcmToken", "")
        client.android_id = int(cred["androidId"])
        client.security_token = int(cred["securityToken"])
        client.load_keys(cred["privateKeyBase64"], cred["authSecretBase64"])

        print(f"✅ Loaded credentials for {config['project_id']}")
    else:
        # Create new credentials
        priv_b64, auth_b64 = client.create_new_keys()
        client.load_keys(priv_b64, auth_b64)
        fcm_token, gcm_token, android_id, security_token = client.register()

        cred = {
            "apiKey": config["api_key"],
            "appId": config["app_id"],
            "projectId": config["project_id"],
            "fcmToken": fcm_token,
            "gcmToken": gcm_token,
            "androidId": android_id,
            "securityToken": security_token,
            "privateKeyBase64": priv_b64,
            "authSecretBase64": auth_b64,
            "subscribedTopics": [],
        }

        with open(cred_path, 'w') as f:
            json.dump(cred, f, indent=2)

        print(f"✅ Created new credentials for {config['project_id']}")

    return cred

def main():
    """Multi-project FCM receiver"""
    global clients

    for config in firebase_projects:
        # Setup client
        client = setup_client(config)

        # Setup credentials
        cred = setup_credentials(client, config)

        # Subscribe to topics
        topics = config.get("topics", [])
        subscribed_topics = set(cred.get("subscribedTopics", []))

        for topic in topics:
            try:
                if topic not in subscribed_topics:
                    result = client.subscribe_to_topic(topic)
                    subscribed_topics.add(result["topic"])
                    print(f"[{config['project_id']}] Subscribed to {topic}")
            except Exception as e:
                print(f"[{config['project_id']}] Failed to subscribe to {topic}: {e}")

        # Update credentials with new topics
        cred["subscribedTopics"] = list(subscribed_topics)
        with open(f"./credentials.{config['project_id']}.json", 'w') as f:
            json.dump(cred, f, indent=2)

        # Start listening
        client.start_listening()
        clients.append(client)

    print(f"🚀 Started {len(clients)} FCM clients")

    try:
        while True:
            time.sleep(3600)  # Keep alive
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        for client in clients:
            client.close()

if __name__ == "__main__":
    main()
```

### Production-Ready Implementation

```python
import logging
from fcm_receiver import FCMClient
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class FirebaseConfig:
    """Configuration for Firebase project"""
    project_id: str
    api_key: str
    app_id: str
    topics: List[str]
    callback_url: Optional[str] = None

class ProductionFCMManager:
    """Production-ready FCM manager with monitoring and error handling"""

    def __init__(self):
        self.clients: Dict[str, FCMClient] = {}
        self.configs: Dict[str, FirebaseConfig] = {}
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Setup comprehensive logging"""
        logger = logging.getLogger("FCMManager")
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def add_project(self, config: FirebaseConfig):
        """Add a Firebase project to monitor"""
        self.configs[config.project_id] = config

        client = FCMClient()
        client.project_id = config.project_id
        client.api_key = config.api_key
        client.app_id = config.app_id
        client.heartbeat_interval_sec = 60

        # Setup production callbacks
        self._setup_production_callbacks(client, config)

        # Setup credentials
        self._setup_credentials(client, config.project_id)

        # Subscribe to topics
        for topic in config.topics:
            try:
                client.subscribe_to_topic(topic)
                self.logger.info(f"Subscribed to {topic} for {config.project_id}")
            except Exception as e:
                self.logger.error(f"Failed to subscribe to {topic}: {e}")

        # Start listening
        client.start_listening()
        self.clients[config.project_id] = client

        self.logger.info(f"Started FCM client for {config.project_id}")

    def _setup_production_callbacks(self, client: FCMClient, config: FirebaseConfig):
        """Setup production-grade callbacks with monitoring"""

        def on_message(msg: bytes):
            try:
                data = msg.decode('utf-8')
                self.logger.info(f"Message from {config.project_id}: {data[:100]}...")

                # Here you could:
                # - Forward to webhook
                # - Store in database
                # - Process business logic
                # - Trigger alerts

                if config.callback_url:
                    self._forward_to_webhook(config.callback_url, data)

            except Exception as e:
                self.logger.error(f"Error processing message: {e}")

        def on_status(status: str):
            status_map = {
                "connecting": "INFO",
                "connected": "INFO",
                "disconnected": "WARNING",
                "error": "ERROR"
            }
            level = status_map.get(status, "INFO")
            getattr(self.logger, level.lower())(f"Status {config.project_id}: {status}")

        def on_error(error: Exception):
            self.logger.error(f"Error in {config.project_id}: {error}")
            # Here you could implement retry logic or alerts

        client.on_data_message = on_message
        client.on_connection_status = on_status
        client.on_error = on_error

    def _setup_credentials(self, client: FCMClient, project_id: str):
        """Setup credentials with proper error handling"""
        try:
            cred_path = f"/etc/fcm/credentials.{project_id}.json"

            if os.path.exists(cred_path):
                with open(cred_path, 'r') as f:
                    cred = json.load(f)

                client.load_credentials(cred)
                self.logger.info(f"Loaded credentials for {project_id}")
            else:
                client.create_new_keys()
                client.register()
                self._save_credentials(client, project_id)
                self.logger.info(f"Created new credentials for {project_id}")

        except Exception as e:
            self.logger.error(f"Failed to setup credentials for {project_id}: {e}")
            raise

    def _save_credentials(self, client: FCMClient, project_id: str):
        """Save credentials securely"""
        cred_path = f"/etc/fcm/credentials.{project_id}.json"

        os.makedirs(os.path.dirname(cred_path), exist_ok=True)

        cred = {
            "project_id": project_id,
            "android_id": client.android_id,
            "security_token": client.security_token,
            "gcm_token": client.gcm_token,
            "fcm_token": client.fcm_token,
            "private_key": client.encode_private_key(),
            "auth_secret": client.auth_secret_b64,
        }

        with open(cred_path, 'w') as f:
            json.dump(cred, f)

        # Set secure permissions
        os.chmod(cred_path, 0o600)

    def shutdown(self):
        """Graceful shutdown"""
        self.logger.info("Shutting down FCM clients...")
        for client in self.clients.values():
            client.close()
        self.logger.info("All FCM clients stopped")

# Usage Example
if __name__ == "__main__":
    manager = ProductionFCMManager()

    # Add multiple projects
    configs = [
        FirebaseConfig(
            project_id="shopee-ad86f",
            api_key="AIzaSyAPkv8NbRwcRTkNQK-xXJ1Za_IN2sPIYCg",
            app_id="1:808332928752:android:24633eecd863d5bd828435",
            topics=["orders", "promotions", "updates"],
            callback_url="https://your-api.com/webhook/fcm"
        ),
        # Add more projects as needed
    ]

    for config in configs:
        manager.add_project(config)

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        manager.shutdown()
```

---

## 🔧 Configuration

### Firebase Project Setup

1. **Create Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create new project or use existing one
   - Add Android app (even if you're using it for backend)

2. **Get Credentials**
   - Project Settings → General → Project ID
   - Project Settings → Cloud Messaging → Web API Key
   - Your App → App ID (from GoogleServices.json)

3. **Environment Variables**

```bash
# For production
export FCM_PROJECT_ID="your-project-id"
export FCM_API_KEY="your-api-key"
export FCM_APP_ID="your-app-id"
```

### Configuration File Format

```json
{
  "firebase_projects": [
    {
      "project_id": "shopee-ad86f",
      "api_key": "AIzaSyAPkv8NbRwcRTkNQK-xXJ1Za_IN2sPIYCg",
      "app_id": "1:808332928752:android:24633eecd863d5bd828435",
      "topics": ["news", "updates", "promotions"],
      "callbacks": {
        "on_data": "your_module.handle_data",
        "on_notification": "your_module.handle_notification"
      }
    }
  ]
}
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=fcm_receiver --cov-report=html

# Run specific test
pytest tests/test_register.py -v
```

### Test Registration

```bash
# Test FCM registration with your credentials
python tests/test_register_simple.py
```

---

## 📖 API Reference

### FCMClient Class

#### Core Methods

```python
# Initialize client
client = FCMClient()

# Configuration
client.project_id = "your-project-id"
client.api_key = "your-api-key"
client.app_id = "your-app-id"

# Key Management
private_key_b64, auth_secret_b64 = client.create_new_keys()
client.load_keys(private_key_b64, auth_secret_b64)

# Registration
fcm_token, gcm_token, android_id, security_token = client.register()

# Topic Management
result = client.subscribe_to_topic("news")
result = client.unsubscribe_from_topic("news")

# Connection
client.start_listening()
client.close()
```

#### Callbacks

```python
# Message callbacks
client.on_data_message = lambda msg: print(f"Data: {msg}")
client.on_notification_message = lambda notif: print(f"Notif: {notif}")
client.on_raw_message = lambda raw: print(f"Raw: {raw}")

# Status callbacks
client.on_connection_status = lambda status: print(f"Status: {status}")
client.on_tag = lambda tag, name: print(f"Tag: {tag} ({name})")
client.on_error = lambda error: print(f"Error: {error}")
```

#### Configuration Options

```python
client.heartbeat_interval_sec = 60  # Heartbeat interval
client.require_gcm_token = True     # Require GCM token
client.timeout = 30                 # Connection timeout
```

---

## 🐛 Troubleshooting

### Common Issues

#### Registration Failed
```python
# Check Firebase credentials
assert client.project_id and client.api_key and client.app_id

# Check network connectivity
import requests
requests.get("https://fcm.googleapis.com", timeout=10)
```

#### Connection Issues
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check firewall settings
# Ensure outbound connections to:
# - fcm.googleapis.com:5228
# - android.clients.google.com:5228
```

#### Key Generation Failed
```python
# Check cryptography library installation
from cryptography.hazmat.primitives.asymmetric import ec

# Test key creation
private_key = ec.generate_private_key(ec.SECP256R1())
```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable verbose logging
client = FCMClient()
client.debug = True
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/agusibrahim/pyfcm-receiver.git
cd pyfcm-receiver

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run linting
black .
flake8 .
mypy .
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging) for the messaging service
- [cryptography](https://cryptography.io/) for encryption primitives
- [Protocol Buffers](https://developers.google.com/protocol-buffers) for message serialization

---

<div align="center">
  <p>Made with ❤️ by the Agus Ibrahim</p>
  <p>⭐ If this project helped you, consider giving it a star!</p>
</div>
