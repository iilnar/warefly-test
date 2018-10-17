from flask import Blueprint, session, request, render_template, flash, redirect, g, url_for
from wtforms import Form, StringField, PasswordField, validators
from db import db_session
from models import User
from functools import wraps
from hashlib import sha256

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db_session.query(User).filter(User.id == user_id).first()


def auth_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)

    return wrapped_view


def password_hash(email, psw, salt='extra_salt'):
    return sha256('{}_{}_{}'.format(email, salt, psw)[::-1].encode('utf-8')).hexdigest()
    

class RegisterForm(Form):
    name = StringField('name', [validators.DataRequired(), validators.Length(min=2, max=20)])
    email = StringField('email', [validators.DataRequired(), validators.Length(min=2, max=20)])
    password = PasswordField('password', [validators.DataRequired(), validators.Length(min=2, max=20)])


@bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        has_error = False    

        if db_session.query(User).filter(User.email==form.email.data).count() != 0:
            flash('Email is already registered.', 'error')
            has_error = True
        
        if not has_error:
            psw_hash = password_hash(form.email.data, form.password.data)
            db_session.add(User(form.name.data, form.email.data, psw_hash))
            db_session.commit()
            user = db_session.query(User).filter(User.email==form.email.data).first()
            session['user_id'] = user.id

            return redirect(url_for('purchase.add'))

    return render_template('auth/register.html', form=form)


class LoginForm(Form):
    email = StringField('email', [validators.DataRequired(), validators.Length(min=2, max=20)])
    password = PasswordField('password', [validators.DataRequired(), validators.Length(min=2, max=20)])


@bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        has_error = False
        user = db_session.query(User).filter(User.email==form.email.data).first()

        if user is None:
            flash('No user with such email.', 'error')
            has_error = True
        else:
            psw_hash = password_hash(form.email.data, form.password.data)
            if user.password != psw_hash:
                flash('Wrong password', 'error')
                has_error = True
        
        if not has_error:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('purchase.add'))
    return render_template('auth/login.html', form=form)


@bp.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
