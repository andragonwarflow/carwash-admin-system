
from app import create_app
from app.models import db, User, Bay, Service, Product
from app.repositories.user_repository import UserRepository

app = create_app()
with app.app_context():
    user_repo = UserRepository()
    # Create admin user if not exists
    if not User.query.filter_by(username='admin').first():
        user_repo.create('admin', 'admin123')
        print("Admin user created: admin/admin123")
    
    # Seed Bays
    if not Bay.query.first():
        for i in range(1, 6):
            db.session.add(Bay(number=i, status='Available'))
        db.session.commit()
        print("Bays seeded.")
        
    # Seed Services
    if not Service.query.first():
        db.session.add_all([
            Service(name="Básico", price=10.0, duration_minutes=20),
            Service(name="Completo", price=20.0, duration_minutes=45),
            Service(name="Premium", price=30.0, duration_minutes=60),
        ])
        db.session.commit()
        print("Services seeded.")

    # Seed Products
    if not Product.query.first():
        db.session.add_all([
            Product(name="Cera", price=5.0, stock=20),
            Product(name="Aromatizante", price=2.0, stock=50),
        ])
        db.session.commit()
        print("Products seeded.")
