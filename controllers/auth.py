from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from models.user import User
from flask_login import login_user, logout_user,current_user
# Đặt tên biến đúng với import ở app.py:
auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Nếu đã đăng nhập rồi thì chuyển thẳng về trang shop
    # if current_user.is_authenticated:
    #     return redirect(url_for('shop.index'))

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        email = request.form.get('email')
        password = request.form.get('password_hash')

        # Tìm user theo email
        user = User.query.filter_by(email=email).first()
        # Kiểm tra mật khẩu
        if user and user.check_password(password):
            login_user(user)
            # Xử lý redirect về trang gốc nếu có next
            next_page = request.args.get('next')
            return redirect(next_page or url_for('shop.index'))
        else:
            flash('Sai email hoặc mật khẩu', 'danger')

    # GET: render form login
    return render_template('login.html')
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # 1. Nếu đã login, chuyển sang shop
    if current_user.is_authenticated:
        return redirect(url_for('shop.index'))

    # 2. Xử lý POST
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        # 2.1. So khớp password
        if password != confirm:
            flash('Mật khẩu và xác nhận không khớp', 'warning')
            # phải return template nữa!
            return render_template('auth/register.html')

        # 2.2. Kiểm tra tồn tại
        exists = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if exists:
            flash('Username hoặc Email đã tồn tại', 'warning')
            return render_template('auth/register.html')

        # 2.3. Tạo user mới
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Đăng ký thành công, mời bạn đăng nhập', 'success')
        # quan trọng: phải return redirect chứ không chỉ flash
        return redirect(url_for('auth.login'))

    # 3. GET: trả về form đăng ký
    return render_template('auth/register.html')

from flask_login import login_required, logout_user, current_user
from flask import Blueprint, redirect, url_for, flash,request
@auth_bp.route('/logout', methods=['GET'])
@login_required              # <- thêm dòng này
def logout():
    username = current_user.username  # lúc này chắc chắn là User
    logout_user()                     # xoá session

    # Trả JSON nếu client yêu cầu, ngược lại redirect + flash
    if request.accept_mimetypes.accept_json:
        return flash({"message": f"Bye {username}! Logged out."}), 200

    flash(f"Bye {username}! Bạn đã đăng xuất.", "success")
    return redirect(url_for('shop.index'))
