#!/usr/bin/env bash
set -euo pipefail

docker stop $(docker ps -q --filter ancestor=firetv-remote)
