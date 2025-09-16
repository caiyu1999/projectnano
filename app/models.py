from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# # 创建 Flask 应用实例
# app = Flask(__name__)

# # 数据库配置
# # SQLALCHEMY_DATABASE_URI: 指定数据库连接的 URI，这里使用 MySQL 数据库，用户名为 root，密码为 yourpassword，数据库名为 nano
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:yourpassword@localhost/nano'
# # SQLALCHEMY_TRACK_MODIFICATIONS: 是否追踪对象的修改并发送信号，关闭可以节省资源
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 创建 SQLAlchemy 数据库对象
db = SQLAlchemy()

# 用户表模型
class User(db.Model, UserMixin):
    __tablename__ = 'users'  # 指定表名为 users
    id = db.Column(db.Integer, primary_key=True)  # 主键，自增
    username = db.Column(db.String(50), nullable=False)  # 用户名，最大长度50，不能为空
    email = db.Column(db.String(100), nullable=False)  # 邮箱，最大长度100，不能为空
    password_hash = db.Column(db.String(255), nullable=False)  # 密码哈希，最大长度255，不能为空
    created_at = db.Column(db.DateTime)  # 创建时间
    updated_at = db.Column(db.DateTime)  # 更新时间

    # 关系属性，关联用户的文件、可视化、历史记录、AI回复
    files = db.relationship('UserFile', backref='user', lazy=True)
    visualizations = db.relationship('Visualization', backref='user', lazy=True)
    histories = db.relationship('UserHistory', backref='user', lazy=True)
    ai_responses = db.relationship('UserAIResponse', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 用户文件表模型
class UserFile(db.Model):
    __tablename__ = 'user_files'  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 主键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 外键，关联 users 表的 id
    filename = db.Column(db.String(255), nullable=False)  # 文件名，最大长度255，不能为空
    file_path = db.Column(db.String(255), nullable=False)  # 文件路径，最大长度255，不能为空
    file_type = db.Column(db.String(50))  # 文件类型，最大长度50
    uploaded_at = db.Column(db.DateTime)  # 上传时间
    description = db.Column(db.Text)  # 文件描述

    # 关系属性，关联提取数据和可视化数据文件
    extracted_data = db.relationship('ExtractedData', backref='file', lazy=True)
    visualization_data_files = db.relationship('VisualizationDataFile', backref='file', lazy=True)

# 提取数据表模型
class ExtractedData(db.Model):
    __tablename__ = 'extracted_data'  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 主键
    file_id = db.Column(db.Integer, db.ForeignKey('user_files.id'), nullable=False)  # 外键，关联 user_files 表的 id
    data_name = db.Column(db.String(255))  # 数据名称，最大长度255
    data_type = db.Column(db.String(50))  # 数据类型，最大长度50
    data_content = db.Column(db.Text)  # 数据内容，文本类型
    extracted_at = db.Column(db.DateTime)  # 提取时间

    # 关系属性，关联可视化数据文件
    visualization_data_files = db.relationship('VisualizationDataFile', backref='extracted_data', lazy=True)

# 可视化表模型
class Visualization(db.Model):
    __tablename__ = 'visualizations'  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 主键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 外键，关联 users 表的 id
    title = db.Column(db.String(255))  # 可视化标题，最大长度255
    description = db.Column(db.Text)  # 可视化描述
    image_path = db.Column(db.String(255))  # 图片路径，最大长度255
    created_at = db.Column(db.DateTime)  # 创建时间

    # 关系属性，关联可视化数据文件
    visualization_data_files = db.relationship('VisualizationDataFile', backref='visualization', lazy=True)

# 可视化数据文件关联表模型
class VisualizationDataFile(db.Model):
    __tablename__ = 'visualization_data_files'  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 主键
    visualization_id = db.Column(db.Integer, db.ForeignKey('visualizations.id'), nullable=False)  # 外键，关联 visualizations 表的 id
    file_id = db.Column(db.Integer, db.ForeignKey('user_files.id'), nullable=False)  # 外键，关联 user_files 表的 id
    extracted_data_id = db.Column(db.Integer, db.ForeignKey('extracted_data.id'))  # 外键，关联 extracted_data 表的 id
    used_at = db.Column(db.DateTime)  # 使用时间

# 用户历史操作表模型
class UserHistory(db.Model):
    __tablename__ = 'user_history'  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 主键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 外键，关联 users 表的 id
    action = db.Column(db.String(255), nullable=False)  # 操作内容，最大长度255，不能为空
    created_at = db.Column(db.DateTime)  # 操作时间

# 大模型回复信息表模型
class UserAIResponse(db.Model):
    __tablename__ = 'user_ai_responses'  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 主键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 外键，关联 users 表的 id
    prompt = db.Column(db.Text, nullable=False)  # 用户提问内容，不能为空
    response = db.Column(db.Text, nullable=False)  # AI回复内容，不能为空
    created_at = db.Column(db.DateTime)  # 回复时间

# 如果需要初始化数据库（只需运行一次）
# with app.app_context():
#     db.create_all()

