import secrets

from flask import Blueprint, render_template, redirect, url_for, abort
from flask_wtf import FlaskForm
from flask_mail import Message
from flask_login import login_user, logout_user
from flask_limiter.util import get_remote_address
from sqlalchemy import func
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Email

from acmumn.globals import limiter, mail, db
from acmumn.models import Member, LoginToken

blueprint = Blueprint(__name__, "base")

@blueprint.route("/")
def index():
    return render_template("index.html")

@blueprint.route("/events")
def events():
    return render_template("events.html", title="Events")

@blueprint.route("/officers")
def officers():
    from acmumn.models import Member, Role
    officer_role = Role.query.filter_by(name="Officer").first()
    if officer_role is None:
        raise Exception("officer role doesn't exist")
    return render_template("officers.html", title="Officers", officers=officer_role.members)

class LoginForm(FlaskForm):
    email = StringField("email", validators=[Email()])
    submit = SubmitField()

@blueprint.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute", get_remote_address, methods=["POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        target_email = login_form.email.data.lower()
        member = Member.query.filter(func.lower(Member.email) == target_email).first()
        if member is not None:
            code = secrets.token_hex(64)
            token = LoginToken(code=code, member_id=member.id)
            db.session.add(token)
            db.session.commit()
            link = url_for("acmumn.views.verify_login", code=code, _external=True, _scheme="https")

            # TODO: offload sending to a task queue so it's not susceptible to timing attack
            message = Message("ACM UMN Login", sender="acm@umn.edu", recipients=[target_email])
            message.body = "Your sign in link is: " + link
            mail.send(message)
        return redirect(url_for("acmumn.views.login_sent"))
    return render_template("login.html", title="Login", login_form=login_form)

@blueprint.route("/login/verify/<code>")
def verify_login(code):
    token = LoginToken.query.filter_by(code=code).first()
    if token is None:
        return abort(404)
    login_user(token.user)
    db.session.delete(token)
    db.session.commit()
    return redirect(url_for("acmumn.views.index"))

@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("acmumn.views.index"))

@blueprint.route("/sent")
def login_sent():
    return render_template("login.html", title="Login", sent=True)

