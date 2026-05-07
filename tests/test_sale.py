
import unittest
from app.models import db, Sale, SaleItem, Product
from app.repositories.sale_repository import SaleRepository
from flask import Flask

class TestSaleRepository(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            self.repo = SaleRepository()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_save_sale(self):
        with self.app.app_context():
            sale_data = {'total_amount': 100.0, 'currency': 'L'}
            items = [
                {'item_id': 1, 'item_type': 'service', 'quantity': 1, 'price': 60.0, 'currency': 'L'},
                {'item_id': 2, 'item_type': 'product', 'quantity': 2, 'price': 20.0, 'currency': 'L'},
            ]
            
            sale = self.repo.save_sale(sale_data, items)
            self.assertIsNotNone(sale.id)
            self.assertEqual(sale.total_amount, 100.0)
            
            sale_items = SaleItem.query.filter_by(sale_id=sale.id).all()
            self.assertEqual(len(sale_items), 2)

    def test_update_product_stock(self):
        with self.app.app_context():
            product = Product(name="Wax", price=10.0, stock=10, currency='L')
            db.session.add(product)
            db.session.commit()
            
            self.repo.update_product_stock(product.id, 2)
            updated_product = Product.query.get(product.id)
            self.assertEqual(updated_product.stock, 8)

if __name__ == '__main__':
    unittest.main()
