from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .utils import is_admin, admin_required
from .models import db, User, UserTypes

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
        users = User.query.filter_by(userType = UserTypes.user).all()
        return render_template("admin.html", name=current_user.username, users = [x.username for x in users])
    return render_template("user.html", name=current_user.username)

@main.route("/users")
def get_users():
    users = User.query.filter_by(userType = UserTypes.user).all()
    print([x.username for x in users])
    return [x.username for x in users]