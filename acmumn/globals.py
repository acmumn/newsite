import flask_assets
import flask_login
import flask_sqlalchemy

assets = flask_assets.Environment()
db = flask_sqlalchemy.SQLAlchemy()
login_manager = flask_login.LoginManager()
