"""
Quick installation test script
Run this to verify your installation is working
"""

print("Testing AgriMarket installation...\n")

# Test 1: Import Flask
try:
    import flask
    print("✓ Flask installed")
except ImportError as e:
    print("✗ Flask not installed:", e)
    exit(1)

# Test 2: Import SQLAlchemy
try:
    import flask_sqlalchemy
    print("✓ Flask-SQLAlchemy installed")
except ImportError as e:
    print("✗ Flask-SQLAlchemy not installed:", e)
    exit(1)

# Test 3: Import Flask-Login
try:
    import flask_login
    print("✓ Flask-Login installed")
except ImportError as e:
    print("✗ Flask-Login not installed:", e)
    exit(1)

# Test 4: Create app
try:
    from app import create_app
    app = create_app()
    print("✓ App factory working")
except Exception as e:
    print("✗ App creation failed:", e)
    exit(1)

# Test 5: Check database models
try:
    from app.models.user import User
    from app.models.product import Product
    from app.models.order import Order
    print("✓ Database models loaded")
except Exception as e:
    print("✗ Models import failed:", e)
    exit(1)

# Test 6: Check blueprints
try:
    from app.blueprints.auth import auth_bp
    from app.blueprints.farmer import farmer_bp
    from app.blueprints.buyer import buyer_bp
    print("✓ Blueprints loaded")
except Exception as e:
    print("✗ Blueprints import failed:", e)
    exit(1)

# Test 7: Check app context
try:
    with app.app_context():
        from app.extensions import db
        print("✓ App context working")
except Exception as e:
    print("✗ App context failed:", e)
    exit(1)

print("\n" + "="*50)
print("✓ All tests passed!")
print("="*50)
print("\nYour installation is working correctly.")
print("\nNext steps:")
print("1. Run: python init_db.py")
print("2. Run: python run.py")
print("3. Visit: http://localhost:5000")
print("\nDefault login:")
print("  Admin: admin@agrimarket.com / admin123")
print("  Farmer: farmer@test.com / test123")
print("  Buyer: buyer@test.com / test123")
