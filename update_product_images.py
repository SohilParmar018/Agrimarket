"""
Update product images in database
Run this after creating sample images
"""
from app import create_app
from app.extensions import db
from app.models.product import Product

app = create_app()

with app.app_context():
    print("Updating product images...")
    print("-" * 50)
    
    # Image mapping
    image_map = {
        'Fresh Tomatoes': 'uploads/products/tomatoes.jpg',
        'Potatoes': 'uploads/products/potatoes.jpg',
        'Onions': 'uploads/products/onions.jpg',
        'Basmati Rice': 'uploads/products/rice.jpg',
        'Fresh Mangoes': 'uploads/products/mangoes.jpg',
    }
    
    updated = 0
    for product_name, image_path in image_map.items():
        product = Product.query.filter_by(name=product_name).first()
        if product:
            product.image_url = image_path
            print(f"✓ Updated {product_name}")
            updated += 1
        else:
            print(f"✗ Product not found: {product_name}")
    
    db.session.commit()
    
    print("-" * 50)
    print(f"✓ Updated {updated} product images!")
    print()
    print("Restart the application to see the changes:")
    print("  Press CTRL+C to stop")
    print("  Run: python run.py")
