import os
from flask import Flask, redirect, url_for
from flask_login import current_user
from config import Config
from database import init_db, db_session
from auth import auth_bp, login_manager
from routes.admin_routes import admin_bp
from routes.faculty_routes import faculty_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(faculty_bp)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.is_admin():
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('faculty.dashboard'))
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    # Initialize database tables and seed accounts
    init_db()
    
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    print(f"\n=======================================================")
    print(f"🚀 Student Record Management System is starting...")
    print(f"📍 Web Interface: http://127.0.0.1:{port}")
    print(f"🔑 Admin Login: admin / Admin@12345")
    print(f"🔑 Faculty Logins: faculty.cs, faculty.math, faculty.ai (Password: Faculty@123)")
    print(f"=======================================================\n")
    app.run(host='0.0.0.0', port=port, debug=True)
