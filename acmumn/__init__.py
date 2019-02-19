from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_migrate import Migrate

from acmumn.config import Config
from acmumn.globals import assets, db, limiter, login_manager, mail
from acmumn.models import *

app = Flask(__name__)
app.config.from_object(Config())

Migrate(app, db)

assets.init_app(app)
limiter.init_app(app)
login_manager.init_app(app)
mail.init_app(app)
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Member.query.filter_by(id=user_id).first()

import acmumn.api as api
app.register_blueprint(api.blueprint, url_prefix="/api")

import acmumn.views as views
app.register_blueprint(views.blueprint)

