
import unittest
from app.models import db, Customer
from app.repositories.customer_repository import CustomerRepository
from flask import Flask

class TestCustomerRepository(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            self.repo = CustomerRepository()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_customer(self):
        with self.app.app_context():
            customer = self.repo.create("John Doe", "12345678")
            self.assertIsNotNone(customer.id)
            self.assertEqual(customer.name, "John Doe")
            self.assertEqual(customer.phone, "12345678")

    def test_find_by_phone(self):
        with self.app.app_context():
            self.repo.create("John Doe", "12345678")
            customer = self.repo.find_by_phone("12345678")
            self.assertIsNotNone(customer)
            self.assertEqual(customer.name, "John Doe")
            
            customer_not_found = self.repo.find_by_phone("00000000")
            self.assertIsNone(customer_not_found)


    def test_update_loyalty(self):
        with self.app.app_context():
            customer = self.repo.create("John Doe", "12345678")
            self.repo.update_loyalty(customer.id, 10)
            
            updated_customer = Customer.query.get(customer.id)
            self.assertEqual(updated_customer.loyalty_points, 10)

if __name__ == '__main__':
    unittest.main()

