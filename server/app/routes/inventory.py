from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from app.models.inventory_entry import InventoryEntry
from app.models.store_product import StoreProduct
from app.models.product import Product
from app.models.user import User
from sqlalchemy import func
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__)

# -----------------------------------------------
# CREATE AN INVENTORY ENTRY (Clerk only)
# -----------------------------------------------
@inventory_bp.route('/', methods=['POST'])
@jwt_required()
def create_entry():
    claims = get_jwt()
    if claims.get('role') != 'clerk':
        return jsonify({'error': 'Only clerks can record inventory'}), 403

    current_user_id = get_jwt_identity()
    data = request.get_json()

    required = ['store_product_id', 'quantity_received', 'buying_price', 'selling_price']
    missing = [f for f in required if f not in data or not data[f]]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    store_product = db.session.get(StoreProduct, data['store_product_id'])
    if not store_product:
        return jsonify({'error': 'Product not found in store'}), 404

    entry = InventoryEntry(
        store_product_id=data['store_product_id'],
        clerk_id=current_user_id,
        quantity_received=int(data['quantity_received']),
        quantity_in_stock=int(data.get('quantity_in_stock', data['quantity_received'])),
        quantity_spoilt=int(data.get('quantity_spoilt', 0)),
        buying_price=float(data['buying_price']),
        selling_price=float(data['selling_price']),
        payment_status=data.get('payment_status', 'unpaid')
    )
    db.session.add(entry)
    db.session.commit()

    return jsonify({
        'message': 'Inventory entry recorded successfully ✅',
        'entry': entry.to_dict()
    }), 201

# -----------------------------------------------
# GET ALL ENTRIES (paginated)
# -----------------------------------------------
@inventory_bp.route('/', methods=['GET'])
@jwt_required()
def get_entries():
    current_user_id = get_jwt_identity()
    current_user = db.session.get(User, current_user_id)
    claims = get_jwt()
    role = claims.get('role')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    payment_status = request.args.get('payment_status')

    if role == 'clerk':
        query = InventoryEntry.query.filter_by(clerk_id=current_user_id)
    elif role == 'admin':
        if not current_user or not current_user.store_id:
            return jsonify({'error': 'Admin not assigned to any store'}), 403
        query = InventoryEntry.query.join(StoreProduct).filter(StoreProduct.store_id == current_user.store_id)
    else:
        query = InventoryEntry.query

    if payment_status in ['paid', 'unpaid']:
        query = query.filter_by(payment_status=payment_status)

    entries = query.order_by(InventoryEntry.recorded_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'entries': [e.to_dict() for e in entries.items],
        'total': entries.total,
        'pages': entries.pages,
        'current_page': entries.page
    }), 200