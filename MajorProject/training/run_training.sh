#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Prefer Anaconda Python 3.12 (PyTorch is not available on Python 3.13 yet).
if command -v /opt/anaconda3/bin/python3.12 >/dev/null 2>&1; then
  PYTHON_BIN="/opt/anaconda3/bin/python3.12"
elif command -v python3.12 >/dev/null 2>&1; then
  PYTHON_BIN="python3.12"
else
  PYTHON_BIN="python3"
fi

echo "Using Python: $PYTHON_BIN"
echo "Project: $PROJECT_ROOT"
echo ""
echo "Tip: progress bars update live in this terminal."
echo ""

export TOKENIZERS_PARALLELISM=false
export PYTHONUNBUFFERED=1

"$PYTHON_BIN" -u training/train_prompt_optimizer.py "$@"
