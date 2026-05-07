
from flask import Flask
from app.models import db
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'carwash-secret-key' # Should be in .env later
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carwash.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    with app.app_context():
        db.create_all()
        
    # Register blueprints
    from app.api.routes import api_bp
    from app.api.auth import auth_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app
