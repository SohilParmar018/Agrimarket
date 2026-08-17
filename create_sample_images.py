"""
Create sample product images
Run this to generate placeholder images for the sample products
"""
import os
from PIL import Image, ImageDraw, ImageFont

# Create uploads directory if it doesn't exist
upload_dir = 'app/static/uploads/products'
os.makedirs(upload_dir, exist_ok=True)

# Product images to create
products = [
    {'name': 'Tomatoes', 'color': '#FF6347', 'filename': 'tomatoes.jpg'},
    {'name': 'Potatoes', 'color': '#D2B48C', 'filename': 'potatoes.jpg'},
    {'name': 'Onions', 'color': '#F5DEB3', 'filename': 'onions.jpg'},
    {'name': 'Rice', 'color': '#F5F5DC', 'filename': 'rice.jpg'},
    {'name': 'Mangoes', 'color': '#FFD700', 'filename': 'mangoes.jpg'},
]

def create_product_image(name, color, filename):
    """Create a simple product image with text"""
    # Create image
    img = Image.new('RGB', (400, 400), color=color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Add text
    text = name
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((400 - text_width) // 2, (400 - text_height) // 2)
    
    # Draw text with shadow for better visibility
    draw.text((position[0]+2, position[1]+2), text, fill='black', font=font)
    draw.text(position, text, fill='white', font=font)
    
    # Save image
    filepath = os.path.join(upload_dir, filename)
    img.save(filepath, 'JPEG', quality=85)
    print(f"✓ Created {filename}")
    return f'uploads/products/{filename}'

print("Creating sample product images...")
print("-" * 50)

image_paths = {}
for product in products:
    path = create_product_image(product['name'], product['color'], product['filename'])
    image_paths[product['name']] = path

print("-" * 50)
print("✓ All images created successfully!")
print()
print("Image paths:")
for name, path in image_paths.items():
    print(f"  {name}: {path}")
print()
print("Now update the database with these image paths:")
print("Run: python update_product_images.py")
