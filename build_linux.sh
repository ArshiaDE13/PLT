#!/usr/bin/env bash
# ============================================================
#  Build a single standalone "PythonTutor" binary for Linux.
#  The binary runs on machines that do NOT have Python installed.
#
#  Run this once on any Linux machine that HAS Python 3.8+:
#      bash build_linux.sh
#
#  The result is written to:  dist/PythonTutor
# ============================================================
set -e
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"

echo "[1/4] Creating a clean build environment (project-local venv)..."
"$PY" -m venv .build-venv
# shellcheck disable=SC1091
source .build-venv/bin/activate

echo "[2/4] Installing PyInstaller (build tool only)..."
pip install --quiet -r requirements.txt

echo "[3/4] Building PythonTutor ..."
python -m PyInstaller --noconfirm --clean python_tutor.spec

echo "[4/4] Done!"
echo
echo "    Your standalone program is here:"
echo "        $(pwd)/dist/PythonTutor"
echo
echo "    Copy that single file to any Linux machine (Python not needed)"
echo "    and run it. The app starts a local server and opens the browser."
