# Installation Help - Quick Fix

## If you're getting installation errors, follow these steps:

### Step 1: Use Minimal Requirements

Instead of `requirements.txt`, use `requirements-minimal.txt`:

```bash
pip install -r requirements-minimal.txt
```

This installs only essential packages without compilation requirements.

### Step 2: Initialize Database

```bash
python init_db.py
```

### Step 3: Run Application

```bash
python run.py
```

Visit: http://localhost:5000

## What's Different?

The minimal requirements:
- ✅ Removes `pandas` (not essential for core functionality)
- ✅ Removes `psycopg2-binary` (only needed for PostgreSQL)
- ✅ Uses `threading` instead of `eventlet/gevent` (better Windows compatibility)
- ✅ Keeps all core features working

## What Still Works?

Everything works except:
- Real-time features use threading (slightly slower but functional)
- PostgreSQL support (use SQLite for development)

## If That Still Fails

Install packages manually:

```bash
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-Migrate==4.0.5
pip install Flask-Login==0.6.3
pip install Flask-WTF==1.2.1
pip install python-dotenv==1.0.0
```

Then run:
```bash
python init_db.py
python run.py
```

## Need More Help?

Check `TROUBLESHOOTING.md` for detailed solutions to common issues.

## Quick Test

After installation, test if it works:

```bash
python -c "from app import create_app; print('✓ Installation successful!')"
```

If you see "✓ Installation successful!", you're good to go!
