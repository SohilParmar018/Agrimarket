"""
Authentication Routes
Handles registration, login, logout, and profile management
"""
import os
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.blueprints.auth import auth_bp
from app.blueprints.auth.forms import RegistrationForm, LoginForm, ProfileUpdateForm, PasswordChangeForm
from app.models.user import User
from app.models.notification import Notification
from app.extensions import db


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Create new user
        user = User(
            name=form.name.data,
            email=form.email.data,
            role=form.role.data,
            phone=form.phone.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            pincode=form.pincode.data
        )
        user.set_password(form.password.data)
        
        # Buyers are auto-verified, farmers need admin approval
        if user.role == 'buyer':
            user.is_verified = True
        else:
            user.is_verified = False
        
        db.session.add(user)
        db.session.commit()
        
        # Create welcome notification
        Notification.create_notification(
            user_id=user.id,
            type='system',
            title='Welcome to AgriMarket!',
            message=f'Your account has been created successfully. {"Start exploring products!" if user.is_buyer() else "Your account is pending admin approval."}'
        )
        
        flash(f'Account created successfully! {"You can now login." if user.is_buyer() else "Your account is pending admin approval."}', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return _redirect_to_dashboard()
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('Your account has been deactivated. Please contact support.', 'warning')
            return redirect(url_for('auth.login'))
        
        if user.is_farmer() and not user.is_verified:
            flash('Your farmer account is pending admin approval.', 'warning')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome back, {user.name}!', 'success')
        
        # Redirect to next page or dashboard
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        
        return _redirect_to_dashboard()
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """View user profile"""
    return render_template('auth/profile.html', user=current_user)


@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    form = ProfileUpdateForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.pincode = form.pincode.data
        
        # Handle profile image upload
        if form.profile_image.data:
            file = form.profile_image.data
            filename = secure_filename(file.filename)
            # Add timestamp to filename to avoid conflicts
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{current_user.id}_{timestamp}_{filename}"
            
            upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            
            # Store relative path
            current_user.profile_image = f'uploads/profiles/{filename}'
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/edit_profile.html', form=form)


@auth_bp.route('/profile/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    form = PasswordChangeForm()
    
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('auth.change_password'))
        
        current_user.set_password(form.new_password.data)
        db.session.commit()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/change_password.html', form=form)


def _redirect_to_dashboard():
    """Redirect user to appropriate dashboard based on role"""
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    elif current_user.is_farmer():
        return redirect(url_for('farmer.dashboard'))
    else:  # buyer
        return redirect(url_for('buyer.dashboard'))
