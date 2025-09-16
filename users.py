from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:yourpassword@localhost/nano'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 用户表
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    files = db.relationship('UserFile', backref='user', lazy=True)
    visualizations = db.relationship('Visualization', backref='user', lazy=True)
    histories = db.relationship('UserHistory', backref='user', lazy=True)
    ai_responses = db.relationship('UserAIResponse', backref='user', lazy=True)

# 用户文件表
class UserFile(db.Model):
    __tablename__ = 'user_files'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))
    uploaded_at = db.Column(db.DateTime)
    description = db.Column(db.Text)

    extracted_data = db.relationship('ExtractedData', backref='file', lazy=True)
    visualization_data_files = db.relationship('VisualizationDataFile', backref='file', lazy=True)

# 提取数据表
class ExtractedData(db.Model):
    __tablename__ = 'extracted_data'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('user_files.id'), nullable=False)
    data_name = db.Column(db.String(255))
    data_type = db.Column(db.String(50))
    data_content = db.Column(db.Text)
    extracted_at = db.Column(db.DateTime)

    visualization_data_files = db.relationship('VisualizationDataFile', backref='extracted_data', lazy=True)

# 可视化表
class Visualization(db.Model):
    __tablename__ = 'visualizations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    image_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)

    visualization_data_files = db.relationship('VisualizationDataFile', backref='visualization', lazy=True)

# 可视化数据文件关联表
class VisualizationDataFile(db.Model):
    __tablename__ = 'visualization_data_files'
    id = db.Column(db.Integer, primary_key=True)
    visualization_id = db.Column(db.Integer, db.ForeignKey('visualizations.id'), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('user_files.id'), nullable=False)
    extracted_data_id = db.Column(db.Integer, db.ForeignKey('extracted_data.id'))
    used_at = db.Column(db.DateTime)

# 用户历史操作表
class UserHistory(db.Model):
    __tablename__ = 'user_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)

# 大模型回复信息表
class UserAIResponse(db.Model):
    __tablename__ = 'user_ai_responses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)

# 如果需要初始化数据库（只需运行一次）
# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
