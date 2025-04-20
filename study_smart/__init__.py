from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from study_smart.models import User

    login_manager.login_view = 'auth.login'  # Redirect if not logged in
    login_manager.login_message_category = 'info'  # Flash message style

    from study_smart.auth import auth
    from study_smart.views import views
    app.register_blueprint(auth)
    app.register_blueprint(views)

    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return app

@login_manager.user_loader
def load_user(user_id):
    from study_smart.models import User
    return User.query.get(int(user_id))
