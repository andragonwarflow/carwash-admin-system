
import unittest
from app.models import db, User
from app.repositories.user_repository import UserRepository
from flask import Flask

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            self.repo = UserRepository()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        with self.app.app_context():
            user = self.repo.create("admin", "password123")
            self.assertIsNotNone(user.id)
            self.assertEqual(user.username, "admin")
            # Password should be hashed, not plain text
            self.assertNotEqual(user.password, "password123")

    def test_authenticate_user(self):
        with self.app.app_context():
            self.repo.create("admin", "password123")
            
            # Correct password
            user = self.repo.authenticate("admin", "password123")
            self.assertIsNotNone(user)
            
            # Wrong password
            user_fail = self.repo.authenticate("admin", "wrong_pass")
            self.assertIsNone(user_fail)

if __name__ == '__main__':
    unittest.main()
