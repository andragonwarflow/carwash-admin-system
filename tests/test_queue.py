
import unittest
from app.models import db, Queue
from app.repositories.queue_repository import QueueRepository
from flask import Flask
from datetime import datetime

class TestQueueRepository(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            self.repo = QueueRepository()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_enqueue(self):
        with self.app.app_context():
            queue_item = self.repo.enqueue(1, 1)
            self.assertIsNotNone(queue_item.id)
            self.assertEqual(queue_item.customer_id, 1)
            self.assertEqual(queue_item.service_id, 1)
            self.assertEqual(queue_item.status, 'Waiting')

    def test_get_next_in_queue(self):
        with self.app.app_context():
            self.repo.enqueue(1, 1)
            self.repo.enqueue(2, 1)
            
            next_item = self.repo.get_next_in_queue()
            self.assertIsNotNone(next_item)
            self.assertEqual(next_item.customer_id, 1)

    def test_update_status(self):
        with self.app.app_context():
            item = self.repo.enqueue(1, 1)
            self.repo.update_status(item.id, 'In-Service')
            
            updated_item = Queue.query.get(item.id)
            self.assertEqual(updated_item.status, 'In-Service')

if __name__ == '__main__':
    unittest.main()
