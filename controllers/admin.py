from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.user import User
from models.teddy import Teddy
from models.order import Order

admin_bp = Blueprint('admin', __name__, template_folder='templates/admin')

# Kiểm tra quyền admin
def admin_required(fn):
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash('Bạn không có quyền truy cập.', 'danger')
            return redirect(url_for('index'))
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@admin_bp.route('/')
@admin_required
def dashboard():
    users = User.query.count()
    teddies = Teddy.query.count()
    orders = Order.query.count()
    return render_template('admin/dashboard.html', users=users, teddies=teddies, orders=orders)

@admin_bp.route('/users')
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/teddies')
@admin_required
def manage_teddies():
    teddies = Teddy.query.all()
    return render_template('admin/manage_teddies.html', teddies=teddies)

@admin_bp.route('/orders')
@admin_required
def manage_orders():
    orders = Order.query.all()
    return render_template('admin/manage_orders.html', orders=orders)