
import unittest
from app.models import db, Sale, SaleItem, Product, Bay, Queue, Transaction
from app.services.sale_service import SaleService
from app.repositories.sale_repository import SaleRepository
from app.repositories.bay_repository import BayRepository
from app.repositories.queue_repository import QueueRepository
from flask import Flask
from unittest.mock import MagicMock

class TestSaleService(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)
        
        with self.app.app_context():
            db.create_all()
            self.sale_repo = SaleRepository()
            self.bay_repo = BayRepository()
            self.queue_repo = QueueRepository()
            self.service = SaleService(self.sale_repo, self.bay_repo, self.queue_repo)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_calculate_total(self):
        items = [
            {'price': 60.0, 'quantity': 1},
            {'price': 20.0, 'quantity': 2},
        ]
        total = self.service.calculate_total(items)
        self.assertEqual(total, 100.0)

    def test_finalize_sale(self):
        with self.app.app_context():
            # Setup: Sale, Queue Item, Bay
            sale = Sale(total_amount=100.0, currency='L')
            db.session.add(sale)
            db.session.commit()
            
            queue_item = Queue(customer_id=1, service_id=1, status='In-Service')
            db.session.add(queue_item)
            db.session.commit()
            
            bay = Bay(number=1, status='Occupied', current_queue_id=queue_item.id)
            db.session.add(bay)
            db.session.commit()
            
            # We need a way to link sale to queue item in this MVP
            # In a real system, Sale might have a queue_id. 
            # Let's assume finalize_sale takes sale_id and we find the associated bay/queue
            # Based on SDD: "libera la bahía y registra la transacción financiera"
            # I'll implement finalize_sale to take sale_id and maybe the queue_id
            
            # For now, let's just test the logic
            self.service.finalize_sale(sale.id, queue_item.id, bay.id)
            
            self.assertEqual(queue_item.status, 'Completed')
            self.assertEqual(bay.status, 'Available')
            self.assertIsNone(bay.current_queue_id)
            
            # Check if transaction was recorded
            tx = Transaction.query.first()
            self.assertIsNotNone(tx)
            self.assertEqual(tx.amount, 100.0)
            self.assertEqual(tx.type, 'income')

if __name__ == '__main__':
    unittest.main()
