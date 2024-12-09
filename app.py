from flask import Flask, render_template
from flask_cors import CORS
from extensions import db, login_manager
from models import User
from werkzeug.security import generate_password_hash
import os


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["SECRET_KEY"] = "your-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///household_services.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
    app.config["UPLOAD_FOLDER"] = "static/uploads"
    app.config["ALLOWED_EXTENSIONS"] = {"pdf", "png", "jpg", "jpeg"}

    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Enable CORS
    CORS(app)

    # Create database tables
    with app.app_context():
        db.create_all()
        create_initial_admin()

    # Register blueprints
    from routes.auth_routes import auth_routes
    from routes.admin_routes import admin_routes
    from routes.customer_routes import customer_routes
    from routes.professional_routes import professional_routes

    app.register_blueprint(auth_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(customer_routes)
    app.register_blueprint(professional_routes)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    @app.errorhandler(413)
    def too_large(error):
        return "File is too large", 413

    return app


def create_initial_admin():
    admin = User.query.filter_by(role="admin").first()
    if not admin:
        hashed_password = generate_password_hash("admin123", method="pbkdf2:sha256")
        admin = User(
            username="admin",
            email="admin@example.com",
            password=hashed_password,
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()
        print("Initial admin user created.")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
