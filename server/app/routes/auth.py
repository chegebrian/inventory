from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request
)
from app import db
from app.models.user import User
from app.models.store import Store
from app.utils.validators import validate_email, validate_required_fields
from app.utils.email import send_invite_email
import bcrypt
import secrets
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

# =============================================
# MERCHANT SELF-REGISTRATION
# =============================================
@auth_bp.route('/register-merchant', methods=['POST'])
def register_merchant():
    data = request.get_json(silent=True) or {}

    required_fields = ['full_name', 'email', 'password', 'store_name']
    missing = validate_required_fields(data, required_fields)

    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    email = data.get('email').strip()

    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    password_hash = bcrypt.hashpw(
        data['password'].encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    new_store = Store(
        name=data['store_name'],
        location=data.get('location', 'Head Office')
    )
    db.session.add(new_store)
    db.session.flush()

    merchant = User(
        full_name=data['full_name'],
        email=email,
        password_hash=password_hash,
        role='merchant',
        is_active=True,
        is_verified=True,
        store_id=new_store.id
    )
    db.session.add(merchant)
    db.session.flush()

    new_store.merchant_id = merchant.id
    db.session.commit()

    access_token = create_access_token(
        identity=str(merchant.id),
        additional_claims={'role': 'merchant'}
    )

    return jsonify({
        'message': 'Merchant created successfully',
        'access_token': access_token,
        'user': merchant.to_dict(),
        'store': new_store.to_dict()
    }), 201


# =============================================
# LOGIN ✅ FIXED
# =============================================
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json(silent=True) or {}

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not user.password_hash:
            return jsonify({'error': 'Invalid credentials'}), 401

        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return jsonify({'error': 'Invalid credentials'}), 401

        if not user.is_active:
            return jsonify({'error': 'Account suspended'}), 403

        if not user.is_verified:
            return jsonify({'error': 'Account not verified'}), 403

        # ✅ CREATE TOKEN (THIS WAS MISSING)
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role}
        )

        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =============================================
# INVITE USER
# =============================================
@auth_bp.route('/invite', methods=['POST'])
@jwt_required()
def invite():
    current_user = User.query.get(get_jwt_identity())

    if current_user.role not in ['merchant', 'admin']:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json(silent=True) or {}
    email = data.get('email')
    role = data.get('role')

    if not email or not role:
        return jsonify({'error': 'Email and role required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 409

    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(hours=48)

    new_user = User(
        email=email,
        role=role,
        invite_token=token,
        invite_token_expiry=expiry,
        is_active=True,
        is_verified=False,
        store_id=current_user.store_id
    )

    db.session.add(new_user)
    db.session.commit()

    invite_link = f"http://localhost:3000/register?token={token}"
    send_invite_email(email, invite_link, role, "LocalShop")

    return jsonify({'message': 'Invite sent'}), 200


# =============================================
# GET USERS
# =============================================
@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        role = request.args.get('role')

        if role:
            users = User.query.filter_by(role=role).all()
        else:
            users = User.query.all()

        return jsonify({
            'users': [u.to_dict() for u in users]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =============================================
# CHANGE PASSWORD
# =============================================
@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    user = User.query.get(get_jwt_identity())

    data = request.get_json(silent=True) or {}
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not current_password or not new_password:
        return jsonify({'error': 'Missing fields'}), 400

    if not bcrypt.checkpw(current_password.encode(), user.password_hash.encode()):
        return jsonify({'error': 'Incorrect password'}), 401

    user.password_hash = bcrypt.hashpw(
        new_password.encode(), bcrypt.gensalt()
    ).decode('utf-8')

    db.session.commit()

    return jsonify({'message': 'Password updated'}), 200


# =============================================
# DELETE USER
# =============================================
@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500