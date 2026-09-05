#!/bin/bash
# Computer Vision Image Processing Studio - Quick Launch Script
# This script activates the virtual environment and runs the application

echo "========================================"
echo "Computer Vision Image Processing Studio"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo ""
    echo "Starting application..."
    echo ""
    python main.py
else
    echo "ERROR: Virtual environment not found!"
    echo ""
    echo "Please run setup first:"
    echo "1. chmod +x setup.sh"
    echo "2. ./setup.sh"
    echo ""
    echo "Or manually:"
    echo "1. python3 -m venv venv"
    echo "2. source venv/bin/activate"
    echo "3. pip install -r requirements.txt"
    echo ""
fi
