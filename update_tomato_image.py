"""Update tomato product with image"""
from app import create_app
from app.models.product import Product
from app.extensions import db

app = create_app()
app.app_context().push()

# Find the tomato product
tomato = Product.query.filter_by(name='tomato').first()

if tomato:
    tomato.image_url = 'uploads/products/tomatoes.jpg'
    db.session.commit()
    print(f'✓ Updated "{tomato.name}" with image: {tomato.image_url}')
else:
    print('⚠️  Tomato product not found')

# Show all products with images
print('\nAll Products:')
products = Product.query.all()
for p in products:
    status = '✓' if p.image_url else '✗'
    print(f'{status} {p.id}. {p.name}: {p.image_url or "No image"}')
