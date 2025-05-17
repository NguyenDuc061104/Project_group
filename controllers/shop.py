from flask import Blueprint, render_template, request, url_for, redirect
from app import db
from models.teddy import Teddy

# Tên biến này phải khớp với import ở app.py:
shop_bp = Blueprint('shop', __name__, template_folder='../templates/shop')

@shop_bp.route('/')
def index():
    teddies = Teddy.query.all()
    return render_template('shop/list.html', teddies=teddies)

@shop_bp.route('/teddy/<int:teddy_id>')
def detail(teddy_id):
    teddy = Teddy.query.get_or_404(teddy_id)
    return render_template('shop/detail.html', teddy=teddy)

# Bạn có thể thêm các route CRUD nếu cần:
@shop_bp.route('/admin/teddy/new', methods=['GET', 'POST'])
def create_teddy():
    # xử lý form tạo mới…
    return render_template('shop/create.html')
