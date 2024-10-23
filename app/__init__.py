from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from app.auth import auth_bp
    from app.leads import leads_bp
    from app.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(leads_bp)
    app.register_blueprint(dashboard_bp)
    
    return app