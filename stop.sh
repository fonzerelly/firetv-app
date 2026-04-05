#!/usr/bin/env bash
set -euo pipefail

docker stop $(docker ps -q --filter ancestor=firetv-remote)

echo "Schließe Port 5555 in ufw..."
sudo ufw delete allow 5555
