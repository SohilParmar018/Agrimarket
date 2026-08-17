#!/bin/bash

echo "========================================"
echo "AgriMarket Quick Start Script"
echo "========================================"
echo ""

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo "Step 3: Installing dependencies..."
pip install -r requirements-minimal.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    echo "Trying alternative installation method..."
    pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF python-dotenv Flask-Migrate
    if [ $? -ne 0 ]; then
        echo "Error: Installation failed. Please check TROUBLESHOOTING.md"
        exit 1
    fi
fi

echo "Step 4: Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created. Please edit it with your settings."
fi

echo "Step 5: Initializing database..."
python init_db.py
if [ $? -ne 0 ]; then
    echo "Error: Failed to initialize database"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To start the application, run:"
echo "  python run.py"
echo ""
echo "Then visit: http://localhost:5000"
echo ""
echo "Default accounts:"
echo "  Admin: admin@agrimarket.com / admin123"
echo "  Farmer: farmer@test.com / test123"
echo "  Buyer: buyer@test.com / test123"
echo ""
