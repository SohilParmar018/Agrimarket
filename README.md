<<<<<<< HEAD
# 🌾 AgriMarket

A full-stack B2B/B2C agricultural marketplace platform connecting farmers and buyers.

## Features

- **Farmer Dashboard**: Inventory management, order tracking, sales analytics
- **Buyer Portal**: Product browsing, cart, order tracking
- **Real-time Notifications**: SocketIO-powered instant updates
- **Messaging System**: Farmer-Buyer communication
- **B2B Module**: Bulk orders and contract management
- **Payment Integration**: Razorpay payment gateway
- **Reports**: Auto-generated PDF/Excel sales reports
- **Admin Panel**: Platform management and analytics

## Tech Stack

- **Backend**: Python 3.11, Flask, SQLAlchemy
- **Frontend**: Jinja2, Bootstrap 5, Chart.js
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Real-time**: Flask-SocketIO + eventlet
- **Payments**: Razorpay
- **Reports**: ReportLab, openpyxl, pandas

## 🚀 Quick Start (Easiest Way)

### Just run ONE command:

```bash
INSTALL_NOW.bat
```

Then:
```bash
python run.py
```

Visit: http://localhost:5000

That's it! The installer handles everything automatically.

---

## ⚠️ Having Installation Issues?

**Read `START_HERE.txt` first!**

The smart installer (`install.py`) installs packages one by one and shows which ones work. The app will run even if some optional packages fail.

### Manual Installation (if automated fails):

```bash
# Step 1: Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Step 2: Install packages
python install.py

# Step 3: Initialize database
python init_db.py

# Step 4: Run
python run.py
```

---

## Quick Start

### ⚠️ Installation Issues?

If you encounter errors during installation, use the minimal requirements:

```bash
pip install -r requirements-minimal.txt
python test_installation.py  # Verify installation
python init_db.py
python run.py
```

See `QUICK_FIX.txt` or `INSTALL_HELP.md` for details.

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
quickstart.bat
```

**Linux/Mac:**
```bash
chmod +x quickstart.sh
./quickstart.sh
```

Then run:
```bash
python run.py
```

### Option 2: Manual Setup

1. **Create virtual environment**
```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Initialize database**
```bash
python init_db.py
```

5. **Run application**
```bash
python run.py
```

Visit `http://localhost:5000`

## Default Credentials

- **Admin**: admin@agrimarket.com / admin123
- **Farmer**: farmer@test.com / test123 (with 5 sample products)
- **Buyer**: buyer@test.com / test123

## Project Structure

```
agrimarket/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py            # Configuration
│   ├── extensions.py        # Flask extensions
│   ├── models/              # Database models
│   ├── blueprints/          # Route blueprints
│   ├── templates/           # Jinja2 templates
│   └── static/              # CSS, JS, uploads
├── migrations/              # Database migrations
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables
```

## Development Roadmap

- [x] Step 1: Project setup and configuration
- [ ] Step 2: Database models
- [ ] Step 3: Authentication system
- [ ] Step 4: Farmer dashboard
- [ ] Step 5: Buyer portal
- [ ] Step 6: Order management
- [ ] Step 7: Real-time notifications
- [ ] Step 8: Messaging system
- [ ] Step 9: Analytics dashboard
- [ ] Step 10: B2B module
- [ ] Step 11: Payment integration
- [ ] Step 12: Reports generation
- [ ] Step 13: Admin panel
- [ ] Step 14: UI polish
- [ ] Step 15: Deployment

## API Routes

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Farmer
- `GET /farmer/dashboard` - Farmer dashboard
- `GET/POST /farmer/products` - Manage products
- `GET /farmer/orders` - View orders

### Buyer
- `GET /buyer/products` - Browse products
- `POST /buyer/cart` - Manage cart
- `POST /buyer/checkout` - Place order

### Orders
- `GET /orders/<id>` - Order details
- `POST /orders/<id>/status` - Update status

### Messaging
- `GET/POST /messages/<user_id>` - Chat

### Notifications
- `GET /notifications` - Get notifications
- `POST /notifications/mark-read` - Mark as read

### B2B
- `POST /b2b/request` - Request bulk order
- `GET /b2b/contracts` - View contracts

### Reports
- `GET /reports/daily` - Daily report
- `GET /reports/monthly` - Monthly report
- `GET /reports/yearly` - Yearly report

### Admin
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/users` - User management
- `GET /admin/orders` - All orders

## License

MIT License
=======
# Agrimarket
>>>>>>> 57cb2598b72096f8f3fc7a1f31a311cf2e4d865f
