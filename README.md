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

## 🚀 Multi-Project Management with MultiFCMClient

`MultiFCMClient` is a powerful wrapper class that simplifies managing multiple Firebase projects simultaneously. It handles credential management, thread pooling, and callback routing automatically.

### ✨ MultiFCMClient Features

- 🎯 **Multi-Project Support** - Manage multiple Firebase projects in one instance
- 🔧 **Automatic Credential Management** - Load/save credentials per project
- 🧵 **Thread Pool Optimization** - Efficient concurrent connection handling
- 📊 **Centralized Callbacks** - Single callback handler for all projects
- 💾 **Persistent Storage** - Automatic credential persistence
- 🔄 **Auto-Reconnection** - Per-project reconnection with backoff
- 🏷️ **Project Identification** - All callbacks include project_id

### 🚀 Basic MultiFCMClient Usage

```python
from fcm_receiver import MultiFCMClient
import time

# Define multiple Firebase projects
projects = [
    {
        "project_id": "shopee-ad86f",
        "api_key": "AIzaSyAPkv8NbRwcRTkNQK-xXJ1Za_IN2sPIYCg",
        "app_id": "1:808332928752:android:24633eecd863d5bd828435",
        "topics": ["orders", "promotions"]
    },
    {
        "project_id": "belajarfirebase-395f8", 
        "api_key": "AIzaSyBTzZdhl5TzFlggYx6bNEn-TxYVp5MUKNQ",
        "app_id": "1:468081959538:android:9c4b4135f08773f50498eb",
        "topics": ["news", "updates"]
    },
    {
        "project_id": "authexample-ffdf9",
        "api_key": "AIzaSyC23PJFvsGcPV-mxk-OOc0d3o9uCuiVZX4", 
        "app_id": "1:640680687175:android:8df68c2a7a979c1c",
        "topics": ["announcements"]
    }
]

# Create MultiFCMClient
multi_client = MultiFCMClient(
    projects=projects,
    credential_dir="./credentials",
    heartbeat_interval_sec=60
)

# Set up centralized callbacks
def on_notification(message: dict, project_id: str):
    print(f"🔔 [{project_id}] {message.get('payload', {}).get('title', 'No title')}")

def on_data(data: bytes, project_id: str):
    print(f"📨 [{project_id}] Raw data: {len(data)} bytes")

def on_status(status: str, project_id: str):
    print(f"📡 [{project_id}] Status: {status}")

def on_tag(tag: int, name: str, project_id: str):
    print(f"🏷️ [{project_id}] Tag: {tag} ({name})")

# Assign callbacks
multi_client.on_notification_message = on_notification
multi_client.on_data_message = on_data
multi_client.on_connection_status = on_status
multi_client.on_tag = on_tag

# Start all clients
print("🚀 Starting multi-project FCM receiver...")
multi_client.start()

# Keep running
try:
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    print("\n🛑 Shutting down...")
    multi_client.close()
```

### 🎯 Advanced MultiFCMClient Configuration

