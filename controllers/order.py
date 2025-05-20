from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.order import Order
from models.order_items import OrderItem
from models.user import User
from extensions import db
from datetime import datetime
from models.teddy import Teddy 

order_bp = Blueprint('order', __name__, url_prefix='/order')


# 🛒 Tạo đơn hàng mới
from models.teddy import Teddy  # 👈 Nhớ import nếu chưa có

@order_bp.route('/create', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        new_order = Order(
            user_id=user_id,
            created_at=datetime.utcnow(),
            status='pending'
        )
        db.session.add(new_order)
        db.session.flush()  # Lấy new_order.id ngay

        # Thêm từng item
        for item in data.get('items', []):
            teddy = Teddy.query.get(item['teddy_id'])
            if not teddy:
                raise Exception(f"Teddy ID {item['teddy_id']} không tồn tại")

            order_item = OrderItem(
                order_id=new_order.id,
                teddy_id=item['teddy_id'],
                quantity=item['quantity'],
                price=teddy.price  # 👈 Lấy giá từ DB
            )
            db.session.add(order_item)

        db.session.commit()
        return jsonify({'message': 'Đơn hàng đã được tạo', 'order_id': new_order.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400



# 📋 Lấy tất cả đơn của user hiện tại
@order_bp.route('/get_all', methods=['GET'])
@jwt_required()
def get_user_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()

    result = []
    for o in orders:
        result.append({
            'id': o.id,
            'created_at': o.created_at.isoformat(),
            'status': o.status,
            'items': [{'teddy_id': i.teddy_id, 'quantity': i.quantity} for i in o.items]
        })

    return jsonify(result), 200


# 🔍 Lấy chi tiết đơn theo ID
@order_bp.route('/getdetails', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.get_or_404(order_id)

    if order.user_id != user_id:
        return jsonify({'error': 'Không có quyền truy cập đơn này'}), 403

    result = {
        'id': order.id,
        'created_at': order.created_at.isoformat(),
        'status': order.status,
        'items': [{'teddy_id': i.teddy_id, 'quantity': i.quantity} for i in order.items]
    }

    return jsonify(result), 200


# ❌ Xoá đơn
@order_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.get_or_404(order_id)

    if order.user_id != user_id:
        return jsonify({'error': 'Không thể xoá đơn của người khác'}), 403

    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Đã xoá đơn'}), 200
