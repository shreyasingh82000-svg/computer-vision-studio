@echo off
REM Computer Vision Image Processing Studio - Quick Launch Script
REM This script activates the virtual environment and runs the application

echo ========================================
echo Computer Vision Image Processing Studio
echo ========================================
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo.
    echo Starting application...
    echo.
    python main.py
) else (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run setup first:
    echo 1. python -m venv venv
    echo 2. venv\Scripts\activate
    echo 3. pip install -r requirements.txt
    echo.
    pause
)
