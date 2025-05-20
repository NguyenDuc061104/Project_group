from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.order_items import OrderItem
from models.order import Order
from models.teddy import Teddy
from extensions import db

order_item_bp = Blueprint('order_item', __name__, url_prefix='/order_item')


# 🔍 GET - lấy tất cả OrderItem (admin dùng hoặc test)
@order_item_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_items():
    items = OrderItem.query.all()
    result = [{
        'id': i.id,
        'order_id': i.order_id,
        'teddy_id': i.teddy_id,
        'quantity': i.quantity,
        'price': i.price
    } for i in items]
    return jsonify(result), 200


# 🔍 GET theo ID
@order_item_bp.route('/<int:item_id>', methods=['GET'])
@jwt_required()
def get_item(item_id):
    item = OrderItem.query.get_or_404(item_id)
    return jsonify({
        'id': item.id,
        'order_id': item.order_id,
        'teddy_id': item.teddy_id,
        'quantity': item.quantity,
        'price': item.price
    }), 200


# ➕ POST - thêm item vào đơn hàng
@order_item_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    data = request.get_json()
    try:
        teddy = Teddy.query.get(data['teddy_id'])
        if not teddy:
            return jsonify({'error': 'Teddy không tồn tại'}), 404

        item = OrderItem(
            order_id=data['order_id'],
            teddy_id=data['teddy_id'],
            quantity=data.get('quantity', 1),
            price=teddy.price
        )
        db.session.add(item)
        db.session.commit()
        return jsonify({'message': 'Tạo thành công', 'id': item.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# ✏️ PUT - cập nhật item
@order_item_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    item = OrderItem.query.get_or_404(item_id)
    data = request.get_json()

    item.quantity = data.get('quantity', item.quantity)
    item.price = data.get('price', item.price)

    db.session.commit()
    return jsonify({'message': 'Cập nhật thành công'}), 200


# ❌ DELETE - xoá item
@order_item_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    item = OrderItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Đã xoá'}), 200
