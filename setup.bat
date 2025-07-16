@echo off
echo 🚀 Solana MCP Server Setup for Windows
echo =====================================

REM Check if Python is available
py --version >nul 2>&1
if %errorlevel% neq 0 (
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Python not found. Please install Python 3.8+ from python.org
        echo    Make sure to add Python to your PATH during installation
        pause
        exit /b 1
    )
    set PYTHON_CMD=python
) else (
    set PYTHON_CMD=py
)

echo ✅ Python found
%PYTHON_CMD% --version

REM Create virtual environment
echo.
echo 📦 Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
)

REM Activate virtual environment and install dependencies
echo.
echo 📦 Installing dependencies...
call venv\Scripts\activate.bat
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\pip.exe install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed

REM Create .env file if it doesn't exist
echo.
echo 📦 Setting up configuration...
if exist .env (
    echo .env file already exists
) else (
    copy .env.example .env
    echo ✅ Created .env file from template
    echo ⚠️  Please edit .env file with your configuration
)

echo.
echo 🎉 Setup completed successfully!
echo =====================================
echo.
echo 📋 Next steps:
echo 1. Edit the .env file with your Solana configuration
echo 2. Activate the virtual environment: venv\Scripts\activate.bat
echo 3. Run the MCP server: venv\Scripts\python.exe solana_mcp_server.py
echo 4. Or run examples: venv\Scripts\python.exe examples.py
echo.
echo 📚 Files created:
echo    - solana_mcp_server.py (main MCP server)
echo    - examples.py (usage examples)
echo    - test_server.py (test script)
echo    - config.py (configuration management)
echo    - utils.py (utility functions)
echo.
echo ⚠️  Security reminders:
echo    - Never commit private keys to version control
echo    - Test on devnet before using mainnet
echo    - Keep your .env file secure
echo.
pause