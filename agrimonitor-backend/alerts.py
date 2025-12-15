from flask import Blueprint, jsonify
from models import Alert

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/', methods=['GET'])
def get_alerts():
    alerts = Alert.query.all()
    return jsonify([{
        'id': a.id,
        'farm_id': a.farm_id,
        'message': a.message,
        'level': a.level,
        'timestamp': a.timestamp.isoformat()
    } for a in alerts])
