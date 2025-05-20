from flask import Blueprint, request, jsonify
from models.teddy import Teddy
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from middleware.usermw import admin_required

teddy_bp = Blueprint('teddy', __name__, url_prefix='/teddy')


# 🔍 GET /teddy - lấy danh sách tất cả sản phẩm
@teddy_bp.route('/get_teddy', methods=['GET'])
def get_all_teddies():
    teddies = Teddy.query.all()
    result = [{
        'id': t.id,
        'name': t.name,
        'description': t.description,
        'price': t.price,
        'stock': t.stock,
        'image_url': t.image_url
    } for t in teddies]
    return jsonify(result), 200


# 🔍 GET /teddy/<id> - lấy chi tiết sản phẩm
@teddy_bp.route('/get_detailteddy', methods=['GET'])
def get_teddy(teddy_id):
    teddy = Teddy.query.get_or_404(teddy_id)
    return jsonify({
        'id': teddy.id,
        'name': teddy.name,
        'description': teddy.description,
        'price': teddy.price,
        'stock': teddy.stock,
        'image_url': teddy.image_url
    }), 200


# ➕ POST /teddy - tạo mới (chỉ admin)
@teddy_bp.route('/create', methods=['POST'])
@jwt_required()
@admin_required
def create_teddy():
    data = request.get_json()

    try:
        teddy = Teddy(
            name=data['name'],
            description=data.get('description', ''),
            price=int(data['price']),
            stock=int(data.get('stock', 0)),
            image_url=data.get('image_url', '')
        )
        db.session.add(teddy)
        db.session.commit()
        return jsonify({'message': 'Tạo thành công', 'id': teddy.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Lỗi: {str(e)}'}), 400


# ✏️ PUT /teddy/<id> - cập nhật (chỉ admin)
@teddy_bp.route('/<int:teddy_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_teddy(teddy_id):
    teddy = Teddy.query.get_or_404(teddy_id)
    data = request.get_json()

    teddy.name = data.get('name', teddy.name)
    teddy.description = data.get('description', teddy.description)
    teddy.price = int(data.get('price', teddy.price))
    teddy.stock = int(data.get('stock', teddy.stock))
    teddy.image_url = data.get('image_url', teddy.image_url)

    try:
        db.session.commit()
        return jsonify({'message': 'Cập nhật thành công'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Lỗi: {str(e)}'}), 400


# ❌ DELETE /teddy/<id> - xoá (chỉ admin)
@teddy_bp.route('/<int:teddy_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_teddy(teddy_id):
    teddy = Teddy.query.get_or_404(teddy_id)
    db.session.delete(teddy)
    db.session.commit()
    return jsonify({'message': 'Xoá thành công'}), 200
