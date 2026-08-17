"""
Smart installer for AgriMarket
Installs packages one by one and handles failures gracefully
"""
import subprocess
import sys

def install_package(package):
    """Install a single package"""
    try:
        print(f"Installing {package}...", end=" ")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print("✓")
            return True
        else:
            print("✗ (skipped)")
            return False
    except Exception as e:
        print(f"✗ (error: {e})")
        return False

def main():
    print("="*60)
    print("AgriMarket Smart Installer")
    print("="*60)
    print()
    
    # Upgrade pip first
    print("Upgrading pip...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                   capture_output=True)
    print()
    
    # Install core packages
    print("Installing CORE packages (required)...")
    print("-"*60)
    
    core_packages = [
        "Flask==3.0.0",
        "Werkzeug==3.0.1",
        "SQLAlchemy>=2.0.25",  # Python 3.13 compatible
        "Flask-SQLAlchemy==3.1.1",
        "Flask-Migrate==4.0.5",
        "Flask-Login==0.6.3",
        "WTForms==3.1.1",
        "Flask-WTF==1.2.1",
        "python-dotenv==1.0.0",
        "email-validator==2.1.0",
        "python-dateutil==2.8.2"
    ]
    
    core_success = 0
    for package in core_packages:
        if install_package(package):
            core_success += 1
    
    print()
    print(f"Core packages: {core_success}/{len(core_packages)} installed")
    
    if core_success < len(core_packages):
        print()
        print("⚠️  Some core packages failed to install.")
        print("The app may not work correctly.")
        print()
    
    # Install optional packages
    print()
    print("Installing OPTIONAL packages (app works without these)...")
    print("-"*60)
    
    optional_packages = [
        "Flask-SocketIO==5.3.5",
        "python-socketio==5.10.0",
        "Flask-JWT-Extended==4.5.3",
        "Flask-Mail==0.9.1",
        "reportlab==4.0.7",
        "openpyxl==3.1.2",
        "Pillow==10.1.0",
        "razorpay==1.4.1",
        "APScheduler==3.10.4"
    ]
    
    optional_success = 0
    for package in optional_packages:
        if install_package(package):
            optional_success += 1
    
    print()
    print(f"Optional packages: {optional_success}/{len(optional_packages)} installed")
    
    # Summary
    print()
    print("="*60)
    print("Installation Summary")
    print("="*60)
    print(f"✓ Core packages: {core_success}/{len(core_packages)}")
    print(f"✓ Optional packages: {optional_success}/{len(optional_packages)}")
    print()
    
    if core_success == len(core_packages):
        print("✓ Installation successful!")
        print()
        print("Next steps:")
        print("1. Run: python test_installation.py")
        print("2. Run: python init_db.py")
        print("3. Run: python run.py")
        print("4. Visit: http://localhost:5000")
        print()
        print("Default accounts:")
        print("  Admin: admin@agrimarket.com / admin123")
        print("  Farmer: farmer@test.com / test123")
        print("  Buyer: buyer@test.com / test123")
    else:
        print("⚠️  Installation incomplete!")
        print()
        print("Some core packages failed. Try:")
        print("1. Update Python: python.org/downloads")
        print("2. Install Visual C++ Build Tools (Windows)")
        print("3. Check TROUBLESHOOTING.md for help")
    
    print("="*60)

if __name__ == "__main__":
    main()
