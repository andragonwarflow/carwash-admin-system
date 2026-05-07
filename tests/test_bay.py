import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import db, Bay, Queue
from app.repositories.bay_repository import BayRepository

class TestBayRepository(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)
        
        with self.app.app_context():
            db.create_all()
            # Setup some bays
            db.session.add(Bay(number=1, status='Available'))
            db.session.add(Bay(number=2, status='Occupied'))
            db.session.commit()
            
            self.repo = BayRepository()

    def test_find_available_bay(self):
        with self.app.app_context():
            bay = self.repo.find_available()
            self.assertIsNotNone(bay)
            self.assertEqual(bay.number, 1)
            self.assertEqual(bay.status, 'Available')

    def test_update_status_to_occupied(self):
        with self.app.app_context():
            bay = Bay.query.filter_by(number=1).first()
            self.repo.update_status(bay.id, 'Occupied')
            
            updated_bay = Bay.query.get(bay.id)
            self.assertEqual(updated_bay.status, 'Occupied')

    def test_assign_vehicle_to_bay(self):
        with self.app.app_context():
            # Create a dummy queue record
            queue_item = Queue(customer_id=1, service_id=1, status='Waiting')
            db.session.add(queue_item)
            db.session.commit()
            
            bay = Bay.query.filter_by(number=1).first()
            self.repo.assign_vehicle(bay.id, queue_item.id)
            
            updated_bay = Bay.query.get(bay.id)
            self.assertEqual(updated_bay.current_queue_id, queue_item.id)
            self.assertEqual(updated_bay.status, 'Occupied')

if __name__ == '__main__':
    unittest.main()
