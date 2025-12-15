from flask import Blueprint, jsonify
from models import Reading

readings_bp = Blueprint('readings', __name__)

@readings_bp.route('/', methods=['GET'])
def get_readings():
    readings = Reading.query.all()
    return jsonify([{
        'id': r.id,
        'farm_id': r.farm_id,
        'temperature': r.temperature,
        'humidity': r.humidity,
        'soil_moisture': r.soil_moisture,
        'light': r.light,
        'timestamp': r.timestamp.isoformat()
    } for r in readings])
