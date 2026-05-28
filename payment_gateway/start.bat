@echo off
REM Colors using echo with special characters
setlocal enabledelayedexpansion

cls
echo.
echo ====================================================================
echo                   PAYMENT GATEWAY SETUP
echo ====================================================================
echo.

REM Get the directory where the script is located
set "SCRIPT_DIR=%~dp0"

echo Location: %SCRIPT_DIR%
echo.

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker not found. Please install Docker.
    pause
    exit /b 1
)

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 18+.
    pause
    exit /b 1
)

echo [INFO] Docker found: %PATH%
echo [INFO] Node.js version:
node --version
echo [INFO] npm version:
npm --version
echo.

REM Check if we need to install frontend dependencies
if not exist "%SCRIPT_DIR%payment_gateway\frontend\node_modules" (
    echo [INFO] Installing frontend dependencies...
    cd /d "%SCRIPT_DIR%payment_gateway\frontend"
    call npm install
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [SUCCESS] Dependencies installed!
    echo.
)

echo ====================================================================
echo Starting Backend (Python + MongoDB)...
echo ====================================================================
echo.

cd /d "%SCRIPT_DIR%payment_gateway"
call docker-compose up -d

if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to start Docker
    pause
    exit /b 1
)

echo [SUCCESS] Docker started!
echo [INFO] Backend running at: http://localhost:8000
echo [INFO] API Docs at: http://localhost:8000/docs
echo.

echo Waiting 15 seconds for services to start...
timeout /t 15 /nobreak

echo.
echo ====================================================================
echo Starting Frontend (Next.js)...
echo ====================================================================
echo.

cd /d "%SCRIPT_DIR%payment_gateway\frontend"
call npm run dev

pause