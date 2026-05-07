from app.models import db, Bay

class BayRepository:
    def get_bay(self, bay_id):
        return Bay.query.get(bay_id)

    def get_all_bays(self):
        return Bay.query.all()

    def find_available(self):
        return Bay.query.filter_by(status='Available').first()

    def update_status(self, bay_id, status):
        bay = Bay.query.get(bay_id)
        if bay:
            bay.status = status
            db.session.commit()
            return True
        return False

    def assign_vehicle(self, bay_id, queue_id):
        bay = Bay.query.get(bay_id)
        if bay:
            bay.current_queue_id = queue_id
            bay.status = 'Occupied'
            db.session.commit()
            return True
        return False
