from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from extensions import db
from models import User, Professional, Service
import os

auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            if user.is_blocked:
                flash(
                    "Your account has been blocked. Please contact the administrator."
                )
                return redirect(url_for("auth.login"))
            login_user(user)
            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))
            elif user.role == "professional":
                return redirect(url_for("professional.dashboard"))
            else:
                return redirect(url_for("customer.dashboard"))
        else:
            flash("Invalid username or password")
    return render_template("login.html")


@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        address = request.form.get("address")
        pin_code = request.form.get("pin_code")

        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists")
        else:
            hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                role=role,
                address=address,
                pin_code=pin_code,
            )
            db.session.add(new_user)
            db.session.commit()

            if role == "professional":
                service_id = request.form.get("service_type")
                experience = request.form.get("experience")
                documents = request.files.getlist("documents")

                professional = Professional(
                    user_id=new_user.id, service_id=service_id, experience=experience
                )
                db.session.add(professional)
                db.session.commit()

                # Handle document uploads
                if documents:
                    upload_folder = os.path.join("static", "uploads", str(new_user.id))
                    os.makedirs(upload_folder, exist_ok=True)
                    document_paths = []
                    for document in documents:
                        if document.filename != "":
                            filename = secure_filename(document.filename)
                            file_path = os.path.join(upload_folder, filename)
                            document.save(file_path)
                            document_paths.append(filename)

                    # Save document paths to the database
                    professional.documents = ",".join(document_paths)
                    db.session.commit()

            flash("Registration successful. Please log in.")
            return redirect(url_for("auth.login"))

    services = Service.query.all()
    return render_template("register.html", services=services)


@auth_routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth_routes.route("/register_admin", methods=["GET", "POST"])
@login_required
def register_admin():
    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        address = request.form.get("address")
        pin_code = request.form.get("pin_code")

        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists")
        else:
            hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
            new_admin = User(
                username=username,
                email=email,
                password=hashed_password,
                role="admin",
                address=address,
                pin_code=pin_code,
            )
            db.session.add(new_admin)
            db.session.commit()
            flash("Admin registration successful.")
            return redirect(url_for("admin.dashboard"))
    return render_template("register_admin.html")
