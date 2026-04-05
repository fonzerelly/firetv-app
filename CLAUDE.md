# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Goal

A Docker-based FireTV remote control web app. A shell script starts a container with `adb` installed, connects to a FireTV Stick via its IP, and serves a web UI on port 5555 where clicking buttons sends `adb shell input keyevent` commands.

## Running the App

```bash
FIRETV_IP=192.168.x.x ./start.sh
```

The web UI is reachable at `http://localhost:5555`.

## Architecture

- `start.sh` — entry point: builds/runs the Docker container, passes `FIRETV_IP` as env var
- `Dockerfile` — installs `adb` (Android Debug Bridge) and the web server
- `entrypoint.sh` — runs inside the container: calls `adb connect $FIRETV_IP`, then starts the web server
- `web/index.html` — static HTML page with FireTV remote buttons
- `web/server` — minimal HTTP server that handles button POST requests and executes `adb shell input keyevent <KEYCODE>`

## FireTV Keycodes

| Button | Keycode |
|---|---|
| Hoch | 19 |
| Runter | 20 |
| Links | 21 |
| Rechts | 22 |
| Auswahl | 23 |
| Zurück | 4 |
| Home | 3 |
| Menü | 82 |
| Zurück-Spulen | 89 |
| Vor-Spulen | 90 |
| Play/Pause | 85 |
| Mute | 164 |
| Lauter | 24 |
| Leiser | 25 |
| Fernseher (TV Input) | 178 |
| Prime Video | — (app launch via adb) |
| Netflix | — (app launch via adb) |
| Amazon Music | — (app launch via adb) |
| Disney+ | — (app launch via adb) |

App launches use `adb shell am start -n <package>/<activity>` rather than keycodes.
