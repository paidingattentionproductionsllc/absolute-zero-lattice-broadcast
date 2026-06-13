#!/usr/bin/env bash
set -euo pipefail

PY=python3
VENV_DIR=.venv

echo "Creating virtual environment in ${VENV_DIR}..."
$PY -m venv ${VENV_DIR}
echo "Activating venv and upgrading pip..."
source ${VENV_DIR}/bin/activate
pip install --upgrade pip
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi
if [ -f requirements-dev.txt ]; then
  pip install -r requirements-dev.txt
fi

echo "Setup complete. Activate with: source ${VENV_DIR}/bin/activate"