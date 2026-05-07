
from app.models import db, Customer

class CustomerRepository:
    def create(self, name, phone):
        customer = Customer(name=name, phone=phone)
        db.session.add(customer)
        db.session.commit()
        return customer

    def find_by_phone(self, phone):
        return Customer.query.filter_by(phone=phone).first()

    def update_loyalty(self, customer_id, points):
        customer = Customer.query.get(customer_id)
        if customer:
            customer.loyalty_points = points
            db.session.commit()
        return customer
