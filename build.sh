#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Baue Docker-Image firetv-remote ..."
docker build --no-cache -t firetv-remote "$SCRIPT_DIR"
echo "Fertig."
