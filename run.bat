@echo off
echo 🚀 Starting Solana MCP Server
echo =============================

REM Check if virtual environment exists
if not exist venv (
    echo ❌ Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found. Using default configuration.
    echo    Create .env file from .env.example for custom settings.
    echo.
)

REM Start the MCP server
echo ✅ Starting MCP server...
echo    Press Ctrl+C to stop the server
echo.
venv\Scripts\python.exe solana_mcp_server.py

echo.
echo 👋 MCP server stopped
pause