@echo off
echo ========================================
echo AgriMarket - Easy Installer
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    echo Make sure Python 3.11+ is installed
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing packages (this may take a few minutes)...
echo.
python install.py

echo.
echo ========================================
echo Testing installation...
echo ========================================
python test_installation.py

if errorlevel 1 (
    echo.
    echo Installation test failed. Check errors above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Initializing database...
echo ========================================
python init_db.py

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To start the application:
echo   python run.py
echo.
echo Then visit: http://localhost:5000
echo.
pause
