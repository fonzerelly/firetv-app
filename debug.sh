#!/usr/bin/env bash
set -euo pipefail

docker logs $(docker ps -q --filter ancestor=firetv-remote)
