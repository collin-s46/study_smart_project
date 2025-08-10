from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SUPABASE_DB_URL') #supabase db url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1) #new

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
