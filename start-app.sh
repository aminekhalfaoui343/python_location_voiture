#!/bin/bash

# Car Rental Management System - Linux/Mac Startup Script

echo ""
echo "========================================"
echo "Car Rental Management System"
echo "Linux/Mac Startup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    echo "Please install Node.js 16+ from https://nodejs.org"
    exit 1
fi

echo "[✓] Python and Node.js are installed"

# Start Backend
echo ""
echo "Starting Backend API..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

python -m uvicorn app.main:app --reload &
BACKEND_PID=$!
echo "[✓] Backend started at http://localhost:8000"
echo "[✓] API Documentation at http://localhost:8000/api/docs"

# Start Frontend
cd ..
cd frontend

echo ""
echo "Installing frontend dependencies..."
npm install --silent

echo ""
echo "Starting Frontend..."
npm run dev &
FRONTEND_PID=$!
echo "[✓] Frontend started at http://localhost:5173"

# Open browser
echo ""
echo "Opening application in browser..."
sleep 3
if command -v open &> /dev/null; then
    open http://localhost:5173
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5173
fi

echo ""
echo "========================================"
echo "Application is running!"
echo "========================================"
echo "Frontend:  http://localhost:5173"
echo "Backend:   http://localhost:8000"
echo "API Docs:  http://localhost:8000/api/docs"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
