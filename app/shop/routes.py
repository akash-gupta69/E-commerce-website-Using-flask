from flask import render_template, url_for, flash, redirect, request, Blueprint
from app.shop import shop
from app.models.product import Product
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.wishlist import WishlistItem
from app.models.review import Review
from app.models.address import Address
from app import db
from flask_login import login_required, current_user

@shop.route("/")
@shop.route("/home")
def home():
    products = Product.query.limit(8).all()
    return render_template('shop/home.html', products=products)

@shop.route("/category/<string:category_name>")
def category(category_name):
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(category=category_name)\
        .order_by(Product.created_at.desc())\
        .paginate(page=page, per_page=12)
    return render_template('shop/category.html', products=products, category_name=category_name)

@shop.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id)\
        .order_by(Review.created_at.desc()).all()
    avg_rating = 0
    if reviews:
        avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1)
    # Check if current user already reviewed
    user_review = None
    in_wishlist = False
    if current_user.is_authenticated:
        user_review = Review.query.filter_by(
            user_id=current_user.id, product_id=product_id).first()
        in_wishlist = WishlistItem.query.filter_by(
            user_id=current_user.id, product_id=product_id).first() is not None
    return render_template('shop/product_detail.html', product=product,
                           reviews=reviews, avg_rating=avg_rating,
                           user_review=user_review, in_wishlist=in_wishlist)

@shop.route("/search")
def search():
    query = request.args.get('q', '', type=str).strip()
    page = request.args.get('page', 1, type=int)
    if query:
        products = Product.query.filter(
            (Product.name.ilike(f'%{query}%')) | (Product.description.ilike(f'%{query}%'))
        ).paginate(page=page, per_page=12)
    else:
        products = Product.query.order_by(Product.created_at.desc()).paginate(page=page, per_page=12)
    return render_template('shop/search.html', products=products, query=query)

# ==================== CART ====================

@shop.route("/cart")
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    addresses = Address.query.filter_by(user_id=current_user.id).all()
    default_address = Address.query.filter_by(user_id=current_user.id, is_default=True).first()
    return render_template('shop/cart.html', cart_items=cart_items, total=total,
                           addresses=addresses, default_address=default_address)

@shop.route("/cart/add/<int:product_id>")
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product.id)
        db.session.add(cart_item)
    db.session.commit()
    flash(f'{product.name} added to cart!', 'success')
    return redirect(request.referrer or url_for('shop.cart'))

