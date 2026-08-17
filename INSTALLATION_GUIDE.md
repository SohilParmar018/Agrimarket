# Complete Installation Guide

## Method 1: Automatic Installation (Recommended)

### Windows

Just double-click or run:
```bash
INSTALL_NOW.bat
```

This will:
1. Create virtual environment
2. Install all packages (one by one)
3. Test the installation
4. Initialize the database
5. Show you what to do next

Then run:
```bash
python run.py
```

### Linux/Mac

```bash
chmod +x quickstart.sh
./quickstart.sh
python run.py
```

## Method 2: Smart Installer

If the automatic installation has issues:

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run smart installer
python install.py

# Initialize database
python init_db.py

# Run application
python run.py
```

The smart installer (`install.py`) installs packages one by one and shows which ones succeed. The app will work with just the core packages!

## Method 3: Manual Installation

If you want full control:

### Step 1: Virtual Environment

```bash
python -m venv venv
```

Activate:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

### Step 2: Install Core Packages

```bash
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-Migrate==4.0.5
pip install Flask-Login==0.6.3
pip install Flask-WTF==1.2.1
pip install python-dotenv==1.0.0
pip install email-validator==2.1.0
pip install python-dateutil==2.8.2
```

### Step 3: Install Optional Packages (skip if they fail)

```bash
pip install Flask-SocketIO==5.3.5
pip install Flask-Mail==0.9.1
pip install reportlab==4.0.7
pip install openpyxl==3.1.2
pip install Pillow==10.1.0
pip install razorpay==1.4.1
pip install APScheduler==3.10.4
```

### Step 4: Test Installation

```bash
python test_installation.py
```

### Step 5: Initialize Database

```bash
python init_db.py
```

### Step 6: Run Application

```bash
python run.py
```

## Method 4: Using Requirements Files

### Core Only (Most Compatible)

```bash
pip install -r requirements-core.txt
```

### Minimal (Core + Some Optional)

```bash
pip install -r requirements-minimal.txt
```

### Full (All Features)

```bash
pip install -r requirements.txt
```

## After Installation

1. Visit: http://localhost:5000

2. Login with default accounts:
   - Admin: admin@agrimarket.com / admin123
   - Farmer: farmer@test.com / test123
   - Buyer: buyer@test.com / test123

3. Explore the features!

## What Works With Core Packages Only?

✅ Everything works! Including:
- User authentication
- Product management
- Shopping cart
- Order processing
- Admin panel
- Reports (PDF/Excel)
- Real-time notifications (using threading)

❌ Only difference:
- Real-time features slightly slower (threading vs eventlet)
- No PostgreSQL support (use SQLite)

## Troubleshooting

### "No module named 'flask_login'"

The package didn't install. Try:
```bash
pip install Flask-Login==0.6.3
```

### "Error building wheel for Pillow"

Pillow is optional. Skip it:
```bash
# The app works without Pillow
# Images just won't be processed
```

### "Port 5000 already in use"

Kill the process:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

Or change the port in `run.py`:
```python
port=5001
```

### Database errors

Reset the database:
```bash
rm agrimarket.db  # or delete the file
python init_db.py
```

### Import errors

Make sure virtual environment is activated:
```bash
# You should see (venv) in your prompt
# If not, activate it:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

## Verification

After installation, verify everything works:

```bash
# Test 1: Check imports
python test_installation.py

# Test 2: Check database
python -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); print('Database OK')"

# Test 3: Check routes
flask routes

# Test 4: Run the app
python run.py
```

## Getting Help

1. Check `START_HERE.txt` for quick start
2. Check `TROUBLESHOOTING.md` for common issues
3. Check `INSTALL_HELP.md` for detailed help
4. Run `python test_installation.py` to see what's missing

## System Requirements

- Python 3.11 or higher
- Windows 10/11, Linux, or macOS
- 100MB free disk space
- Internet connection (for installation)

## Optional: Production Setup

For production deployment:

1. Use PostgreSQL instead of SQLite
2. Set up proper email server
3. Configure Razorpay for payments
4. Use Gunicorn with multiple workers
5. Set up Nginx as reverse proxy
6. Enable HTTPS

See `SETUP.md` for production configuration.

## Success!

If you see the AgriMarket homepage at http://localhost:5000, you're all set!

Explore the features:
- Register as a farmer or buyer
- Add products (farmer)
- Browse and order (buyer)
- Manage platform (admin)
- View analytics and reports

Enjoy using AgriMarket! 🌾
