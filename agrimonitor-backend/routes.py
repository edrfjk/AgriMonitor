from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import hashlib
from models import db, Farm, SensorReading, Alert

api_bp = Blueprint('api', __name__)

def is_farm_owner(user_id, farm_id):
    """Check if user owns farm"""
    farm = Farm.query.get(farm_id)
    if not farm:
        return False
    return farm.farmer_id == user_id

# ============ FARM ROUTES ============

@api_bp.route('/farms', methods=['POST'])
@jwt_required()
def create_farm():
    """Create new farm"""
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        if not data.get('name'):
            return jsonify(error='Farm name required'), 400
        
        farm = Farm(
            farmer_id=user_id,
            name=data.get('name'),
            location=data.get('location', ''),
            crop_type=data.get('crop_type', '')
        )
        
        db.session.add(farm)
        db.session.commit()
        
        return jsonify(farm_id=farm.id, message='Farm created'), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500


@api_bp.route('/farms', methods=['GET'])
@jwt_required()
def list_farms():
    """List user's farms"""
    try:
        user_id = get_jwt_identity()
        farms = Farm.query.filter_by(farmer_id=user_id).all()
        
        return jsonify([{
            'id': f.id,
            'name': f.name,
            'location': f.location,
            'crop_type': f.crop_type
        } for f in farms]), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


# ============ SENSOR ROUTES ============

@api_bp.route('/sensor-data', methods=['POST'])
@jwt_required()
def submit_sensor_data():
    """Submit sensor reading"""
    try:
        user_id = get_jwt_identity()
        data = request.json
        farm_id = data.get('farm_id')
        
        if not is_farm_owner(user_id, farm_id):
            return jsonify(error='Unauthorized'), 403
        
        # Validate values
        if not all([
            -10 <= data.get('temperature', -100) <= 50,
            0 <= data.get('humidity', -1) <= 100,
            0 <= data.get('soil_moisture', -1) <= 100
        ]):
            return jsonify(error='Invalid sensor values'), 400
        
        reading = SensorReading(
            farm_id=farm_id,
            temperature=float(data['temperature']),
            humidity=float(data['humidity']),
            soil_moisture=float(data['soil_moisture']),
            light_intensity=data.get('light_intensity'),
            timestamp=datetime.utcnow()
        )
        
        db.session.add(reading)
        db.session.commit()
        
        return jsonify(
            success=True,
            reading_id=reading.id,
            timestamp=reading.timestamp.isoformat()
        ), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500


@api_bp.route('/farms/<int:farm_id>/data', methods=['GET'])
@jwt_required()
def get_farm_data(farm_id):
    """Get sensor data"""
    try:
        user_id = get_jwt_identity()
        
        if not is_farm_owner(user_id, farm_id):
            return jsonify(error='Unauthorized'), 403
        
        days = request.args.get('days', 7, type=int)
        start_time = datetime.utcnow() - timedelta(days=days)
        
        readings = SensorReading.query.filter_by(farm_id=farm_id).filter(
            SensorReading.timestamp >= start_time
        ).order_by(SensorReading.timestamp.desc()).all()
        
        return jsonify([{
            'id': r.id,
            'temperature': r.temperature,
            'humidity': r.humidity,
            'soil_moisture': r.soil_moisture,
            'light_intensity': r.light_intensity,
            'timestamp': r.timestamp.isoformat()
        } for r in readings]), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@api_bp.route('/farms/<int:farm_id>/latest', methods=['GET'])
@jwt_required()
def get_latest_reading(farm_id):
    """Get latest sensor reading"""
    try:
        user_id = get_jwt_identity()
        
        if not is_farm_owner(user_id, farm_id):
            return jsonify(error='Unauthorized'), 403
        
        reading = SensorReading.query.filter_by(farm_id=farm_id).order_by(
            SensorReading.timestamp.desc()
        ).first()
        
        if not reading:
            return jsonify(error='No data'), 404
        
        return jsonify(
            temperature=reading.temperature,
            humidity=reading.humidity,
            soil_moisture=reading.soil_moisture,
            light_intensity=reading.light_intensity,
            timestamp=reading.timestamp.isoformat()
        ), 200
    except Exception as e:
        return jsonify(error=str(e)), 500