import os

from dotenv import load_dotenv

load_dotenv()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mailman import Mail
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.update(
        # ================= SECURITY =================
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "dev-jwt"),

        # ================= DB =================
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,

        # ================= MAIL =================
        MAIL_SERVER='smtp.sendgrid.net',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
    )

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # ================================
    # ✅ FIXED CORS (IMPORTANT)
    # ================================
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "*"
            }
        },
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"]
    )

    # ================================
    # REGISTER BLUEPRINTS
    # ================================
    from app.routes.auth import auth_bp
    from app.routes.stores import stores_bp
    from app.routes.products import products_bp
    from app.routes.inventory import inventory_bp
    from app.routes.supply_requests import supply_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(stores_bp, url_prefix='/api/stores')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(supply_bp, url_prefix='/api/supply-requests')

    return app