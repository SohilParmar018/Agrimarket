"""
B2B Routes
Bulk orders and contracts
"""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.blueprints.b2b import b2b_bp
from app.models.b2b_contract import B2BContract
from app.models.product import Product
from app.models.notification import Notification
from app.extensions import db


@b2b_bp.route('/contracts')
@login_required
def contracts():
    """View contracts"""
    if current_user.is_buyer():
        contracts = B2BContract.query.filter_by(buyer_id=current_user.id).all()
    elif current_user.is_farmer():
        contracts = B2BContract.query.filter_by(farmer_id=current_user.id).all()
    else:
        contracts = B2BContract.query.all()
    
    return render_template('b2b/contracts.html', contracts=contracts)


@b2b_bp.route('/request', methods=['GET', 'POST'])
@login_required
def request_contract():
    """Request bulk order contract"""
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        product = Product.query.get_or_404(product_id)
        
        contract = B2BContract(
            buyer_id=current_user.id,
            farmer_id=product.farmer_id,
            product_id=product_id,
            agreed_price_per_unit=float(request.form.get('price')),
            total_volume=float(request.form.get('volume')),
            unit=product.unit,
            start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date(),
            end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date(),
            delivery_schedule=request.form.get('schedule')
        )
        
        db.session.add(contract)
        db.session.commit()
        
        # Notify farmer
        Notification.create_notification(
            user_id=product.farmer_id,
            type='order',
            title='New B2B Contract Request',
            message=f'{current_user.name} requested a bulk order contract',
            action_url=url_for('b2b.contracts')
        )
        
        flash('Contract request submitted!', 'success')
        return redirect(url_for('b2b.contracts'))
    
    products = Product.query.filter_by(is_bulk_available=True, is_active=True).all()
    return render_template('b2b/request.html', products=products)


@b2b_bp.route('/contracts/<int:id>/activate', methods=['POST'])
@login_required
def activate_contract(id):
    """Activate contract"""
    contract = B2BContract.query.get_or_404(id)
    
    if contract.farmer_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('b2b.contracts'))
    
    advance = float(request.form.get('advance_paid', 0))
    contract.advance_paid = advance
    
    if contract.activate():
        db.session.commit()
        flash('Contract activated!', 'success')
    else:
        flash('Cannot activate contract', 'danger')
    
    return redirect(url_for('b2b.contracts'))
