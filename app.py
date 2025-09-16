import os
import logging
from datetime import datetime
from flask import Flask, request, redirect, url_for, flash, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from graph.state.state import GraphState

# --- 初始化应用 ---
app = Flask(__name__, template_folder='front/templates', static_folder='front/static')

# --- 日志配置 ---
logging.basicConfig(level=logging.DEBUG)

# --- 配置 ---
# !!! 重要: 请将下面的占位符替换为你的真实 MySQL 数据库信息 !!!
DB_USER = 'caiyu'
DB_PASS = '12345678'
DB_HOST = 'localhost'
DB_NAME = 'nano'

app.config['SECRET_KEY'] = 'a_very_secret_key_that_should_be_changed'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'front/uploads'

# --- 初始化扩展 ---
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# --- 数据库模型 ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # 主键
    username = db.Column(db.String(80), unique=True, nullable=False)# 用户名称
    password = db.Column(db.String(120), nullable=False) # 用户密码
    files = db.relationship('UploadedFile', backref='owner', lazy=True) # 上传的文件
    visualizations = db.relationship('DataVisualization', backref='owner', lazy=True) # 该用户创建的可视化

    def __repr__(self):
        return f'<User {self.username}>'

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False, unique=True)
    upload_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    requirements = db.Column(db.String(500), nullable=True)  # 用户需求
    template = db.Column(db.String(50), nullable=True)  # 用户选择的模板
    visualizations = db.relationship('DataVisualization', backref='source_file', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<UploadedFile {self.filename}>'

class DataVisualization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    config = db.Column(db.JSON, nullable=True)
    file_id = db.Column(db.Integer, db.ForeignKey('uploaded_file.id'), nullable=False) # 关联的文件 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<DataVisualization {self.name}>'

# --- 路由 ---
@app.route('/')
def home():
    app.logger.debug("访问主页路由 '/'")
    if 'user_id' in session:
        username = session.get('username')
        app.logger.debug(f"用户 '{username}' 已登录，渲染主页")
        # 登录后显示一个简单的欢迎页面
        return render_template('home.html', username=username)
    app.logger.debug("用户未登录，重定向到登录页面")
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    app.logger.debug(f"访问注册页面路由 '/register'，方法: {request.method}")
    if 'user_id' in session:
        app.logger.debug(f"用户 '{session.get('username')}' 已登录，重定向到主页")
        return redirect(url_for('home'))

    if request.method == 'POST':
        app.logger.debug("处理注册表单提交 (POST)")
        username = request.form.get('username')
        password = request.form.get('password')
        app.logger.debug(f"获取到注册用户名: '{username}'")

        if not username or not password:
            app.logger.warning("注册失败：用户名或密码为空")
            flash('用户名和密码不能为空。')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            app.logger.warning(f"注册失败：用户名 '{username}' 已存在")
            flash('该用户名已被注册，请选择其他用户名。')
            return redirect(url_for('register'))

        app.logger.debug(f"用户名 '{username}' 可用，正在创建新用户")
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        app.logger.info(f"新用户 '{username}' 创建成功并已存入数据库")

        flash('注册成功！请登录。')
        return redirect(url_for('login'))

    app.logger.debug("渲染注册页面 (GET)")
    # 我们需要创建一个 register.html 模板
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.debug(f"访问登录页面路由 '/login'，方法: {request.method}")
    if 'user_id' in session:
        app.logger.debug(f"用户 '{session.get('username')}' 已登录，重定向到主页")
        return redirect(url_for('home'))

    if request.method == 'POST':
        app.logger.debug("处理登录表单提交 (POST)")
        username = request.form.get('username')
        password = request.form.get('password')
        app.logger.debug(f"尝试为用户 '{username}' 登录")

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            app.logger.info(f"用户 '{username}' 登录成功")
            flash('登录成功！')
            return redirect(url_for('home'))
        else:
            app.logger.warning(f"用户 '{username}' 登录失败：用户名或密码无效")
            flash('用户名或密码无效。')
            return redirect(url_for('login'))

    app.logger.debug("渲染登录页面 (GET)")
    return render_template('login.html')

@app.route('/logout')
def logout():
    username = session.get('username', '未知用户')
    app.logger.debug(f"访问登出路由 '/logout'，用户: '{username}'")
    session.clear()
    app.logger.info(f"用户 '{username}' 已清除 session 并登出")
    flash('您已成功登出。')
    return redirect(url_for('login'))

# 文件上传页面，现在需要登录才能访问
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    app.logger.debug(f"访问上传页面路由 '/upload'，方法: {request.method}")
    if 'user_id' not in session:
        app.logger.warning("未登录用户尝试访问上传页面，重定向到登录")
        flash('请先登录！')
        return redirect(url_for('login'))
    
    username = session.get('username')
    app.logger.debug(f"用户 '{username}' 已登录，访问上传页面")
    
    # 初始化 GraphState 并传递用户信息
    state = GraphState.from_flask_session(session)
    
    # 这里保留了之前的文件上传逻辑，你可以根据需要进行修改或集成
    if request.method == 'POST':
        app.logger.debug(f"用户 '{username}' 正在上传文件")
        if 'files[]' not in request.files:
            app.logger.warning(f"用户 '{username}' 的上传请求中没有文件部分")
            flash('请求中没有文件部分')
            return redirect(request.url)

        # 获取用户需求和模板选择
        requirements = request.form.get('requirements', '')
        template = request.form.get('template', '')
        app.logger.debug(f"用户 '{username}' 的需求: '{requirements}'，模板选择: '{template}'")

        files = request.files.getlist('files[]')
        uploaded_count = 0
        for file in files:
            if file.filename == '':
                app.logger.debug("收到一个没有文件名的空文件部分，已跳过")
                continue
            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # 检查文件是否已存在，如果存在则添加后缀以避免覆盖
                counter = 1
                original_filepath = filepath
                while os.path.exists(filepath):
                    name, ext = os.path.splitext(original_filepath)
                    filepath = f"{name}_{counter}{ext}"
                    counter += 1
                
                file.save(filepath)
                app.logger.info(f"文件 '{filename}' 已保存到 '{filepath}'")

                # 将文件信息存入数据库
                new_file = UploadedFile(
                    filename=filename,
                    filepath=filepath,
                    requirements=requirements,
                    template=template,
                    user_id=session['user_id']
                )
                db.session.add(new_file)
                uploaded_count += 1
        
        if uploaded_count > 0:
            db.session.commit()
            app.logger.info(f"为用户 '{username}' 在数据库中创建了 {uploaded_count} 个文件记录")
            flash(f'成功上传 {uploaded_count} 个文件！')
        else:
            flash('没有选择任何有效文件进行上传。')
            
        return redirect(request.url)

    app.logger.debug(f"为用户 '{username}' 渲染上传页面 (GET)")
    return render_template('upload.html')


if __name__ == '__main__':
    with app.app_context():
        app.logger.info("应用启动中... 检查并创建数据库表")
        # 这会在应用启动时自动创建数据库表（如果表不存在）
        db.create_all()
        app.logger.info("数据库表检查/创建完成")
    app.logger.info("启动 Flask 开发服务器，地址为 http://0.0.0.0:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
