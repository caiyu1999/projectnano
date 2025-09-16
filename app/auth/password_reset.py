from flask import url_for, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from ..models import User
from .. import db

def generate_reset_token(user_id, expires_sec=1800):
    s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': user_id}).decode('utf-8')

def verify_reset_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    return User.query.get(user_id)