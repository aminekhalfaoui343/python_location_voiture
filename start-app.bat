@echo off
REM Car Rental Management System - Windows Startup Script

echo.
echo ========================================
echo Car Rental Management System
echo Windows Startup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org
    pause
    exit /b 1
)

echo [✓] Python and Node.js are installed

REM Start Backend
echo.
echo Starting Backend API...
cd backend
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -q -r requirements.txt

start "Car Rental Backend" python -m uvicorn app.main:app --reload
echo [✓] Backend started at http://localhost:8000
echo [✓] API Documentation at http://localhost:8000/api/docs

REM Start Frontend
cd ..
cd frontend
echo.
echo Installing frontend dependencies...
call npm install --silent

echo.
echo Starting Frontend...
start "Car Rental Frontend" npm run dev
echo [✓] Frontend started at http://localhost:5173

REM Open browser
echo.
echo Opening application in browser...
timeout /t 3
start http://localhost:5173

echo.
echo ========================================
echo Application is running!
echo ========================================
echo Frontend:  http://localhost:5173
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/api/docs
echo ========================================
echo.
echo Press any key to close this window...
pause
