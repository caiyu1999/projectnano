from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig

# 初始化 Flask 应用
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# 初始化数据库
db = SQLAlchemy(app)

# 测试数据库连接
try:
    with app.app_context():
        from sqlalchemy import text
        result = db.session.execute(text('SELECT 1')).fetchone()
        print("数据库连接成功！查询结果:", result)
except Exception as e:
    print("数据库连接失败:", e)
    
db.session.close()