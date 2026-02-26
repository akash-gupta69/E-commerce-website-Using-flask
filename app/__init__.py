from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from config import Config


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    login_manager.login_view = "auth.login"

    from app.models.user import User
    from app.models.product import Product
    from app.models.order import Order, OrderItem
    from app.models.cart import CartItem
    from app.models.wishlist import WishlistItem
    from app.models.review import Review
    from app.models.address import Address

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from app.auth import auth
    from app.shop import shop
    from app.admin import admin
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(shop)
    app.register_blueprint(admin, url_prefix='/admin')


    return app