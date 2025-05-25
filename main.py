from study_smart import create_app
from flask_migrate import Migrate
from study_smart.models import db

app = create_app()
migrate = Migrate(app, db)

#gunicorn handles app.run()