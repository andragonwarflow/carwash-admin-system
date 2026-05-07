
from app.models import db, Queue

class QueueRepository:
    def enqueue(self, customer_id, service_id):
        item = Queue(customer_id=customer_id, service_id=service_id)
        db.session.add(item)
        db.session.commit()
        return item

    def get_next_in_queue(self):
        return Queue.query.filter_by(status='Waiting').order_by(Queue.entry_time.asc()).first()

    def get_waiting_items(self):
        return Queue.query.filter_by(status='Waiting').all()

    def update_status(self, queue_id, status):
        item = Queue.query.get(queue_id)
        if item:
            item.status = status
            db.session.commit()
        return item
