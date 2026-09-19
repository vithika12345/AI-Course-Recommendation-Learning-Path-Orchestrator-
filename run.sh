#!/usr/bin/env bash
echo "========================================================"
echo "  EduAgent: AI Course Recommendation & Roadmap Orchestrator"
echo "========================================================"
echo ""

if ! command -v python3 &> /dev/null
then
    echo "[ERROR] python3 could not be found. Please install Python."
    exit 1
fi

echo "Installing required dependencies..."
pip install -r requirements.txt

echo "Launching Gradio Web App on http://127.0.0.1:7860..."
python3 app.py
