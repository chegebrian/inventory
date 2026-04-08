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