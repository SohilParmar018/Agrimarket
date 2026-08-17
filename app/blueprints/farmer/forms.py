"""
Farmer Forms
Forms for product management
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, SelectField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional


class ProductForm(FlaskForm):
    """Product creation/edit form"""
    name = StringField('Product Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('grains', 'Grains'),
        ('pulses', 'Pulses'),
        ('spices', 'Spices'),
        ('dairy', 'Dairy'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    price_per_unit = FloatField('Price per Unit (₹)', validators=[
        DataRequired(),
        NumberRange(min=0.01)
    ])
    unit = SelectField('Unit', choices=[
        ('kg', 'Kilogram (kg)'),
        ('quintal', 'Quintal'),
        ('ton', 'Ton'),
        ('piece', 'Piece'),
        ('dozen', 'Dozen')
    ], validators=[DataRequired()])
    stock_qty = FloatField('Stock Quantity', validators=[
        DataRequired(),
        NumberRange(min=0)
    ])
    min_order_qty = FloatField('Minimum Order Quantity', validators=[
        DataRequired(),
        NumberRange(min=0.01)
    ])
    is_bulk_available = BooleanField('Available for Bulk Orders')
    bulk_price = FloatField('Bulk Price per Unit (₹)', validators=[Optional()])
    min_bulk_qty = FloatField('Minimum Bulk Quantity', validators=[Optional()])
    image = FileField('Product Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    is_active = BooleanField('Active', default=True)
