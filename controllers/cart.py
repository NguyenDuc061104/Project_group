from flask import Blueprint, render_template, session, redirect, url_for, request
from app import db
from models.teddy import Teddy

# Biến này phải khớp với import trong app.py
cart_bp = Blueprint('cart', __name__, template_folder='../templates')

@cart_bp.route('/', methods=['GET'])
def view_cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for teddy_id, qty in cart.items():
        teddy = Teddy.query.get(int(teddy_id))
        if teddy:
            subtotal = teddy.price * qty
            items.append({'teddy': teddy, 'quantity': qty, 'subtotal': subtotal})
            total += subtotal
    return render_template('cart.html', cart_items=items, cart_total=total)

@cart_bp.route('/add/<int:teddy_id>', methods=['POST'])
def add_to_cart(teddy_id):
    cart = session.setdefault('cart', {})
    cart[str(teddy_id)] = cart.get(str(teddy_id), 0) + 1
    session.modified = True
    return redirect(url_for('shop.index'))

@cart_bp.route('/remove/<int:teddy_id>', methods=['POST'])
def remove_from_cart(teddy_id):
    cart = session.get('cart', {})
    cart.pop(str(teddy_id), None)
    session.modified = True
    return redirect(url_for('cart.view_cart'))
