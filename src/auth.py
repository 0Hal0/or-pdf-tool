from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, UserTypes, db

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again")
        return redirect(url_for("auth.login"))
    
    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))

@auth.route("/add/admin", methods=["POST"])
@login_required
def add_admin_post():
    #Authorization required here
    print("WTF")
    username = request.form.get("username")
    password = request.form.get("password")
    print(username)
    user = User.query.filter_by(username=username).first()

    if user:
        flash("This username already exists")
        return redirect(url_for("auth.add_admin"))

    new_user = User(username=username, password=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))

@auth.route("/add/admin")
@login_required
def add_admin():
    return render_template("signup.html")

@auth.route("/add/company")
@login_required
def add_user():
    return "Add company"

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))