#!/usr/bin/env python3
"""HTTP-Server für die FireTV-Fernbedienung.

Bedient statische Dateien aus dem web/-Verzeichnis und nimmt POST /keyevent
entgegen, um adb-Befehle auf dem verbundenen FireTV-Stick auszuführen.
"""

import http.server
import json
import os
import subprocess
import sys
from pathlib import Path

PORT = 5555
WEB_DIR = Path(__file__).parent
FIRETV_IP = os.environ["FIRETV_IP"]
FIRETV_AUTH = os.environ["FIRETV_AUTH"]


def log(msg):
    print(msg, flush=True)


def adb_connect():
    """Stellt sicher, dass die adb-Verbindung zum FireTV aktiv ist."""
    result = subprocess.run(["adb", "connect", FIRETV_IP], capture_output=True, text=True)
    log(f"[adb connect] stdout: {result.stdout.strip()}")
    if result.stderr.strip():
        log(f"[adb connect] stderr: {result.stderr.strip()}")


def adb_run(cmd):
    """Führt einen adb-Befehl aus und gibt das CompletedProcess-Objekt zurück."""
    log(f"[adb] Befehl: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout.strip():
        log(f"[adb] stdout: {result.stdout.strip()}")
    if result.stderr.strip():
        log(f"[adb] stderr: {result.stderr.strip()}")
    log(f"[adb] returncode: {result.returncode}")
    return result


# Paketnamen der Streaming-Apps auf dem FireTV
APP_PACKAGES = {
    "prime":   "com.amazon.avod.thirdpartyclient/com.amazon.avod.thirdpartyclient.LauncherActivity",
    "netflix": "com.netflix.ninja/com.netflix.ninja.MainActivity",
    "music":   "com.amazon.mp3/com.amazon.mp3.MainActivity",
    "disney":  "com.disney.disneyplus/com.disney.disneyplus.MainActivity",
}


class RemoteHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def _auth_ok(self):
        return self.headers.get("X-FireTV-Auth") == FIRETV_AUTH

    def do_GET(self):
        if not self._auth_ok():
            self.send_error(403, "Forbidden")
            return
        super().do_GET()

    def do_POST(self):
        log(f"[http] POST {self.path} von {self.client_address[0]}")

        if not self._auth_ok():
            log("[http] Authentifizierung fehlgeschlagen")
            self.send_error(403, "Forbidden")
            return

        if self.path != "/keyevent":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        log(f"[http] Body: {body}")

        if "app" in body:
            package = APP_PACKAGES.get(body["app"])
            if not package:
                log(f"[http] Unbekannte App: {body['app']}")
                self.send_error(400, "Unbekannte App")
                return
            cmd = ["adb", "shell", "am", "start", "-n", package]
        else:
            keycode = int(body["keycode"])
            cmd = ["adb", "shell", "input", "keyevent", str(keycode)]

        adb_connect()
        result = adb_run(cmd)

        self.send_response(200 if result.returncode == 0 else 500)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "ok": result.returncode == 0,
            "stderr": result.stderr.strip(),
        }).encode())

    def log_message(self, format, *args):
        log(f"[http] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    log(f"FireTV-Fernbedienung läuft unter http://localhost:{PORT}")
    log(f"Ziel: {FIRETV_IP}")
    server = http.server.HTTPServer(("0.0.0.0", PORT), RemoteHandler)
    server.serve_forever()
