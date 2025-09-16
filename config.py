class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:yourpassword@localhost/nano'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key-here'