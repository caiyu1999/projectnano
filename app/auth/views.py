from flask import render_template, redirect, url_for, flash, request, jsonify, session
from .auth_utils import hash_password, verify_password
from . import auth
from .forms import RegistrationForm, LoginForm
from ..models import User
from .. import db

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.password_hash = hash_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！请登录。', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and verify_password(user.password_hash, form.password.data):
            flash('登录成功！', 'success')
            return redirect(url_for('main.home'))
        flash('邮箱或密码错误。', 'danger')
    return render_template('auth/login.html', form=form)
