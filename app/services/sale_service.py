
from app.models import db, Transaction, Sale

class SaleService:
    def __init__(self, sale_repo, bay_repo, queue_repo):
        self.sale_repo = sale_repo
        self.bay_repo = bay_repo
        self.queue_repo = queue_repo

    def calculate_total(self, items):
        return sum(item['price'] * item['quantity'] for item in items)

    def finalize_sale(self, sale_id, queue_id, bay_id):
        sale = Sale.query.get(sale_id)
        if not sale:
            return False
            
        # 1. Record Transaction
        transaction = Transaction(
            amount=sale.total_amount,
            currency=sale.currency,
            type='income',
            description=f"Sale #{sale.id}"
        )
        db.session.add(transaction)
        
        # 2. Update Queue Status
        self.queue_repo.update_status(queue_id, 'Completed')
        
        # 3. Liberate Bay
        self.bay_repo.update_status(bay_id, 'Available')
        # Clear the current_queue_id from bay
        bay = self.bay_repo.get_bay(bay_id) # I need to implement get_bay in BayRepository
        if bay:
            bay.current_queue_id = None
            db.session.commit()
            
        db.session.commit()
        return True