```python
from fcm_receiver import MultiFCMClient
import json
import logging
from pathlib import Path

class AdvancedMultiFCMManager:
    """Advanced multi-project FCM manager with enhanced features"""
    
    def __init__(self, config_file: str = "fcm_config.json"):
        self.config_file = config_file
        self.multi_client = None
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        logger = logging.getLogger("MultiFCMManager")
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def load_config(self) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Config file {self.config_file} not found")
            return {}
    
    def setup_message_handlers(self):
        """Setup comprehensive message handlers"""
        
        def handle_notification(message: dict, project_id: str):
            """Handle notification messages with project-specific logic"""
            payload = message.get('payload', {})
            title = payload.get('title', 'No Title')
            body = payload.get('body', '')
            
            self.logger.info(f"🔔 [{project_id}] {title}")
            
            # Project-specific handling
            if project_id == "shopee-ad86f":
                self._handle_shopee_notification(payload)
            elif project_id == "belajarfirebase-395f8":
                self._handle_news_notification(payload)
            elif project_id == "authexample-ffdf9":
                self._handle_auth_notification(payload)
        
        def handle_data(data: bytes, project_id: str):
            """Handle raw data messages"""
            try:
                text = data.decode('utf-8')
                self.logger.info(f"📨 [{project_id}] Data: {text[:100]}...")
                
                # Process business logic
                self._process_business_data(project_id, data)
                
            except UnicodeDecodeError:
                self.logger.warning(f"📦 [{project_id}] Binary data: {len(data)} bytes")
        
        def handle_connection_status(status: str, project_id: str):
            """Handle connection status changes"""
            status_emoji = {
                "connecting": "🔄",
                "connected": "✅", 
                "disconnected": "❌",
                "reconnecting": "🔄",
                "error": "⚠️"
            }
            
            emoji = status_emoji.get(status, "📡")
            self.logger.info(f"{emoji} [{project_id}] {status}")
            
            # Trigger alerts for critical status
            if status == "error":
                self._send_alert(f"FCM connection error for {project_id}")
        
        def handle_protocol_tag(tag: int, name: str, project_id: str):
            """Handle FCM protocol tags"""
            tag_info = {
                0: "HEARTBEAT_PING",
                1: "HEARTBEAT_ACK", 
                2: "LOGIN_REQUEST",
                3: "LOGIN_RESPONSE",
                8: "DATA_MESSAGE_STANZA"
            }
            
            tag_name = tag_info.get(tag, f"UNKNOWN_{tag}")
            self.logger.debug(f"🏷️ [{project_id}] {tag_name} ({tag})")
        
        # Register handlers
        self.multi_client.on_notification_message = handle_notification
        self.multi_client.on_data_message = handle_data
        self.multi_client.on_connection_status = handle_connection_status
        self.multi_client.on_tag = handle_protocol_tag
    
    def _handle_shopee_notification(self, payload: dict):
        """Handle Shopee-specific notifications"""
        if 'order_id' in payload:
            self.logger.info(f"🛒 New order: {payload['order_id']}")
            # Trigger order processing workflow
        elif 'promotion' in payload:
            self.logger.info(f"🎉 Promotion: {payload['promotion']}")
    
    def _handle_news_notification(self, payload: dict):
        """Handle news notifications"""
        category = payload.get('category', 'general')
        self.logger.info(f"📰 [{category}] {payload.get('title', 'News')}")
    
    def _handle_auth_notification(self, payload: dict):
        """Handle authentication notifications"""
        event = payload.get('event', 'auth_event')
        self.logger.info(f"🔐 Auth event: {event}")
    
    def _process_business_data(self, project_id: str, data: bytes):
        """Process business-specific data"""
        # Implement your business logic here
        # Examples:
        # - Store in database
        # - Forward to other services
        # - Trigger workflows
        # - Update caches
        pass
    
    def _send_alert(self, message: str):
        """Send alert (implement your alerting system)"""
        # Examples:
        # - Send email
        # - Post to Slack
        # - Create ticket
        # - Send SMS
        self.logger.warning(f"🚨 ALERT: {message}")
    
    def start(self):
        """Start the multi-client manager"""
        config = self.load_config()
        
        if not config or 'projects' not in config:
            raise ValueError("Invalid configuration file")
        
        # Create MultiFCMClient with advanced settings
        self.multi_client = MultiFCMClient(
            projects=config['projects'],
            credential_dir=config.get('credential_dir', './credentials'),
            heartbeat_interval_sec=config.get('heartbeat_interval', 60),
            max_workers=config.get('max_workers', None)
        )
        
        # Setup message handlers
        self.setup_message_handlers()
        
        # Start all clients
        self.logger.info(f"🚀 Starting {len(config['projects'])} FCM projects...")
        self.multi_client.start()
        
        self.logger.info("✅ Multi-project FCM manager started successfully!")
    
    def stop(self):
        """Stop all clients gracefully"""
        if self.multi_client:
            self.logger.info("🛑 Stopping multi-project FCM manager...")
            self.multi_client.close()
            self.logger.info("✅ All clients stopped")

# Example configuration file (fcm_config.json)
"""
{
  "projects": [
    {
      "project_id": "shopee-ad86f",
      "api_key": "AIzaSyAPkv8NbRwcRTkNQK-xXJ1Za_IN2sPIYCg",
      "app_id": "1:808332928752:android:24633eecd863d5bd828435",
      "topics": ["orders", "promotions", "shipping"]
    },
    {
      "project_id": "belajarfirebase-395f8",
      "api_key": "AIzaSyBTzZdhl5TzFlggYx6bNEn-TxYVp5MUKNQ", 
      "app_id": "1:468081959538:android:9c4b4135f08773f50498eb",
      "topics": ["news", "updates", "alerts"]
    },
    {
      "project_id": "authexample-ffdf9",
      "api_key": "AIzaSyC23PJFvsGcPV-mxk-OOc0d3o9uCuiVZX4",
      "app_id": "1:640680687175:android:8df68c2a7a979c1c", 
      "topics": ["auth", "security", "notifications"]
    }
  ],
  "credential_dir": "./fcm_credentials",
  "heartbeat_interval": 60,
  "max_workers": 10
}
"""

# Usage
if __name__ == "__main__":
    manager = AdvancedMultiFCMManager("fcm_config.json")
    
    try:
        manager.start()
        
        # Keep running
        import time
        while True:
            time.sleep(3600)
            
    except KeyboardInterrupt:
        manager.stop()
```

