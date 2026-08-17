# Python 3.13 Compatibility Issue

## The Problem

You're using **Python 3.13**, which is very new (released October 2024). Some packages don't fully support it yet, causing installation errors.

## Solution 1: Use Python 3.11 or 3.12 (Recommended)

### Download and Install

1. Go to: https://www.python.org/downloads/
2. Download **Python 3.11.x** (most stable) or **Python 3.12.x**
3. Install it (check "Add to PATH")
4. Open new terminal
5. Run:
   ```bash
   py -3.11 -m venv venv
   venv\Scripts\activate
   .\FIX_NOW.bat
   ```

## Solution 2: Fix Current Python 3.13 Installation

Run this script which installs Python 3.13 compatible versions:

```bash
.\FIX_NOW.bat
```

This will:
- Install latest SQLAlchemy (3.13 compatible)
- Install all core packages
- Skip problematic packages
- Initialize the database
- Get you running!

## Solution 3: Manual Fix (If scripts fail)

Open PowerShell in the project folder:

```powershell
# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install core packages one by one
pip install Flask==3.0.0
pip install "SQLAlchemy>=2.0.25"
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-Login==0.6.3
pip install Flask-WTF==1.2.1
pip install Flask-Migrate==4.0.5
pip install python-dotenv==1.0.0
pip install email-validator==2.1.0
pip install python-dateutil==2.8.2

# Test it
python test_installation.py

# Initialize database
python init_db.py

# Run the app
python run.py
```

## What's the Issue?

The error you're seeing:
```
AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> 
directly inherits TypingOnly but has additional attributes
```

This happens because SQLAlchemy 2.0.23 uses Python typing features that changed in Python 3.13.

## Quick Check: Which Python Version?

```bash
python --version
```

If it says **3.13.x**, you have two options:
1. Use Python 3.11 or 3.12 (easier)
2. Use latest package versions (FIX_NOW.bat does this)

## After Fix

Once packages are installed:

```bash
python run.py
```

Visit: http://localhost:5000

Login:
- Admin: admin@agrimarket.com / admin123
- Farmer: farmer@test.com / test123
- Buyer: buyer@test.com / test123

## Still Having Issues?

Try the absolute minimal installation:

```bash
venv\Scripts\activate
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF python-dotenv
python init_db.py
python run.py
```

This installs only the bare minimum. The app will work but without some optional features.
