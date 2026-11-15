from functools import wraps
import re
from flask import Blueprint, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User

auth = Blueprint('auth', __name__)


def current_user():
    user_id = session.get('user_id')
    return db.session.get(User, user_id) if isinstance(user_id, int) else None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().casefold()
        password = request.form.get('password', '')
        if len(email) > 254 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email) or not 12 <= len(password) <= 128:
            return render_template('login.html', mode='register', error='Enter a valid email and a password of 12 to 128 characters.'), 400
        db.session.add(User(email=email, password=generate_password_hash(password)))
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('login.html', mode='register', error='An account with this email already exists.'), 409
        return redirect(url_for('auth.login'), code=303)
    return render_template('login.html', mode='register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().casefold()
        password = request.form.get('password', '')
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
        if user is None or not 1 <= len(password) <= 128 or not check_password_hash(user.password, password):
            return render_template('login.html', mode='login', error='Invalid email or password.'), 401
        session.clear()
        session['user_id'] = user.id
        return redirect(url_for('auth.dashboard'), code=303)
    return render_template('login.html', mode='login')


@auth.post('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('shop.index'), code=303)


@auth.get('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user())
