<div align="center">
  <h1>🔥 FCM Receiver</h1>
  <p>Powerful Python library for receiving Firebase Cloud Messages with end-to-end encryption support</p>

  [![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

  <p>
    <a href="#-what-is-fcm-receiver">Overview</a> •
    <a href="#-installation">Installation</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-callback-reference">Callback Reference</a> •
    <a href="#-configuration-notes">Configuration</a>
  </p>
</div>

---

## 🚀 What is FCM Receiver?

FCM Receiver is a Python library that implements the low-level Firebase Cloud Messaging (FCM) protocol so you can receive push messages without depending on the official SDKs. It supports encrypted payloads, automatic reconnection, and credential persistence, making it a good fit for headless services or backend tooling.

### ✨ Key Highlights

- 🔐 End-to-end encryption with elliptic curve keys
- 📱 Connect to one or many Firebase projects simultaneously
- 🔄 Automatic reconnect with exponential backoff
- 💾 Credential storage helpers for repeatable startups
- 🧩 Lightweight Python API without external Firebase dependencies

---

## 📦 Installation

Install from PyPI:

```bash
pip install fcm-receiver
```

Or install from source for local development:

```bash
git clone https://github.com/agusibrahim/pyfcm-receiver.git
cd pyfcm-receiver
pip install -e .
```

---

## 🎯 Quick Start

### Basic Usage – Single Project

```python
from fcm_receiver import FCMClient
import time

client = FCMClient()
client.project_id = "demo-project-123"
client.api_key = "demo-api-key"
client.app_id = "1:1234567890:web:demo-app"

# Every callback receives the data plus the client identifier.
def handle_data(payload: bytes, client_id: str) -> None:
    print(f"📨 [{client_id}]", payload.decode("utf-8"))

def handle_status(status: str, client_id: str) -> None:
    print(f"📡 [{client_id}] {status}")

client.on_data_message = handle_data
client.on_connection_status = handle_status

# Setup cryptographic keys and register the device with FCM.
client.create_new_keys()
client.register()

client.start_listening()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    client.close()
```

### Basic Usage – Multiple Projects

```python
from fcm_receiver import MultiFCMClient
import time

projects = [
    {
        "id": "marketing",
        "project_id": "demo-project-a",
        "api_key": "demo-api-key-a",
        "app_id": "1:100000000000:android:demoapp-a",
    },
    {
        "id": "logistics",
        "project_id": "demo-project-b",
        "api_key": "demo-api-key-b",
        "app_id": "1:200000000000:android:demoapp-b",
    },
]

multi = MultiFCMClient(projects=projects, credential_dir="./credentials")

def handle_notification(message: dict, client_id: str) -> None:
    title = message.get("payload", {}).get("title", "(no title)")
    print(f"🔔 [{client_id}] {title}")

def handle_data(data: bytes, client_id: str) -> None:
    print(f"📨 [{client_id}] {data.decode('utf-8')}")

def handle_status(status: str, client_id: str) -> None:
    print(f"📡 [{client_id}] {status}")

multi.on_notification_message = handle_notification
multi.on_data_message = handle_data
multi.on_connection_status = handle_status

print("🚀 Starting MultiFCMClient...")
multi.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    multi.close()
```

> **Note:** Each project configuration must include a unique `id`. That identifier is returned as the second argument on every callback so you can distinguish which project emitted the event, even if multiple Firebase projects share the same `project_id`.

---

## 🔁 Callback Reference

The library sends an identifier alongside every callback so you always know which client produced the event.

### FCMClient

- `on_notification_message(message: dict, client_id: str)` – decrypted notification payloads
- `on_data_message(data: bytes, client_id: str)` – raw decrypted bytes
- `on_raw_message(message_obj: object, client_id: str)` – low-level protocol objects
- `on_connection_status(status: str, client_id: str)` – lifecycle updates (`connecting`, `connected`, etc.)
- `on_tag(tag: int, name: str, client_id: str)` – protocol tags emitted by the socket

### MultiFCMClient

- Accepts the same callbacks as `FCMClient`
- Proxies events from all child clients while preserving the `id` you define in each project entry

---

## ⚙️ Configuration Notes

- Every project dictionary passed to `MultiFCMClient` must include `id`, `project_id`, `api_key`, and `app_id`.
- Credentials are cached under `credential_dir` so subsequent runs can reconnect quickly. Remove the files in that directory if you need to force a new registration.
- Topic subscriptions are optional; call `subscribe_to_topic()` on the underlying `FCMClient` instances if needed.
- Network access and valid Firebase credentials are still required at runtime even when using dummy values in these examples.

---

## 📄 License

This project is released under the [MIT License](LICENSE).
