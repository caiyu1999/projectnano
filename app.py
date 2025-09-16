import os
from flask import Flask, request, redirect, url_for, flash, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# --- 初始化应用 ---
app = Flask(__name__, template_folder='front/templates', static_folder='front/static')

# --- 配置 ---
# !!! 重要: 请将下面的占位符替换为你的真实 MySQL 数据库信息 !!!
DB_USER = 'your_mysql_username'
DB_PASS = 'your_mysql_password'
DB_HOST = 'localhost'
DB_NAME = 'your_database_name'

app.config['SECRET_KEY'] = 'a_very_secret_key_that_should_be_changed'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- 初始化扩展 ---
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# --- 数据库模型 ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# --- 路由 ---
@app.route('/')
def home():
    if 'user_id' in session:
        # 登录后显示一个简单的欢迎页面
        return render_template('home.html', username=session.get('username'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('用户名和密码不能为空。')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('该用户名已被注册，请选择其他用户名。')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('注册成功！请登录。')
        return redirect(url_for('login'))

    # 我们需要创建一个 register.html 模板
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('登录成功！')
            return redirect(url_for('home'))
        else:
            flash('用户名或密码无效。')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('您已成功登出。')
    return redirect(url_for('login'))

# 文件上传页面，现在需要登录才能访问
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user_id' not in session:
        flash('请先登录！')
        return redirect(url_for('login'))
    
    # 这里保留了之前的文件上传逻辑，你可以根据需要进行修改或集成
    if request.method == 'POST':
        # ... (省略具体上传逻辑)
        flash('文件处理完成。')
        return redirect(request.url)

    return render_template('upload.html')


if __name__ == '__main__':
    with app.app_context():
        # 这会在应用启动时自动创建数据库表（如果表不存在）
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)