@shop.route("/cart/update/<int:item_id>", methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        return redirect(url_for('shop.cart'))
    quantity = int(request.form.get('quantity', 1))
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    db.session.commit()
    return redirect(url_for('shop.cart'))

@shop.route("/cart/remove/<int:item_id>")
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id == current_user.id:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart.', 'info')
    return redirect(url_for('shop.cart'))

# ==================== CHECKOUT ====================

@shop.route("/checkout", methods=['POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('shop.cart'))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    # Get shipping address
    address_id = request.form.get('address_id', type=int)
    shipping_text = None
    if address_id:
        address = Address.query.get(address_id)
        if address and address.user_id == current_user.id:
            shipping_text = address.formatted()
    
    order = Order(user_id=current_user.id, total_amount=total, shipping_address=shipping_text)
    db.session.add(order)
    db.session.flush()  # get order.id
    
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.session.add(order_item)
        # Reduce stock
        item.product.stock = max(0, item.product.stock - item.quantity)
        db.session.delete(item)
    
    db.session.commit()
    flash('Order placed successfully!', 'success')
    return redirect(url_for('shop.order_confirmation', order_id=order.id))

@shop.route("/order/<int:order_id>")
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return redirect(url_for('shop.home'))
    return render_template('shop/order_confirmation.html', order=order)

@shop.route("/orders")
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id)\
        .order_by(Order.order_date.desc()).all()
    return render_template('shop/orders.html', orders=orders)

# ==================== WISHLIST ====================

@shop.route("/wishlist")
@login_required
def wishlist():
    items = WishlistItem.query.filter_by(user_id=current_user.id)\
        .order_by(WishlistItem.added_at.desc()).all()
    return render_template('shop/wishlist.html', items=items)

@shop.route("/wishlist/add/<int:product_id>")
@login_required
def add_to_wishlist(product_id):
    product = Product.query.get_or_404(product_id)
    existing = WishlistItem.query.filter_by(
        user_id=current_user.id, product_id=product_id).first()
    if existing:
        flash(f'{product.name} is already in your wishlist.', 'info')
    else:
        item = WishlistItem(user_id=current_user.id, product_id=product_id)
        db.session.add(item)
        db.session.commit()
        flash(f'{product.name} added to wishlist!', 'success')
    return redirect(request.referrer or url_for('shop.wishlist'))

@shop.route("/wishlist/remove/<int:product_id>")
@login_required
def remove_from_wishlist(product_id):
    item = WishlistItem.query.filter_by(
        user_id=current_user.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Removed from wishlist.', 'info')
    return redirect(request.referrer or url_for('shop.wishlist'))

# ==================== REVIEWS ====================

@shop.route("/product/<int:product_id>/review", methods=['POST'])
@login_required
def submit_review(product_id):
    product = Product.query.get_or_404(product_id)
    existing = Review.query.filter_by(
        user_id=current_user.id, product_id=product_id).first()
    if existing:
        flash('You have already reviewed this product.', 'warning')
        return redirect(url_for('shop.product_detail', product_id=product_id))
    
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '').strip()
    
    if not rating or rating < 1 or rating > 5:
        flash('Please select a rating between 1 and 5.', 'danger')
        return redirect(url_for('shop.product_detail', product_id=product_id))
    
    review = Review(user_id=current_user.id, product_id=product_id,
                    rating=rating, comment=comment if comment else None)
    db.session.add(review)
    db.session.commit()
    flash('Review submitted!', 'success')
    return redirect(url_for('shop.product_detail', product_id=product_id))

@shop.route("/review/<int:review_id>/delete", methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        flash('You cannot delete this review.', 'danger')
        return redirect(url_for('shop.home'))
    product_id = review.product_id
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted.', 'info')
    return redirect(url_for('shop.product_detail', product_id=product_id))

# ==================== ADDRESSES ====================

@shop.route("/addresses")
@login_required
def addresses():
    user_addresses = Address.query.filter_by(user_id=current_user.id).all()
    return render_template('shop/addresses.html', addresses=user_addresses)

@shop.route("/address/add", methods=['POST'])
@login_required
def add_address():
    full_name = request.form.get('full_name', '').strip()
    phone = request.form.get('phone', '').strip()
    line1 = request.form.get('address_line1', '').strip()
    line2 = request.form.get('address_line2', '').strip()
    city = request.form.get('city', '').strip()
    state = request.form.get('state', '').strip()
    pincode = request.form.get('pincode', '').strip()
    
    if not all([full_name, phone, line1, city, state, pincode]):
        flash('Please fill in all required fields.', 'danger')
        return redirect(url_for('shop.addresses'))
    
    # If this is first address, make it default
    is_first = Address.query.filter_by(user_id=current_user.id).count() == 0
    
    addr = Address(user_id=current_user.id, full_name=full_name, phone=phone,
                   address_line1=line1, address_line2=line2 or None,
                   city=city, state=state, pincode=pincode,
                   is_default=is_first)
    db.session.add(addr)
    db.session.commit()
    flash('Address added successfully!', 'success')
    return redirect(url_for('shop.addresses'))

@shop.route("/address/edit/<int:address_id>", methods=['POST'])
@login_required
def edit_address(address_id):
    addr = Address.query.get_or_404(address_id)
    if addr.user_id != current_user.id:
        return redirect(url_for('shop.addresses'))
    
    addr.full_name = request.form.get('full_name', '').strip()
    addr.phone = request.form.get('phone', '').strip()
    addr.address_line1 = request.form.get('address_line1', '').strip()
    addr.address_line2 = request.form.get('address_line2', '').strip() or None
    addr.city = request.form.get('city', '').strip()
    addr.state = request.form.get('state', '').strip()
    addr.pincode = request.form.get('pincode', '').strip()
    
    db.session.commit()
    flash('Address updated!', 'success')
    return redirect(url_for('shop.addresses'))

@shop.route("/address/delete/<int:address_id>", methods=['POST'])
@login_required
def delete_address(address_id):
    addr = Address.query.get_or_404(address_id)
    if addr.user_id != current_user.id:
        return redirect(url_for('shop.addresses'))
    was_default = addr.is_default
    db.session.delete(addr)
    db.session.commit()
    # If deleted address was default, make the first remaining address default
    if was_default:
        first = Address.query.filter_by(user_id=current_user.id).first()
        if first:
            first.is_default = True
            db.session.commit()
    flash('Address deleted.', 'info')
    return redirect(url_for('shop.addresses'))

@shop.route("/address/<int:address_id>/default", methods=['POST'])
@login_required
def set_default_address(address_id):
    addr = Address.query.get_or_404(address_id)
    if addr.user_id != current_user.id:
        return redirect(url_for('shop.addresses'))
    # Remove default from all
    Address.query.filter_by(user_id=current_user.id).update({'is_default': False})
    addr.is_default = True
    db.session.commit()
    flash('Default address updated!', 'success')
    return redirect(url_for('shop.addresses'))
