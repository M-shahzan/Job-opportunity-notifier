from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        full_name = request.form["full_name"]
        role = request.form["role"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for("auth.signup"))

        # Hash the password
        new_user = User(
            email=email,
            full_name=full_name,
            role=role,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        # Automatically log in the user
        login_user(new_user)

        # Redirect based on role
        if role == "seeker":
            return redirect(url_for("seeker.preferences", user_id=new_user.id))
        else:
            return "Employer dashboard (to be implemented)"

    return render_template("signup.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if user.role == "seeker":
                return redirect(url_for("home"))
            return "Employer dashboard (to be implemented)"
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
