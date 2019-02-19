import flask_assets
import flask_limiter
import flask_login
import flask_mail
import flask_sqlalchemy

assets = flask_assets.Environment()
db = flask_sqlalchemy.SQLAlchemy()
limiter = flask_limiter.Limiter()
login_manager = flask_login.LoginManager()
mail = flask_mail.Mail()

