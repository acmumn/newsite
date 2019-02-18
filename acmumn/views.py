from flask import Blueprint, render_template

blueprint = Blueprint(__name__, "base")

@blueprint.route("/")
def index():
    return render_template("index.html")
