from flask import Flask

from acmumn.globals import assets, db, login_manager

app = Flask(__name__)

assets.init_app(app)
db.init_app(app)
login_manager.init_app(app)

import acmumn.api as api
app.register_blueprint(api.blueprint, url_prefix="/api")

import acmumn.views as views
app.register_blueprint(views.blueprint)
