from flask import Blueprint, render_template, request, send_file
from flask_login import login_required, current_user
from .utils import is_admin, admin_required
from .models import User, UserTypes
from ReportTool import service_manager, ReportGenerator

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

@main.route("/services/<user>")
def get_services(user):
    try:
        return service_manager.get_services_for_user(user)["id"].astype(str).to_list()
    except ValueError:
        return []

@main.route("/services/<user>/add", methods = ["POST"] )
def add_services(user):
    service_manager.add_services_for_user(user, request.json["services"])
    return ""

@main.route("/report/<user>")
def generate_report(user):
    file_path = ReportGenerator.generate_user_report(False, False, False, user)
    return send_file(file_path, download_name=f"{user}-report.pdf", as_attachment=True)