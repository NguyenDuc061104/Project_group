from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from models.order import Order
from models.order_items import OrderItem
from flask_login import login_required, current_user
from datetime import datetime

# Tên biến này phải là checkout_bp để app.py import được
checkout_bp = Blueprint('checkout', __name__, template_folder='../templates')

@checkout_bp.route('/', methods=['GET'])
@login_required
def checkout():
    # Lấy giỏ hàng từ session
    cart = session.get('cart', {})
    if not cart:
        flash('Giỏ hàng trống!', 'warning')
        return redirect(url_for('shop.index'))

    # Tổng tiền
    total = 0
    for teddy_id, qty in cart.items():
        from models.teddy import Teddy
        teddy = Teddy.query.get(int(teddy_id))
        total += teddy.price * qty

    return render_template('checkout.html', cart_items=cart, total=total)

@checkout_bp.route('/', methods=['POST'])
@login_required
def process_checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Giỏ hàng trống!', 'warning')
        return redirect(url_for('shop.index'))

    # Tạo Order
    order = Order(user_id=current_user.id, created_at=datetime.utcnow(), status='pending')
    db.session.add(order)
    db.session.flush()  # để order.id có giá trị

    # Tạo OrderItem cho mỗi mục trong giỏ
    for teddy_id, qty in cart.items():
        from models.teddy import Teddy
        teddy = Teddy.query.get(int(teddy_id))
        item = OrderItem(
            order_id=order.id,
            teddy_id=teddy.id,
            quantity=qty,
            price=teddy.price
        )
        db.session.add(item)

    # Commit và xóa giỏ
    db.session.commit()
    session.pop('cart', None)
    flash('Đơn hàng của bạn đã được tạo!', 'success')
    return redirect(url_for('shop.index'))
