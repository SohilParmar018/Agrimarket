========================================
   AGRIMARKET - READ THIS FIRST!
========================================

YOU HAVE PYTHON 3.13 - IT'S TOO NEW!
------------------------------------

The packages don't fully support Python 3.13 yet.

EASIEST FIX:
-----------

In PowerShell, run:

    .\FIX_NOW.bat

This installs Python 3.13 compatible versions.

Then:

    python run.py

Visit: http://localhost:5000

========================================

OR: Use Python 3.11/3.12 (Better)
----------------------------------

1. Download Python 3.11 from python.org
2. Install it
3. Run: py -3.11 -m venv venv
4. Run: venv\Scripts\activate
5. Run: .\FIX_NOW.bat

========================================

MANUAL FIX (if scripts don't work):
-----------------------------------

venv\Scripts\activate
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF python-dotenv Flask-Migrate email-validator
python init_db.py
python run.py

========================================

DEFAULT ACCOUNTS:
----------------
Admin:  admin@agrimarket.com / admin123
Farmer: farmer@test.com / test123
Buyer:  buyer@test.com / test123

========================================
