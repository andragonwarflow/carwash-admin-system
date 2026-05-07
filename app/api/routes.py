
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required
from app.repositories.bay_repository import BayRepository
from app.repositories.queue_repository import QueueRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.sale_repository import SaleRepository
from app.services.queue_service import QueueService
from app.services.sale_service import SaleService
from app.services.customer_service import CustomerService

api_bp = Blueprint('api', __name__)

# Repositories
bay_repo = BayRepository()
queue_repo = QueueRepository()
customer_repo = CustomerRepository()
sale_repo = SaleRepository()

# Services
queue_service = QueueService(queue_repo, bay_repo)
sale_service = SaleService(sale_repo, bay_repo, queue_repo)
customer_service = CustomerService(customer_repo)

@api_bp.route('/')
@login_required
def index():
    bays = bay_repo.get_all_bays() # Need to implement get_all_bays
    queue = queue_repo.get_waiting_items()
    return render_template('index.html', bays=bays, queue=queue)

@api_bp.route('/bays')
@login_required
def get_bays():
    bays = bay_repo.get_all_bays()
    return jsonify([{'id': b.id, 'number': b.number, 'status': b.status} for b in bays])

@api_bp.route('/queue/add', methods=['POST'])
@login_required
def add_to_queue():
    data = request.json
    customer_id = data.get('customer_id')
    service_id = data.get('service_id')
    
    item = queue_repo.enqueue(customer_id, service_id)
    return jsonify({'status': 'success', 'item_id': item.id})

@api_bp.route('/queue/process', methods=['POST'])
@login_required
def process_queue():
    success = queue_service.process_next_vehicle()
    return jsonify({'status': 'success' if success else 'failed'})

@api_bp.route('/sale/finalize', methods=['POST'])
@login_required
def finalize_sale():
    data = request.json
    sale_id = data.get('sale_id')
    queue_id = data.get('queue_id')
    bay_id = data.get('bay_id')
    
    success = sale_service.finalize_sale(sale_id, queue_id, bay_id)
    return jsonify({'status': 'success' if success else 'failed'})

@api_bp.route('/customer/register', methods=['POST'])
@login_required
def register_customer():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    
    customer = customer_service.register_customer(name, phone)
    return jsonify({'status': 'success', 'customer_id': customer.id})
