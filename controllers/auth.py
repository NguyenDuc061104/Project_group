from flask import request, jsonify
from flask_login import login_user, current_user,logout_user
from sqlalchemy.exc import IntegrityError
from models.user import User
from extensions import db
from flask import Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')
#register function
@auth_bp.route('/register', methods=['POST'])
def register():
    # Lấy dữ liệu từ form-data hoặc JSON
    data = request.get_json() or request.form

    username = data.get('username', '').strip()
    email    = data.get('email', '').strip().lower()
    password = data.get('password', '')
    confirm  = data.get('confirm_password', '')

    # Kiểm tra dữ liệu đầu vào
    if not username or not email or not password:
        return jsonify({'error': 'Thiếu thông tin bắt buộc'}), 400

    if password != confirm:
        return jsonify({'error': 'Mật khẩu và xác nhận không khớp'}), 400

    # Kiểm tra username hoặc email đã tồn tại
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'Username hoặc Email đã tồn tại'}), 409

    # Tạo và lưu user
    try:
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'message': 'Đăng ký thành công',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Dữ liệu đã tồn tại hoặc lỗi cơ sở dữ liệu'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Đăng ký thất bại: {str(e)}'}), 500
    
#login function
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or request.form

    email    = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Vui lòng nhập đầy đủ email và mật khẩu'}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(
            identity=str(user.id),  # identity là id của user
            additional_claims={
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin
        }, expires_delta=timedelta(hours=1))

        return jsonify({
            'message': 'Đăng nhập thành công',
            'access_token': access_token
        }), 200

    return jsonify({'error': 'Sai email hoặc mật khẩu'}), 401

#logout function
@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Với JWT, logout phía server chỉ mang tính tượng trưng
    return jsonify({'message': 'Đăng xuất thành công. Hãy xóa token ở phía client'}), 200