### 🏗️ Production-Grade MultiFCMClient Setup

```python
from fcm_receiver import MultiFCMClient
import json
import os
import signal
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class ProductionMultiFCMService:
    """Production-ready multi-project FCM service"""
    
    def __init__(self, config_path: str = "/etc/fcm/config.json"):
        self.config_path = config_path
        self.multi_client = None
        self.running = False
        self.stats = {
            'start_time': None,
            'messages_received': 0,
            'connections': 0,
            'errors': 0
        }
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.running = False
        self.stop()
    
    def load_configuration(self) -> Dict[str, Any]:
        """Load and validate configuration"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            # Validate configuration
            required_fields = ['projects', 'credential_dir']
            for field in required_fields:
                if field not in config:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate each project
            for project in config['projects']:
                required_project_fields = ['project_id', 'api_key', 'app_id']
                for field in required_project_fields:
                    if field not in project:
                        raise ValueError(f"Project missing {field}: {project}")
            
            return config
            
        except Exception as e:
            print(f"❌ Configuration error: {e}")
            sys.exit(1)
    
    def setup_logging(self, config: Dict[str, Any]):
        """Setup comprehensive logging"""
        log_dir = Path(config.get('log_dir', '/var/log/fcm'))
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"fcm_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger('ProductionFCM')
    
    def setup_metrics(self, config: Dict[str, Any]):
        """Setup metrics collection (optional)"""
        # This is a placeholder for metrics integration
        # You could integrate with:
        # - Prometheus
        # - StatsD  
        # - Custom metrics system
        
        metrics_enabled = config.get('metrics_enabled', False)
        if metrics_enabled:
            # Setup your metrics collector here
            pass
    
    def setup_health_check(self, config: Dict[str, Any]):
        """Setup health check endpoint"""
        health_port = config.get('health_check_port', 8080)
        
        # This is a placeholder for health check endpoint
        # You could use Flask, FastAPI, or other web frameworks
        
        if health_port:
            print(f"🩺 Health check would be available on port {health_port}")
    
    def start(self):
        """Start the production FCM service"""
        print("🚀 Starting Production Multi-Project FCM Service...")
        
        # Load configuration
        config = self.load_configuration()
        
        # Setup logging
        logger = self.setup_logging(config)
        
        # Setup metrics
        self.setup_metrics(config)
        
        # Setup health check
        self.setup_health_check(config)
        
        # Create MultiFCMClient
        self.multi_client = MultiFCMClient(
            projects=config['projects'],
            credential_dir=config['credential_dir'],
            heartbeat_interval_sec=config.get('heartbeat_interval', 60),
            max_workers=config.get('max_workers')
        )
        
        # Setup message handlers
        self.setup_message_handlers(logger, config)
        
        # Ensure credential directory exists
        Path(config['credential_dir']).mkdir(parents=True, exist_ok=True)
        
        # Start clients
        logger.info(f"Starting {len(config['projects'])} FCM projects...")
        self.multi_client.start()
        
        self.running = True
        self.stats['start_time'] = datetime.now()
        self.stats['connections'] = len(self.multi_client.clients)
        
        logger.info("✅ Production FCM service started successfully!")
        logger.info(f"Managing {len(config['projects'])} projects")
        logger.info(f"Credentials stored in: {config['credential_dir']}")
        
        # Main loop
        try:
            while self.running:
                self._log_stats(logger)
                import time
                time.sleep(60)  # Stats interval
                
        except Exception as e:
            logger.error(f"Service error: {e}")
        finally:
            self.stop()
    
    def setup_message_handlers(self, logger, config: Dict[str, Any]):
        """Setup production message handlers"""
        
        def handle_notification(message: dict, project_id: str):
            """Handle notification messages"""
            self.stats['messages_received'] += 1
            
            payload = message.get('payload', {})
            title = payload.get('title', 'No Title')
            
            logger.info(f"🔔 [{project_id}] {title}")
            
            # Implement your business logic here
            self.process_notification(project_id, payload, config)
        
        def handle_data(data: bytes, project_id: str):
            """Handle data messages"""
            self.stats['messages_received'] += 1
            
            try:
                text = data.decode('utf-8')
                logger.info(f"📨 [{project_id}] Data message: {len(data)} bytes")
                self.process_data(project_id, data, config)
            except UnicodeDecodeError:
                logger.info(f"📦 [{project_id}] Binary data: {len(data)} bytes")
        
        def handle_status(status: str, project_id: str):
            """Handle connection status"""
            logger.info(f"📡 [{project_id}] Status: {status}")
        
        def handle_error(error: Exception, project_id: str):
            """Handle errors"""
            self.stats['errors'] += 1
            logger.error(f"❌ [{project_id}] Error: {error}")
        
        # Register handlers
        self.multi_client.on_notification_message = handle_notification
        self.multi_client.on_data_message = handle_data
        self.multi_client.on_connection_status = handle_status
        # Note: You might need to extend MultiFCMClient to support error callbacks
    
    def process_notification(self, project_id: str, payload: dict, config: Dict[str, Any]):
        """Process notification based on project type"""
        # Implement your business logic here
        # This could forward to webhooks, store in database, etc.
        pass
    
    def process_data(self, project_id: str, data: bytes, config: Dict[str, Any]):
        """Process data messages"""
        # Implement your data processing logic
        pass
    
    def _log_stats(self, logger):
        """Log service statistics"""
        if self.stats['start_time']:
            uptime = datetime.now() - self.stats['start_time']
            logger.info(f"📊 Stats - Uptime: {uptime}, Messages: {self.stats['messages_received']}, Errors: {self.stats['errors']}")
    
    def stop(self):
        """Stop the service gracefully"""
        if self.multi_client:
            print("🛑 Stopping FCM service...")
            self.multi_client.close()
            print("✅ FCM service stopped")

# Systemd service example (/etc/systemd/system/fcm-receiver.service)
"""
[Unit]
Description=FCM Multi-Project Receiver Service
After=network.target

[Service]
Type=simple
User=fcm
Group=fcm
WorkingDirectory=/opt/fcm-receiver
ExecStart=/opt/fcm-receiver/venv/bin/python /opt/fcm-receiver/production_service.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/opt/fcm-receiver

[Install]
WantedBy=multi-user.target
"""

if __name__ == "__main__":
    service = ProductionMultiFCMService()
    service.start()
```

