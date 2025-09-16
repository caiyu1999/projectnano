import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)

    # 注册蓝图
    from .auth import auth
    app.register_blueprint(auth)

    return app