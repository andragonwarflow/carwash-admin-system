
# As-Built Documentation - Carwash Administrative System v2

## 1. Architecture
The system follows a **Layered Architecture** (Clean Architecture inspired):
- **Presentation Layer**: Flask Blueprints, HTML Templates (Jinja2), and Bootstrap 5.
- **Service Layer**: Business logic encapsulated in Service classes (`QueueService`, `SaleService`, etc.).
- **Data Access Layer**: Repository Pattern (`BayRepository`, `CustomerRepository`, etc.) to abstract SQLAlchemy.

## 2. Component Map
- `app/models.py`: Database schema.
- `app/repositories/`: Data persistence logic.
- `app/services/`: Business rules and orchestration.
- `app/api/`: HTTP endpoints and auth.
- `tests/`: TDD suite.

## 3. Security
- **Authentication**: Flask-Login.
- **Password Storage**: Hashed using `werkzeug.security.generate_password_hash` (PBKDF2).
- **Access Control**: `@login_required` decorators on sensitive routes.

## 4. Setup
1. Activate venv: `source venv/bin/activate`
2. Install deps: `pip install -r requirements.txt` (if available)
3. Run: `python run.py`
