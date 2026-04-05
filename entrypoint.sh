#!/usr/bin/env bash
set -euo pipefail

# Port anhängen, falls nicht bereits angegeben
[[ "$FIRETV_IP" != *:* ]] && export FIRETV_IP="$FIRETV_IP:5555"

echo "Verbinde mit FireTV unter $FIRETV_IP ..."
adb connect "$FIRETV_IP"
echo "Verbindung hergestellt."

exec python3 web/server.py
