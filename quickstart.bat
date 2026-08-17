@echo off
echo ========================================
echo AgriMarket Quick Start Script
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 3: Installing dependencies...
echo This may take a few minutes...
python install.py
if errorlevel 1 (
    echo.
    echo Installation had some issues.
    echo Trying basic installation...
    pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF python-dotenv Flask-Migrate email-validator python-dateutil
    if errorlevel 1 (
        echo.
        echo Error: Installation failed.
        echo.
        echo Please try:
        echo   1. Run: python install.py
        echo   2. Check: TROUBLESHOOTING.md
        pause
        exit /b 1
    )
)

echo Step 4: Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo .env file created. Please edit it with your settings.
)

echo Step 5: Initializing database...
python init_db.py
if errorlevel 1 (
    echo Error: Failed to initialize database
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application, run:
echo   python run.py
echo.
echo Then visit: http://localhost:5000
echo.
echo Default accounts:
echo   Admin: admin@agrimarket.com / admin123
echo   Farmer: farmer@test.com / test123
echo   Buyer: buyer@test.com / test123
echo.
pause
