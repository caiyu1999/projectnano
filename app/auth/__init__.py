# 初始化认证模块
from flask import Blueprint
from ..models import User
from flask_login import LoginManager

auth = Blueprint('auth', __name__)

from . import views, forms

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))