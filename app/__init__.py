from flask import Flask
from flask_login import LoginManager

from app.public import config

app = Flask (__name__)
from app.user import user as user_blueprint
from app.health import health as health_blueprint
from app.consultant import consultant as consultant_blueprint
from app.medical import medical as medicals_blueprint
app.register_blueprint (user_blueprint)
app.register_blueprint (health_blueprint)
app.register_blueprint (consultant_blueprint)
app.register_blueprint (medicals_blueprint)
from app.public.exts import db

db.init_app (app)
app.config.from_object (config)