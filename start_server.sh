#!/bin/bash
echo "======================================================================="
echo "  Smart Project Manager Assistant (SPMA) - Blue Nile University 2026"
echo "  Portable Server & Web Workspace Launcher (Linux / Mac)"
echo "======================================================================="
echo ""
cd "$(dirname "$0")"

# Step 1: Check Python3 installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 could not be found. Please install Python 3.8+."
    exit 1
fi

# Step 2: Create Virtual Environment
if [ ! -d "venv" ]; then
    echo "[1/3] Creating virtual environment (venv)..."
    python3 -m venv venv
fi

# Step 3: Activate venv & install dependencies
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
echo "[2/3] Installing dependencies..."
pip install -r backend/requirements.txt --quiet

# Step 4: Generate Web UI & Start Uvicorn
echo "[3/3] Generating Web UI & starting server..."
python3 backend/generate_complete_ui.py

echo "======================================================================="
echo "  [SUCCESS] SPMA Engine is starting!"
echo "  Local Web Access:   http://localhost:8000"
echo "  Network Web Access: http://0.0.0.0:8000"
echo "======================================================================="
echo ""

# Auto open browser if desktop environment exists
which xdg-open &>/dev/null && xdg-open http://localhost:8000 || which open &>/dev/null && open http://localhost:8000 || true

python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
