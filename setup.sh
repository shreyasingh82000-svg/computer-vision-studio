#!/bin/bash
# Computer Vision Image Processing Studio - Setup Script
# This script sets up the virtual environment and installs dependencies

echo "========================================"
echo "Computer Vision Image Processing Studio"
echo "Setup Script"
echo "========================================"
echo ""

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment!"
    echo "Make sure Python 3 is installed."
    exit 1
fi
echo "Virtual environment created successfully!"
echo ""

echo "Step 2: Activating virtual environment..."
source venv/bin/activate
echo ""

echo "Step 3: Upgrading pip..."
python -m pip install --upgrade pip
echo ""

echo "Step 4: Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies!"
    exit 1
fi
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  1. source venv/bin/activate"
echo "  2. python main.py"
echo ""
echo "Dependencies installed:"
pip list | grep -E "opencv-python|numpy|Pillow"
echo ""
