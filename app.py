from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from extensions import db
from models.user import User
from flask_jwt_extended import JWTManager, get_jwt
from controllers.teddy import teddy_bp
from middleware.usermw import admin_auth
from controllers.auth import auth_bp
from controllers.order import order_bp
from controllers.order_items import order_item_bp

migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # đổi key thật kỹ

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)


    # app.config['JWT_IDENTITY_CLAIM'] = 'sub'
    # app.config['JWT_JSON_KEY'] = 'identity'
    app.register_blueprint(admin_auth, url_prefix='/admin_auth') 
    app.register_blueprint(auth_bp, url_prefix='/auth') 
    app.register_blueprint(teddy_bp, url_prefix='/teddy')
    app.register_blueprint(order_bp, url_prefix='/order')
    app.register_blueprint(order_item_bp,url_prefix='/order_item')


    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # import models để SQLAlchemy biết
        from models.user       import User
        from models.teddy      import Teddy
        from models.order      import Order
        from models.order_items import OrderItem
        db.create_all()
        print("✅ Tables created.")
    app.run(debug=True)
