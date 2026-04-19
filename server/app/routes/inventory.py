from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from app.models.inventory_entry import InventoryEntry
from app.models.store_product import StoreProduct
from app.models.product import Product
from app.models.store import Store
from app.models.user import User
from sqlalchemy import func
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__)

def get_merchant_store_ids(merchant_id):
    stores = Store.query.filter_by(merchant_id=merchant_id).all()
    return [s.id for s in stores]

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
    current_user = db.session.get(User, current_user_id)

    data = request.get_json()

    required = ['product_id', 'quantity_received', 'buying_price', 'selling_price']
    missing = [f for f in required if f not in data]

    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    # ✅ FIXED: safe store_id resolution (NO JWT store_id dependency)
    store_id = data.get('store_id')

    if not store_id:
        store_id = current_user.store_id

    if not store_id:
        return jsonify({'error': 'Store not assigned to user'}), 400

    entry = InventoryEntry(
        store_id=store_id,
        product_id=data['product_id'],
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
        'message': 'Inventory entry recorded successfully',
        'entry': entry.to_dict()
    }), 201
# -----------------------------------------------
# GET ALL ENTRIES (paginated, scoped per role)
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

    # Base query (NO JOINS)
    query = InventoryEntry.query

    if role == 'clerk':
        query = query.filter(InventoryEntry.clerk_id == current_user_id)

    elif role == 'admin':
        query = query.filter(InventoryEntry.store_id == current_user.store_id)

    elif role == 'merchant':
        owned_ids = [s.id for s in Store.query.filter_by(merchant_id=current_user_id).all()]
        query = query.filter(InventoryEntry.store_id.in_(owned_ids))

    else:
        return jsonify({'error': 'Unauthorized'}), 403

    if payment_status in ['paid', 'unpaid']:
        query = query.filter(InventoryEntry.payment_status == payment_status)

    entries = query.order_by(InventoryEntry.recorded_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'entries': [e.to_dict() for e in entries.items],
        'total': entries.total,
        'pages': entries.pages,
        'current_page': entries.page
    }), 200

# -----------------------------------------------
# GET MY ENTRIES (Clerk Dashboard)
# -----------------------------------------------
@inventory_bp.route('/my-entries', methods=['GET'])
@jwt_required()
def get_my_entries():
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    if claims.get('role') != 'clerk':
        return jsonify({'error': 'Only clerks can access my-entries'}), 403

    limit = request.args.get('limit', 6, type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    payment_status = request.args.get('payment_status')

    query = InventoryEntry.query.filter_by(clerk_id=current_user_id)

    if payment_status in ['paid', 'unpaid']:
        query = query.filter_by(payment_status=payment_status)

    # Support both limit (dashboard) and pagination (my-entries page)
    if request.args.get('limit'):
        entries = query.order_by(InventoryEntry.recorded_at.desc()).limit(limit).all()
        return jsonify({'entries': [e.to_dict() for e in entries]}), 200
    else:
        result = query.order_by(InventoryEntry.recorded_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return jsonify({
            'entries': [e.to_dict() for e in result.items],
            'total': result.total,
            'pages': result.pages,
            'current_page': result.page
        }), 200

# -----------------------------------------------
# UPDATE PAYMENT STATUS
# -----------------------------------------------
@inventory_bp.route('/<int:entry_id>/payment', methods=['PATCH'])
@jwt_required()
def update_payment_status(entry_id):
    claims = get_jwt()
    role = claims.get('role')
    current_user_id = get_jwt_identity()

    if role not in ['admin', 'merchant']:
        return jsonify({'error': 'Not authorized'}), 403

    entry = InventoryEntry.query.get(entry_id)
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404

    if role == 'merchant':
        owned_ids = [s.id for s in Store.query.filter_by(merchant_id=current_user_id).all()]
        if entry.store_id not in owned_ids:
            return jsonify({'error': 'Not authorized'}), 403

    data = request.get_json()
    status = data.get('payment_status')

    if status not in ['paid', 'unpaid']:
        return jsonify({'error': 'Invalid status'}), 400

    entry.payment_status = status
    db.session.commit()

    return jsonify({
        'message': f'Payment status updated to {status}',
        'entry': entry.to_dict()
    }), 200
# -----------------------------------------------
# REPORT SUMMARY 
# -----------------------------------------------
@inventory_bp.route('/report/summary', methods=['GET'])
@jwt_required()
def get_summary():
    current_user_id = get_jwt_identity()
    current_user = db.session.get(User, current_user_id)
    claims = get_jwt()
    role = claims.get('role')

    query = InventoryEntry.query

    if role == 'clerk':
        query = query.filter(InventoryEntry.clerk_id == current_user_id)

    elif role == 'admin':
        query = query.filter(InventoryEntry.store_id == current_user.store_id)

    elif role == 'merchant':
        owned_ids = [s.id for s in Store.query.filter_by(merchant_id=current_user_id).all()]
        query = query.filter(InventoryEntry.store_id.in_(owned_ids))

    else:
        return jsonify({'error': 'Unauthorized'}), 403

    entries = query.all()

    total_received = sum(e.quantity_received for e in entries)
    total_in_stock = sum(e.quantity_in_stock for e in entries)
    total_spoilt = sum(e.quantity_spoilt for e in entries)
    total_paid = sum(e.buying_price * e.quantity_received for e in entries if e.payment_status == 'paid')
    total_unpaid = sum(e.buying_price * e.quantity_received for e in entries if e.payment_status == 'unpaid')

    return jsonify({
        'summary': {
            'total_items_received': total_received,
            'total_items_in_stock': total_in_stock,
            'total_items_spoilt': total_spoilt,
            'total_paid_amount': round(total_paid, 2),
            'total_unpaid_amount': round(total_unpaid, 2),
            'total_entries': len(entries)
        }
    }), 200

# -----------------------------------------------
# REPORT TREND 
# -----------------------------------------------
@inventory_bp.route('/report/trend', methods=['GET'])
@jwt_required()
def report_trend():
    claims = get_jwt()
    role = claims.get('role')
    current_user_id = get_jwt_identity()
    current_user = db.session.get(User, current_user_id)

    query = db.session.query(
        Product.name.label('product_name'),
        func.sum(InventoryEntry.quantity_received).label('quantity_received'),
        func.sum(InventoryEntry.quantity_in_stock).label('quantity_in_stock')
    ).join(Product, Product.id == InventoryEntry.product_id)

    if role == 'clerk':
        query = query.filter(InventoryEntry.clerk_id == current_user_id)

    elif role == 'admin':
        query = query.filter(InventoryEntry.store_id == current_user.store_id)

    elif role == 'merchant':
        owned_ids = [s.id for s in Store.query.filter_by(merchant_id=current_user_id).all()]
        query = query.filter(InventoryEntry.store_id.in_(owned_ids))

    else:
        return jsonify({'error': 'Unauthorized'}), 403

    trend = query.group_by(Product.name)\
                 .order_by(func.sum(InventoryEntry.quantity_received).desc())\
                 .limit(10).all()

    return jsonify({
        'trend': [
            {
                'product_name': r.product_name,
                'quantity_received': int(r.quantity_received or 0),
                'quantity_in_stock': int(r.quantity_in_stock or 0)
            } for r in trend
        ]
    }), 200