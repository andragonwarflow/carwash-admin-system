
class CustomerService:
    def __init__(self, customer_repo):
        self.repo = customer_repo

    def register_customer(self, name, phone):
        existing = self.repo.find_by_phone(phone)
        if existing:
            return existing
        return self.repo.create(name, phone)
