from flask import Flask

from acmumn.globals import db, login_manager

app = Flask(__name__)

db.init_app(app)
login_manager.init_app(app)

import acmumn.views as views
app.register_blueprint(views.blueprint)
