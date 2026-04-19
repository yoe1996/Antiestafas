from flask import Blueprint, render_template, request, redirect
from models import db, User
from flask_login import login_user, logout_user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect("/dashboard")
    return render_template("login.html")

@auth.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        hashed = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        user = User(username=request.form["username"], email=request.form["email"], password=hashed)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@auth.route("/logout")
def logout():
    logout_user()
    return redirect("/login")
