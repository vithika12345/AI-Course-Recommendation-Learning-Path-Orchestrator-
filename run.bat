@echo off
title EduAgent - AI Course Recommender
echo ========================================================
echo   EduAgent: AI Course Recommendation & Roadmap Orchestrator
echo ========================================================
echo.
echo Checking Python environment...
python --version
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    pause
    exit /b 1
)

echo.
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo Starting EduAgent Gradio Application on http://127.0.0.1:7860...
python app.py
pause
