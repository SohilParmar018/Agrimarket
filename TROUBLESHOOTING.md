# Troubleshooting Guide

## Installation Issues

### Error: "Getting requirements to build wheel did not run successfully"

This error typically occurs when packages require compilation and you don't have the necessary build tools.

#### Solution 1: Use Minimal Requirements (Recommended for Development)

```bash
pip install -r requirements-minimal.txt
```

This installs only the essential packages without heavy dependencies like pandas, gevent, or psycopg2.

#### Solution 2: Install Build Tools

**Windows:**
1. Install Microsoft C++ Build Tools:
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Install "Desktop development with C++"
   - Restart your terminal

2. Then retry:
   ```bash
   pip install -r requirements.txt
   ```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3-dev build-essential
pip install -r requirements.txt
```

**Mac:**
```bash
xcode-select --install
pip install -r requirements.txt
```

#### Solution 3: Install Packages Individually

If you still have issues, install packages one by one:

```bash
# Core packages (should work on all systems)
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-Migrate==4.0.5
pip install Flask-Login==0.6.3
pip install Flask-WTF==1.2.1
pip install Flask-SocketIO==5.3.5
pip install python-socketio==5.10.0
pip install python-dotenv==1.0.0
pip install Werkzeug==3.0.1
pip install email-validator==2.1.0
pip install WTForms==3.1.1
pip install Pillow==10.1.0
pip install reportlab==4.0.7
pip install openpyxl==3.1.2
pip install APScheduler==3.10.4
pip install python-dateutil==2.8.2

# Optional packages (skip if they fail)
pip install razorpay==1.4.1
pip install cloudinary==1.36.0
```

### Error: "No module named 'eventlet'" or "No module named 'gevent'"

The app uses SocketIO for real-time features. If you can't install eventlet or gevent:

**Option 1: Run without real-time features**

Edit `run.py` and change:
```python
if __name__ == '__main__':
    # Run with SocketIO for real-time features
    socketio.run(
        app,
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=5000
    )
```

To:
```python
if __name__ == '__main__':
    # Run without SocketIO (no real-time features)
    app.run(
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=5000
    )
```

**Option 2: Use threading mode**

Edit `app/__init__.py` and change:
```python
socketio.init_app(app, cors_allowed_origins="*", async_mode='eventlet')
```

To:
```python
socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')
```

### Error: "No module named 'psycopg2'"

This is only needed for PostgreSQL in production. For development with SQLite, you don't need it.

If you need PostgreSQL support:
```bash
# Windows (easier alternative)
pip install psycopg2-binary

# Or use the connection string without psycopg2
# In .env, use SQLite:
DATABASE_URL=sqlite:///agrimarket.db
```

### Error: Database migration issues

```bash
# Delete existing migrations and database
rm -rf migrations/
rm agrimarket.db

# Reinitialize
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python init_db.py
```

### Error: "Port 5000 already in use"

**Windows:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
# Find and kill process
lsof -ti:5000 | xargs kill -9
```

Or change the port in `run.py`:
```python
port=5001  # Change to any available port
```

### Error: "ImportError: cannot import name 'X' from 'Y'"

This usually means version conflicts. Try:

```bash
# Uninstall all packages
pip freeze > installed.txt
pip uninstall -r installed.txt -y

# Reinstall
pip install -r requirements-minimal.txt
```

## Runtime Issues

### Error: "Working outside of application context"

Make sure you're running commands with the app context:

```python
from app import create_app
app = create_app()

with app.app_context():
    # Your code here
    pass
```

### Error: "No such table: users"

Database not initialized. Run:
```bash
python init_db.py
```

### Error: "CSRF token missing"

Make sure forms include:
```html
{{ form.hidden_tag() }}
```

Or disable CSRF for testing (not recommended for production):
```python
# In config.py
WTF_CSRF_ENABLED = False
```

### Error: "Template not found"

Check that template paths match blueprint names:
```python
# In blueprint __init__.py
Blueprint('auth', __name__, template_folder='templates')

# Templates should be in: app/templates/auth/
```

### Error: "Static files not loading"

Make sure static files are in `app/static/` and referenced correctly:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

## Development Tips

### Quick Reset

```bash
# Delete database and start fresh
rm agrimarket.db
python init_db.py
python run.py
```

### Debug Mode

Make sure `FLASK_ENV=development` in `.env` for detailed error messages.

### Check Routes

```bash
flask routes
```

### Interactive Shell

```bash
flask shell
>>> from app.models.user import User
>>> User.query.all()
```

## Common Configuration Issues

### Email not sending

For development, emails are just logged. To actually send:

1. Use Gmail:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=your-app-password  # Not your regular password!
```

2. Generate app password: https://myaccount.google.com/apppasswords

### File uploads not working

Check permissions:
```bash
# Windows
icacls app\static\uploads /grant Users:F

# Linux/Mac
chmod -R 755 app/static/uploads
```

### SocketIO not connecting

1. Check browser console for errors
2. Make sure SocketIO client is loaded:
```html
<script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
```

3. Check CORS settings in `app/__init__.py`

## Performance Issues

### Slow page loads

1. Use pagination for large datasets
2. Add database indexes
3. Enable query caching

### Database locked (SQLite)

SQLite doesn't handle concurrent writes well. For production, use PostgreSQL.

## Getting Help

1. Check error message carefully
2. Search error on Stack Overflow
3. Check Flask documentation: https://flask.palletsprojects.com/
4. Check SQLAlchemy docs: https://docs.sqlalchemy.org/

## Minimal Working Setup

If all else fails, here's the absolute minimum to get started:

```bash
# Install only core packages
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF python-dotenv

# Create minimal .env
echo "FLASK_ENV=development" > .env
echo "SECRET_KEY=dev-secret-key" >> .env
echo "DATABASE_URL=sqlite:///agrimarket.db" >> .env

# Initialize database
python init_db.py

# Run (without SocketIO)
python -c "from app import create_app; app = create_app(); app.run(debug=True)"
```

This gives you a working app without real-time features, which you can add later.

## Windows-Specific Issues

### Python not found

Make sure Python is in PATH:
```bash
# Check Python installation
python --version

# If not found, reinstall Python and check "Add to PATH"
```

### Virtual environment activation fails

```bash
# Use full path
C:\path\to\venv\Scripts\activate.bat

# Or use PowerShell
.\venv\Scripts\Activate.ps1

# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Line ending issues

If you get syntax errors after cloning:
```bash
git config core.autocrlf true
```

## Still Having Issues?

Try the minimal installation:

1. Create a new virtual environment
2. Install minimal requirements: `pip install -r requirements-minimal.txt`
3. Initialize database: `python init_db.py`
4. Run app: `python run.py`

This should work on any system with Python 3.11+.
