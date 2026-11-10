from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db_session
from models import User

auth_bp = Blueprint('auth', __name__)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this system.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return db_session.get(User, int(user_id))

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('Access restricted. Admin permissions are required for this action.', 'danger')
            return redirect(url_for('faculty.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def faculty_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_faculty() and not current_user.is_admin():
            flash('Access restricted to faculty members only.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('faculty.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = db_session.query(User).filter_by(username=username).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash('This account has been deactivated. Please contact the administrator.', 'danger')
                return render_template('login.html')

            login_user(user)
            flash(f'Welcome back, {user.full_name}!', 'success')

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)

            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('faculty.dashboard'))
        else:
            flash('Invalid username or password. Please check your credentials.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
