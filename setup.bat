@echo off
REM Computer Vision Image Processing Studio - Setup Script
REM This script sets up the virtual environment and installs dependencies

echo ========================================
echo Computer Vision Image Processing Studio
echo Setup Script
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment!
    echo Make sure Python is installed and added to PATH.
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 4: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application:
echo   Option 1: Double-click "run_app.bat"
echo   Option 2: Run "python main.py" in terminal
echo.
echo Dependencies installed:
pip list | findstr "opencv-python numpy Pillow"
echo.
pause
