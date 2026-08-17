# AgriMarket Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update with your settings:

```bash
cp .env.example .env
```

Edit `.env` with your configuration (database, mail, Razorpay keys, etc.)

### 3. Initialize Database

```bash
# Initialize Flask-Migrate
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade

# Create admin user
python run.py seed_admin
```

Default admin credentials:
- Email: admin@agrimarket.com
- Password: admin123

### 4. Run Application

```bash
# Development mode
python run.py
```

Visit http://localhost:5000

## Project Structure

```
agrimarket/
├── app/
│   ├── __init__.py              # App factory
│   ├── config.py                # Configuration
│   ├── extensions.py            # Flask extensions
│   ├── models/                  # Database models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── message.py
│   │   ├── notification.py
│   │   ├── b2b_contract.py
│   │   └── sales_report.py
│   ├── blueprints/              # Route blueprints
│   │   ├── auth/                # Authentication
│   │   ├── farmer/              # Farmer features
│   │   ├── buyer/               # Buyer features
│   │   ├── orders/              # Order management
│   │   ├── messaging/           # Real-time chat
│   │   ├── notifications/       # Notifications
│   │   ├── b2b/                 # B2B contracts
│   │   ├── reports/             # Reports & exports
│   │   └── admin/               # Admin panel
│   ├── templates/               # Jinja2 templates
│   ├── static/                  # CSS, JS, uploads
│   └── utils/                   # Helper functions
├── migrations/                  # Database migrations
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── .env                         # Environment variables
```

## Features Implemented

✅ Step 1: Project setup and configuration
✅ Step 2: Database models with relationships
✅ Step 3: Authentication system (register, login, profile)
✅ Step 4: Farmer dashboard and inventory management
✅ Step 5: Buyer portal (browse, cart, checkout)
✅ Step 6: Order management and tracking
✅ Step 7: Real-time notifications (SocketIO)
✅ Step 8: Messaging system
✅ Step 9: Farmer analytics dashboard
✅ Step 10: B2B module (bulk orders, contracts)
✅ Step 11: Payment integration (Razorpay ready)
✅ Step 12: Reports generation (PDF/Excel)
✅ Step 13: Admin panel
✅ Step 14: UI polish (Bootstrap 5, responsive)
✅ Step 15: Deployment config (Dockerfile, Gunicorn)

## User Roles

### Farmer
- Manage product inventory
- View and process orders
- Access sales analytics
- Handle B2B contracts
- Generate reports

### Buyer
- Browse products
- Shopping cart
- Place orders
- Track deliveries
- Request bulk orders

### Admin
- User management
- Verify farmer accounts
- Platform statistics
- Broadcast notifications
- Monitor all orders

## Next Steps

1. Configure Razorpay payment gateway
2. Set up email server for notifications
3. Configure Cloudinary for production file uploads
4. Set up Redis for SocketIO in production
5. Deploy to production server

## Development Tips

- Use `flask shell` to interact with models
- Check `flask routes` to see all registered routes
- Run migrations after model changes: `flask db migrate` then `flask db upgrade`
- View logs in terminal for debugging

## Production Deployment

See `Dockerfile` for containerized deployment.

For manual deployment:
1. Set `FLASK_ENV=production` in `.env`
2. Use PostgreSQL database
3. Configure Gunicorn: `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 run:app`
4. Set up Nginx as reverse proxy
5. Enable HTTPS with SSL certificate
