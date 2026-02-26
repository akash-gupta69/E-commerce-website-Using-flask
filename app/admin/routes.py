from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from app.admin import admin
from app.models.product import Product
from app.models.order import Order
from app.models.user import User
from app import db
from flask_login import login_required, current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin.route("/dashboard")
@login_required
@admin_required
def dashboard():
    products_count = Product.query.count()
    orders_count = Order.query.count()
    users_count = User.query.count()
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(5).all()
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template('admin/dashboard.html', 
                           products_count=products_count, 
                           orders_count=orders_count,
                           users_count=users_count,
                           recent_orders=recent_orders,
                           products=products)

@admin.route("/product/new", methods=['GET', 'POST'])
@login_required
@admin_required
def new_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        stock = int(request.form.get('stock'))
        image_url = request.form.get('image_url', '').strip() or None
        
        product = Product(name=name, description=description, price=price, 
                          category=category, stock=stock, image_url=image_url)
        db.session.add(product)
        db.session.commit()
        flash('Product has been created!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/new_product.html', title='New Product')

@admin.route("/product/edit/<int:product_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.category = request.form.get('category')
        product.stock = int(request.form.get('stock'))
        product.image_url = request.form.get('image_url', '').strip() or None
        db.session.commit()
        flash(f'{product.name} updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_product.html', product=product, title='Edit Product')

@admin.route("/product/delete/<int:product_id>", methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    name = product.name
    db.session.delete(product)
    db.session.commit()
    flash(f'{name} has been deleted.', 'info')
    return redirect(url_for('admin.dashboard'))

@admin.route("/order/<int:order_id>/status", methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status', 'Pending')
    order.status = new_status
    db.session.commit()
    flash(f'Order #{order.id} status updated to {new_status}.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.errorhandler(403)
def forbidden(e):
    return render_template('admin/forbidden.html'), 403
