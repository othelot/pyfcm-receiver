from __future__ import annotations

import select
import socket
import ssl
import threading
import time
from typing import Callable, Optional, Tuple

from .proto_manual import uvarint
from .unmarshal_manual import (
    unmarshal_data_message_stanza,
    unmarshal_login_response,
)


# Constants aligned with go-fcm-receiver/consts.go
KMCS_VERSION = 41

K_HEARTBEAT_PING = 0
K_HEARTBEAT_ACK = 1
K_LOGIN_REQUEST = 2
K_LOGIN_RESPONSE = 3
K_CLOSE = 4
K_MESSAGE_STANZA = 5
K_PRESENCE_STANZA = 6
K_IQ_STANZA = 7
K_DATA_MESSAGE_STANZA = 8
K_STREAM_ERROR_STANZA = 10

TAG_NAMES = {
    K_HEARTBEAT_PING: "HEARTBEAT_PING",
    K_HEARTBEAT_ACK: "HEARTBEAT_ACK",
    K_LOGIN_REQUEST: "LOGIN_REQUEST",
    K_LOGIN_RESPONSE: "LOGIN_RESPONSE",
    K_CLOSE: "CLOSE",
    K_MESSAGE_STANZA: "MESSAGE_STANZA",
    K_PRESENCE_STANZA: "PRESENCE_STANZA",
    K_IQ_STANZA: "IQ_STANZA",
    K_DATA_MESSAGE_STANZA: "DATA_MESSAGE_STANZA",
    K_STREAM_ERROR_STANZA: "STREAM_ERROR_STANZA",
}

def get_tag_name(tag: int) -> str:
    return TAG_NAMES.get(tag, "UNKNOWN")


