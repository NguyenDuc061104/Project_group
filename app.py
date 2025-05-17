from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from extensions import db
from models.user import User


migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import models để Flask-Migrate thấy được
    # from models import teddy, user, order, order_items
    

    # Import và register các blueprint
    from controllers.auth import auth_bp
    from controllers.shop import shop_bp
    from controllers.cart import cart_bp
    from controllers.checkout import checkout_bp
    from controllers.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(shop_bp)
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(checkout_bp, url_prefix='/checkout')
    app.register_blueprint(admin_bp, url_prefix='/admin')

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
