@echo off
echo ========================================
echo Python 3.13 Compatibility Fix
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing compatible packages...
echo.

pip install --upgrade pip

echo Installing Flask...
pip install Flask==3.0.0

echo Installing SQLAlchemy (latest for Python 3.13)...
pip install SQLAlchemy>=2.0.25

echo Installing Flask-SQLAlchemy...
pip install Flask-SQLAlchemy==3.1.1

echo Installing Flask-Login...
pip install Flask-Login==0.6.3

echo Installing Flask-WTF...
pip install Flask-WTF==1.2.1

echo Installing Flask-Migrate...
pip install Flask-Migrate==4.0.5

echo Installing utilities...
pip install python-dotenv==1.0.0
pip install email-validator==2.1.0
pip install python-dateutil==2.8.2
pip install WTForms==3.1.1

echo Installing optional packages (may fail, that's OK)...
pip install Flask-SocketIO --no-deps
pip install python-socketio
pip install Flask-Mail
pip install reportlab
pip install openpyxl

echo.
echo ========================================
echo Testing installation...
echo ========================================
python test_installation.py

if errorlevel 1 (
    echo.
    echo Some packages failed but core packages should work.
    echo.
)

echo.
echo ========================================
echo Initializing database...
echo ========================================
python init_db.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo   python run.py
echo.
echo Then visit: http://localhost:5000
echo.
pause
