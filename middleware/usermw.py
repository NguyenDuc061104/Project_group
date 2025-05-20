from flask import Blueprint
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from flask import request, jsonify
admin_auth = Blueprint('admin_auth', __name__, template_folder='../templates/auth')
from functools import wraps


@admin_auth.route('/me', methods=['GET'])
@jwt_required()
def get_user_info():
    identity = get_jwt_identity()  # id
    claims = get_jwt()  # thêm hàm này để lấy dữ liệu bổ sung

    return jsonify({
        'id': identity,
        'username': claims.get('username'),
        'email': claims.get('email'),
        'is_admin': claims.get('is_admin')
    }), 200

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return jsonify({'error': 'Bạn không có quyền truy cập'}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_auth.route('/admin-only', methods=['GET'])
@jwt_required()
@admin_required
def admin_route():
    return jsonify({'message': 'Chào admin!'}), 200
