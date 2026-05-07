
import unittest
from app.models import db, Customer
from app.services.customer_service import CustomerService
from app.repositories.customer_repository import CustomerRepository
from flask import Flask
from unittest.mock import MagicMock

class TestCustomerService(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)
        
        self.repo = MagicMock(spec=CustomerRepository)
        self.service = CustomerService(self.repo)

    def test_register_customer_new(self):
        self.repo.find_by_phone.return_value = None
        self.repo.create.return_value = Customer(id=1, name="John", phone="123")
        
        customer = self.service.register_customer("John", "123")
        
        self.repo.find_by_phone.assert_called_with("123")
        self.repo.create.assert_called_with("John", "123")
        self.assertEqual(customer.name, "John")

    def test_register_customer_existing(self):
        existing_customer = Customer(id=1, name="John", phone="123")
        self.repo.find_by_phone.return_value = existing_customer
        
        customer = self.service.register_customer("John", "123")
        
        self.repo.create.assert_not_called()
        self.assertEqual(customer.id, 1)

if __name__ == '__main__':
    unittest.main()
