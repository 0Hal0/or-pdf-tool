from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .utils import is_admin, admin_required
from . import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/admin")
@admin_required()
def admin():
    return render_template("profile.html", name=current_user.username)

@main.route("/account")
@login_required
def profile():
    if is_admin(current_user):
        return render_template("admin.html", name=current_user.username)
    return render_template("user.html", name=current_user.username)