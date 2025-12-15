from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='farmer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    farms = db.relationship('Farm', backref='farmer', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Farm(db.Model):
    """Farm model"""
    __tablename__ = 'farms'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    crop_type = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    readings = db.relationship('SensorReading', backref='farm', lazy=True)
    alerts = db.relationship('Alert', backref='farm', lazy=True)
    
    def __repr__(self):
        return f'<Farm {self.name}>'


class SensorReading(db.Model):
    """Sensor reading model"""
    __tablename__ = 'sensor_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    soil_moisture = db.Column(db.Float, nullable=False)
    light_intensity = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    checksum = db.Column(db.String(255))
    
    __table_args__ = (
        db.CheckConstraint('temperature > -10 AND temperature < 50'),
        db.CheckConstraint('humidity >= 0 AND humidity <= 100'),
        db.CheckConstraint('soil_moisture >= 0 AND soil_moisture <= 100'),
    )
    
    def __repr__(self):
        return f'<SensorReading temp={self.temperature}>'


class Alert(db.Model):
    """Alert model"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    alert_type = db.Column(db.String(100))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Alert {self.alert_type}>'