from extensions import db 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# models/user.py
class User(db.Model, UserMixin):
    id        = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(64),  unique=True, nullable=False)
    email     = db.Column(db.String(120), unique=True, nullable=False)
    password  = db.Column(db.String(128), nullable=False)   # lưu plain
    is_admin  = db.Column(db.Boolean, default=False)
    confirmed      = db.Column(db.Boolean, default=False)
    confirm_token  = db.Column(db.String(128))
    reset_token    = db.Column(db.String(128))  
    avatar_url     = db.Column(db.String(256))

    # KHÔNG hash nữa
    def set_password(self, pwd):
        self.password = pwd

    def check_password(self, pwd):
        return self.password == pwd