### 🔧 MultiFCMClient API Reference

#### Constructor

```python
MultiFCMClient(
    projects: List[dict],           # List of project configurations
    credential_dir: str = ".",       # Directory for credential storage
    heartbeat_interval_sec: int = 60, # Heartbeat interval
    max_workers: int = None          # Thread pool size (auto-calculated)
)
```

#### Configuration Format

```python
projects = [
    {
        "project_id": "your-project-id",     # Required
        "api_key": "your-api-key",           # Required  
        "app_id": "your-app-id",             # Required
        "topics": ["topic1", "topic2"]        # Optional
    }
]
```

#### Callback Methods

```python
# Notification messages (decrypted JSON)
multi_client.on_notification_message = callable(message: dict, project_id: str)

# Raw data messages (bytes)
multi_client.on_data_message = callable(data: bytes, project_id: str)

# Raw protocol messages
multi_client.on_raw_message = callable(obj: object, project_id: str)

# Connection status changes
multi_client.on_connection_status = callable(status: str, project_id: str)

# Protocol tags
multi_client.on_tag = callable(tag: int, name: str, project_id: str)
```

#### Control Methods

```python
# Start all clients
multi_client.start()

# Stop all clients  
multi_client.close()

# Access individual clients
clients = multi_client.clients  # Dict[str, FCMClient]
```

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
