
from app.models import Service

class QueueService:
    def __init__(self, queue_repo, bay_repo):
        self.queue_repo = queue_repo
        self.bay_repo = bay_repo

    def calculate_wait_time(self, service_id):
        waiting_items = self.queue_repo.get_waiting_items()
        total_time = 0
        for item in waiting_items:
            # Here we'd normally use a ServiceRepository, but for now we use the model
            service = Service.query.get(item.service_id)
            if service:
                total_time += service.duration_minutes
        return total_time

    def process_next_vehicle(self):
        next_item = self.queue_repo.get_next_in_queue()
        if not next_item:
            return False
        
        bay = self.bay_repo.find_available()
        if not bay:
            return False
            
        self.queue_repo.update_status(next_item.id, 'In-Service')
        self.bay_repo.update_status(bay.id, 'Occupied')
        self.bay_repo.assign_vehicle(bay.id, next_item.id)
        return True
