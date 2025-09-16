import unittest
from app import create_app, db
from app.models import User
from app.config import TestingConfig
from app.auth.auth_utils import hash_password, verify_password

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()

        # 创建数据库表
        db.create_all()

        # Create a test user
        self.user = User(username='testuser', email='test@example.com', password_hash=hash_password('password'))
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Tear down all initialized variables."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration(self):
        """Test user registration."""
        response = self.client().post('/auth/register', data=dict(
            username='newuser', email='new@example.com', password='newpassword', confirm='newpassword'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn('注册成功！请登录。', str(response.data))

    def test_user_login(self):
        """Test user login."""
        response = self.client().post('/auth/login', data=dict(
            email='test@example.com', password='password'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn('登录成功！', str(response.data))

if __name__ == "__main__":
    unittest.main()
