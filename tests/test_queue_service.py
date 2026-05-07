
import unittest
from app.models import db, Queue, Bay, Service
from app.services.queue_service import QueueService
from app.repositories.queue_repository import QueueRepository
from app.repositories.bay_repository import BayRepository
from flask import Flask
from unittest.mock import MagicMock

class TestQueueService(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)
        
        with self.app.app_context():
            db.create_all()
            self.queue_repo = QueueRepository()
            self.bay_repo = BayRepository()
            self.service = QueueService(self.queue_repo, self.bay_repo)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_calculate_wait_time(self):
        with self.app.app_context():
            # Create services
            s1 = Service(name="Basic", price=10.0, duration_minutes=15)
            s2 = Service(name="Full", price=20.0, duration_minutes=30)
            db.session.add_all([s1, s2])
            db.session.commit()
            
            # Enqueue
            self.queue_repo.enqueue(1, s1.id)
            self.queue_repo.enqueue(2, s2.id)
            
            wait_time = self.service.calculate_wait_time(s1.id)
            # Total waiting time = 15 + 30 = 45
            self.assertEqual(wait_time, 45)

    def test_process_next_vehicle_success(self):
        with self.app.app_context():
            # Create bay and queue item
            bay = Bay(number=1, status='Available')
            db.session.add(bay)
            db.session.commit()
            
            item = self.queue_repo.enqueue(1, 1) # Service ID 1 (doesn't exist but we just need the item)
            
            result = self.service.process_next_vehicle()
            
            self.assertTrue(result)
            self.assertEqual(item.status, 'In-Service')
            self.assertEqual(bay.status, 'Occupied')
            self.assertEqual(bay.current_queue_id, item.id)

    def test_process_next_vehicle_no_bay(self):
        with self.app.app_context():
            # No bays created
            item = self.queue_repo.enqueue(1, 1)
            
            result = self.service.process_next_vehicle()
            
            self.assertFalse(result)
            self.assertEqual(item.status, 'Waiting')

if __name__ == '__main__':
    unittest.main()
