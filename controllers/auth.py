# controllers/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import (
    login_user, logout_user, current_user,
    login_required
)
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask_mail import Message

from extensions import db   
from models.user import User

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

# -------------------------------------------------------------------
# -------------------------  LOGIN  ---------------------------------
# -------------------------------------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('shop.index'))

    if request.method == 'POST':
        email     = request.form.get('email', '').lower()
        password  = request.form.get('password', '')
        remember  = bool(request.form.get('remember'))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):            # plain-text compare
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('shop.index'))
        flash('Sai email hoặc mật khẩu', 'danger')

    return render_template('auth/login.html')

# -------------------------------------------------------------------
# ------------------------  REGISTER  -------------------------------
# -------------------------------------------------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('shop.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        if password != confirm:
            flash('Mật khẩu và xác nhận không khớp', 'warning')
            return render_template('auth/register.html')

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username hoặc Email đã tồn tại', 'warning')
            return render_template('auth/register.html')

        user = User(username=username, email=email)
        user.set_password(password)        # lưu plain-text
        db.session.add(user); db.session.commit()

        flash('Đăng ký thành công, mời bạn đăng nhập', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

# -------------------------------------------------------------------
# --------------------------  LOGOUT  -------------------------------
# -------------------------------------------------------------------
@auth_bp.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()

    # Nếu client yêu cầu JSON
    if request.accept_mimetypes.accept_json:
        return jsonify({"message": f"Bye {username}! Logged out."}), 200

    flash(f'Bye {username}! Bạn đã đăng xuất.', 'success')
    return redirect(url_for('shop.index'))

# -------------------------------------------------------------------
# --------------------- CHANGE PASSWORD -----------------------------
# -------------------------------------------------------------------
@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old = request.form.get('old_pwd', '')
        new = request.form.get('new_pwd', '')

        user = User.query.get(current_user.id)
        print("[DEBUG] current_user:", current_user.id)

        if not user.check_password(old):
            flash('Mật khẩu cũ sai', 'danger')
        elif len(new) < 6:
            flash('Mật khẩu phải ≥ 6 ký tự', 'warning')
        else:
            user.set_password(new)
            try:
                db.session.commit()
                print("[DEBUG] Password updated:", user.password)
                flash('Đổi mật khẩu thành công', 'success')
            except Exception as e:
                db.session.rollback()
                print("[ERROR]", e)
                flash("Có lỗi khi lưu mật khẩu", "danger")

            return redirect(url_for('shop.index'))

    return render_template('auth/change_password.html')


# -------------------------------------------------------------------
# --------------  FORGOT / RESET PASSWORD (EMAIL) -------------------
# -------------------------------------------------------------------
# s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
# TOKEN_EXP = 900  # 15 phút

# @auth_bp.route('/forgot-password', methods=['GET', 'POST'])
# def forgot_password():
#     if request.method == 'POST':
#         email = request.form['email'].lower()
#         user  = User.query.filter_by(email=email).first()
#         if user:
#             token = s.dumps(email, salt='reset')
#             user.reset_token = token
#             db.session.commit()

#             link = url_for('auth.reset_password', token=token, _external=True)
#             msg  = Message('Reset mật khẩu TeddyShop', recipients=[email],
#                            body=f'Click vào {link} trong 15 phút để đặt lại mật khẩu.')
#             mail.send(msg)
#         flash('Nếu email tồn tại, hướng dẫn reset đã được gửi.', 'info')
#     return render_template('auth/forgot_password.html')

# @auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     try:
#         email = s.loads(token, salt='reset', max_age=TOKEN_EXP)
#     except (SignatureExpired, BadSignature):
#         flash('Token không hợp lệ hoặc đã hết hạn', 'danger')
#         return redirect(url_for('auth.forgot_password'))

#     user = User.query.filter_by(email=email, reset_token=token).first_or_404()

#     if request.method == 'POST':
#         pwd = request.form['new_pwd']
#         user.set_password(pwd)      # plain-text
#         user.reset_token = None
#         db.session.commit()
#         flash('Đặt lại mật khẩu thành công, mời đăng nhập', 'success')
#         return redirect(url_for('auth.login'))
#     return render_template('auth/reset_password.html')

# # -------------------------------------------------------------------
# # ---------------  EMAIL CONFIRMATION AFTER REGISTER ----------------
# # -------------------------------------------------------------------
# def send_confirm_email(user):
#     token = s.dumps(user.email, salt='confirm')
#     user.confirm_token = token
#     db.session.commit()

#     link = url_for('auth.confirm_email', token=token, _external=True)
#     msg  = Message('Xác thực email TeddyShop', recipients=[user.email],
#                    body=f'Chào {user.username}, click {link} để kích hoạt tài khoản.')
#     mail.send(msg)

# @auth_bp.route('/confirm/<token>')
# def confirm_email(token):
#     try:
#         email = s.loads(token, salt='confirm', max_age=86400)  # 24 h
#     except (SignatureExpired, BadSignature):
#         flash('Token hết hạn hoặc sai', 'danger')
#         return redirect(url_for('auth.login'))

#     user = User.query.filter_by(email=email, confirm_token=token).first_or_404()
#     if not user.confirmed:
#         user.confirmed = True
#         user.confirm_token = None
#         db.session.commit()
#         flash('Xác thực thành công! Bạn có thể đăng nhập.', 'success')
#     else:
#         flash('Email đã xác thực!', 'info')
#     return redirect(url_for('auth.login'))
