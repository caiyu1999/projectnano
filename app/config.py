# Flask 应用配置
class Config:
    # 密钥配置
    SECRET_KEY = 'your-secret-key-here'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://caiyu:12345678@localhost/nano'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 文件上传配置
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'csv', 'json', 'xlsx'}

    # 调试模式
    DEBUG = True

# 其他环境配置（如生产环境、测试环境等）
class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
