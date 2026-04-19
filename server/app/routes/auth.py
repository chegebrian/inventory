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
    try:
        data = request.get_json(force=True)

        if not isinstance(data, dict):
            return jsonify({'error': 'Invalid JSON format'}), 400

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
            data.get('password').encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        new_store = Store(
            name=data.get('store_name'),
            location=data.get('location', 'Head Office')
        )
        db.session.add(new_store)
        db.session.flush()

        merchant = User(
            full_name=data.get('full_name'),
            email=email,
            phone_number=data.get('phone_number'),
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
            'message': 'Merchant account created successfully!',
            'access_token': access_token,
            'user': merchant.to_dict(),
            'store': new_store.to_dict()
        }), 201

    except Exception as e:
        print("❌ ERROR IN REGISTER MERCHANT:", str(e))
        return jsonify({'error': str(e)}), 500


# =============================================
# LOGIN
# =============================================
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)

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

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role}
        )

        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        print("❌ ERROR IN LOGIN:", str(e))
        return jsonify({'error': str(e)}), 500


# =============================================
# GET USERS (SAFE FOR CORS)
# =============================================
@auth_bp.route('/users', methods=['GET', 'OPTIONS'])
def get_users():

    if request.method == 'OPTIONS':
        return '', 200

    try:
        verify_jwt_in_request()

        role = request.args.get('role')

        if role:
            users = User.query.filter_by(role=role).all()
        else:
            users = User.query.all()

        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200

    except Exception as e:
        print("❌ ERROR IN GET USERS:", str(e))
        return jsonify({'error': str(e)}), 500


# =============================================
# INVITE USER
# =============================================
@auth_bp.route('/invite', methods=['POST', 'OPTIONS'])
def invite_user():

    if request.method == 'OPTIONS':
        return '', 200

    try:
        verify_jwt_in_request()

        data = request.get_json(force=True)

        email = data.get('email')
        role = data.get('role')

        if not email or not role:
            return jsonify({'error': 'Email and role are required'}), 400

        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'User already exists'}), 409

        invite_token = secrets.token_urlsafe(32)
        expiry = datetime.utcnow() + timedelta(hours=24)

        current_user = User.query.get(get_jwt_identity())

        new_user = User(
            email=email,
            role=role,
            is_active=True,
            is_verified=False,
            invite_token=invite_token,
            invite_token_expiry=expiry,
            store_id=current_user.store_id
        )

        db.session.add(new_user)
        db.session.commit()

        send_invite_email(email, invite_token)

        return jsonify({'message': f'{role} invited successfully'}), 201

    except Exception as e:
        print("❌ ERROR IN INVITE:", str(e))
        return jsonify({'error': str(e)}), 500


# =============================================
# UPDATE PROFILE
# =============================================
@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json(force=True)

        if 'full_name' in data:
            user.full_name = data['full_name']

        if 'phone_number' in data:
            user.phone_number = data['phone_number']

        db.session.commit()

        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =============================================
# TOGGLE USER ACTIVE
# =============================================
@auth_bp.route('/users/<int:user_id>/toggle-active', methods=['PUT', 'OPTIONS'])
def toggle_user_status(user_id):

    if request.method == 'OPTIONS':
        return '', 200

    try:
        verify_jwt_in_request()

        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        user.is_active = not user.is_active
        db.session.commit()

        return jsonify({
            'message': 'Status updated successfully',
            'is_active': user.is_active
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =============================================
# ✅ DELETE USER (FINAL FIX)
# =============================================
@auth_bp.route('/users/<int:user_id>', methods=['DELETE', 'OPTIONS'])
def delete_user(user_id):

    if request.method == 'OPTIONS':
        return '', 200

    try:
        verify_jwt_in_request()

        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        print("❌ ERROR IN DELETE USER:", str(e))
        return jsonify({'error': str(e)}), 500