from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.json
        
        if not data.get('email') or not data.get('password'):
            return jsonify(error='Email and password required'), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify(error='Email already registered'), 409
        
        user = User(email=data['email'], role='farmer')
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify(
            message='User registered successfully',
            user_id=user.id,
            email=user.email
        ), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login and get JWT token"""
    try:
        data = request.json
        
        if not data.get('email') or not data.get('password'):
            return jsonify(error='Email and password required'), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify(error='Invalid email or password'), 401
        
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(hours=24)
        )
        
        return jsonify(
            access_token=access_token,
            user_id=user.id,
            email=user.email,
            role=user.role
        ), 200
    
    except Exception as e:
        return jsonify(error=str(e)), 500