class FCMSocketHandler:
    def __init__(self) -> None:
        self.sock: Optional[ssl.SSLSocket] = None
        self.is_alive: bool = False
        self.heartbeat_interval_sec: int = 600
        self.on_message: Optional[Callable[[int, object], None]] = None
        self.on_close: Optional[Callable[[Optional[Exception]], None]] = None
        self.on_tag: Optional[Callable[[int, str], None]] = None
        self._reader_thread: Optional[threading.Thread] = None
        self._hb_thread: Optional[threading.Thread] = None
        self._watchdog_thread: Optional[threading.Thread] = None
        self._stop = threading.Event()

        # parser state
        self._state = 0  # 0: VERSION_TAG_SIZE, 1: TAG_SIZE, 2: SIZE, 3: BYTES
        self._buf = bytearray()
        self._size_pkt_so_far = 0
        self._message_tag = 0
        self._message_size = 0
        self._handshake_complete = False
        self._last_activity = time.time()

    def init(self) -> None:
        self._state = 0
        self._buf.clear()
        self._size_pkt_so_far = 0
        self._message_tag = 0
        self._message_size = 0
        self._handshake_complete = False

    def start(self) -> None:
        self._stop.clear()
        self._reader_thread = threading.Thread(target=self._read_loop, daemon=True)
        self._reader_thread.start()
        # Heartbeat sender
        self._hb_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._hb_thread.start()
        # Watchdog to detect stale connections
        self._watchdog_thread = threading.Thread(target=self._watchdog_loop, daemon=True)
        self._watchdog_thread.start()

    def close(self, err: Optional[Exception] = None) -> None:
        self._stop.set()
        try:
            if self.sock:
                self.sock.close()
        finally:
            self.is_alive = False
            self.sock = None
            self.init()
            cb = self.on_close
            if cb:
                try:
                    cb(err)
                except Exception:
                    pass

    def send(self, data: bytes) -> None:
        assert self.sock is not None
        try:
            self.sock.sendall(data)
            self._last_activity = time.time()
        except Exception as e:
            print(f"[fcm_socket] send failed: {e}")
            self.close(e)

    def send_heartbeat_ping(self) -> None:
        # tag + zero-length
        self.send(bytes([K_HEARTBEAT_PING, 0]))

    def _read_loop(self) -> None:
        print("[fcm_socket] read loop started")
        while not self._stop.is_set():
            sock = self.sock
            if sock is None:
                return
            try:
                r, _, _ = select.select([sock], [], [], 1.0)
            except Exception as e:
                # Socket likely closed; exit gracefully
                self.close()
                return
            if not r:
                continue
            try:
                chunk = sock.recv(32 * 1024)
            except Exception:
                self.close()
                return
            if not chunk:
                print("[fcm_socket] socket closed by peer")
                self.close()
                return
            self._buf.extend(chunk)
            self._last_activity = time.time()
            self._on_data()

    def _on_data(self) -> None:
        while True:
            if self._state == 0:  # VERSION_TAG_SIZE
                if len(self._buf) < 1:
                    return
                version = self._buf[0]
                del self._buf[:1]
                # accept version 41 or 38
                if version not in (KMCS_VERSION, 38):
                    self.close()
                    return
                self._state = 1
            if self._state == 1:  # TAG_SIZE
                if len(self._buf) < 1:
                    return
                self._message_tag = self._buf[0]
                del self._buf[:1]
                # Debug tags and optional callback
                name = get_tag_name(self._message_tag)
                print(f"[fcm_socket] tag={self._message_tag}")
                if self.on_tag:
                    try:
                        self.on_tag(self._message_tag, name)
                    except Exception:
                        pass
                self._state = 2
                self._size_pkt_so_far = 0
            if self._state == 2:  # SIZE
                size, n = uvarint(self._buf, 0)
                if n <= 0:
                    return
                self._message_size = size
                del self._buf[:n]
                self._state = 3
            if self._state == 3:  # BYTES
                if len(self._buf) < self._message_size:
                    return
                payload = bytes(self._buf[: self._message_size])
                del self._buf[: self._message_size]
                self._dispatch(self._message_tag, payload)
                self._state = 1  # next messages are tag+size+payload

    def _dispatch(self, tag: int, payload: bytes) -> None:
        if self.on_message is None:
            return
        if tag == K_HEARTBEAT_PING:
            # Respond ping immediately
            try:
                self.send_heartbeat_ping()
            except Exception:
                self.close()
                return
            self.on_message(tag, None)
            return
        if tag == K_CLOSE:
            # Server requested close
            self.on_message(tag, None)
            self.close()
            return
        if tag == K_LOGIN_RESPONSE:
            obj = unmarshal_login_response(payload)
            print("[fcm_socket] login response received")
            self.on_message(tag, obj)
            return
        if tag == K_DATA_MESSAGE_STANZA:
            obj = unmarshal_data_message_stanza(payload)
            print("[fcm_socket] data message received (persistentId=", getattr(obj, 'persistent_id', None), ")")
            self.on_message(tag, obj)
            return
        # Other tags can be parsed/ignored similarly
        self.on_message(tag, payload)

    def _heartbeat_loop(self) -> None:
        if self.heartbeat_interval_sec <= 0:
            self.heartbeat_interval_sec = 600
        while not self._stop.is_set():
            time.sleep(self.heartbeat_interval_sec)
            if self._stop.is_set():
                break
            try:
                self.send_heartbeat_ping()
            except Exception as e:
                print(f"[fcm_socket] heartbeat send failed: {e}")
                return

    def _watchdog_loop(self) -> None:
        # If no activity for 2x heartbeat interval, force close to trigger reconnect
        interval = max(self.heartbeat_interval_sec, 60)
        timeout = interval * 2
        while not self._stop.is_set():
            time.sleep(5)
            if self._stop.is_set():
                break
            if time.time() - self._last_activity > timeout:
                print("[fcm_socket] watchdog: no activity, closing to reconnect")
                self.close()
                return


def dial_fcm(address: str = "mtalk.google.com", port: int = 5228) -> ssl.SSLSocket:
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.load_default_certs()
    raw = socket.create_connection((address, port))
    try:
        raw.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    except Exception:
        pass
    tls = ctx.wrap_socket(raw, server_hostname=address)
    return tls
