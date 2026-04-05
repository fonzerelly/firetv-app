#!/usr/bin/env bash
set -euo pipefail

if [ -z "${FIRETV_IP:-}" ]; then
  echo "Fehler: Umgebungsvariable FIRETV_IP ist nicht gesetzt."
  echo "Aufruf: FIRETV_IP=192.168.x.x FIRETV_AUTH=geheim ./start.sh"
  exit 1
fi

if [ -z "${FIRETV_AUTH:-}" ]; then
  echo "Fehler: Umgebungsvariable FIRETV_AUTH ist nicht gesetzt."
  echo "Aufruf: FIRETV_IP=192.168.x.x FIRETV_AUTH=geheim ./start.sh"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Baue Docker-Image..."
docker build -t firetv-remote "$SCRIPT_DIR"

echo "Öffne Port 5555 in ufw..."
sudo ufw allow 5555

echo "Starte Container (WebUI: http://localhost:5555)..."
docker run --restart unless-stopped --detach \
  -e FIRETV_IP="$FIRETV_IP" \
  ${FIRETV_AUTH:+-e FIRETV_AUTH="$FIRETV_AUTH"} \
  -p 5555:5555 \
  firetv-remote
