"""
Buyer Routes
Product browsing, cart, and checkout
"""
from flask import render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_required, current_user
from app.blueprints.buyer import buyer_bp
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.notification import Notification
from app.extensions import db, socketio
from app.utils.decorators import buyer_required


@buyer_bp.route('/dashboard')
@login_required
@buyer_required
def dashboard():
    """Buyer dashboard"""
    recent_orders = Order.query.filter_by(
        buyer_id=current_user.id
    ).order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('buyer/dashboard.html', recent_orders=recent_orders)


@buyer_bp.route('/products')
@login_required
@buyer_required
def products():
    """Browse products"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    
    query = Product.query.filter_by(is_active=True)
    
    if category != 'all':
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    return render_template('buyer/products.html', products=products, 
                         current_category=category, search=search)


@buyer_bp.route('/products/<int:id>')
@login_required
@buyer_required
def product_detail(id):
    """Product detail page"""
    product = Product.query.get_or_404(id)
    return render_template('buyer/product_detail.html', product=product)


@buyer_bp.route('/cart')
@login_required
@buyer_required
def cart():
    """View cart"""
    cart_items = session.get('cart', {})
    products = []
    total = 0
    
    for product_id, quantity in cart_items.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.calculate_total(quantity)
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
    
    return render_template('buyer/cart.html', products=products, total=total)


@buyer_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
@buyer_required
def add_to_cart(product_id):
    """Add product to cart"""
    product = Product.query.get_or_404(product_id)
    quantity = float(request.form.get('quantity', 1))
    
    if not product.can_fulfill_order(quantity):
        flash('Insufficient stock!', 'danger')
        return redirect(url_for('buyer.product_detail', id=product_id))
    
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    session['cart'] = cart
    
    flash('Product added to cart!', 'success')
    return redirect(url_for('buyer.products'))


@buyer_bp.route('/cart/remove/<int:product_id>', methods=['POST'])
@login_required
@buyer_required
def remove_from_cart(product_id):
    """Remove product from cart"""
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    
    flash('Product removed from cart!', 'info')
    return redirect(url_for('buyer.cart'))


@buyer_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
@buyer_required
def checkout():
    """Checkout and place order"""
    cart_items = session.get('cart', {})
    
    if not cart_items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('buyer.products'))
    
    if request.method == 'POST':
        address = request.form.get('address')
        notes = request.form.get('notes', '')
        
        # Group items by farmer
        farmer_orders = {}
        for product_id, quantity in cart_items.items():
            product = Product.query.get(int(product_id))
            if product and product.can_fulfill_order(quantity):
                if product.farmer_id not in farmer_orders:
                    farmer_orders[product.farmer_id] = []
                farmer_orders[product.farmer_id].append((product, quantity))
        
        # Create orders for each farmer
        for farmer_id, items in farmer_orders.items():
            order = Order(
                buyer_id=current_user.id,
                farmer_id=farmer_id,
                delivery_address=address,
                notes=notes
            )
            db.session.add(order)
            db.session.flush()
            
            for product, quantity in items:
                order.add_item(product, quantity)
                product.reduce_stock(quantity)
            
            order.calculate_totals()
            
            # Create notification for farmer
            Notification.create_notification(
                user_id=farmer_id,
                type='order',
                title='New Order Received',
                message=f'You have a new order from {current_user.name}',
                action_url=url_for('farmer.orders')
            )
        
        db.session.commit()
        session.pop('cart', None)
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('buyer.orders'))
    
    return render_template('buyer/checkout.html')


@buyer_bp.route('/orders')
@login_required
@buyer_required
def orders():
    """View buyer orders"""
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(
        buyer_id=current_user.id
    ).order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('buyer/orders.html', orders=orders)
