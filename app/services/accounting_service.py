
from app.models import db, Transaction

class AccountingService:
    def record_transaction(self, amount, type, description):
        tx = Transaction(
            amount=amount,
            type=type, # 'income' or 'expense'
            description=description
        )
        db.session.add(tx)
        db.session.commit()
        return tx
