#!/usr/bin/env bash
# Setup aman (Linux/macOS): environment terisolasi .venv di folder kerja.
cd "$(dirname "$0")"
PY=$(command -v python3 || command -v python)
[ -z "$PY" ] && { echo "Python tidak ditemukan"; exit 1; }
"$PY" tools/setup_env.py "$@"
