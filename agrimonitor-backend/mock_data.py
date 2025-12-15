import random
from datetime import datetime, timedelta
from app import create_app
from models import db, User, Farm, SensorReading

def generate_mock_data():
    """Generate test data"""
    app = create_app()
    
    with app.app_context():
        print("🌱 Generating mock data...")
        
        # Create demo user
        user = User.query.filter_by(email='demo@example.com').first()
        if not user:
            user = User(email='demo@example.com', role='farmer')
            user.set_password('demo123')
            db.session.add(user)
            db.session.commit()
            print("✓ Created demo user")
        
        # Create demo farm
        farm = Farm.query.filter_by(farmer_id=user.id).first()
        if not farm:
            farm = Farm(
                farmer_id=user.id,
                name='Demo Farm',
                location='Tamayo, Ilocos',
                crop_type='tomato'
            )
            db.session.add(farm)
            db.session.commit()
            print("✓ Created demo farm")
        
        # Generate readings
        readings = []
        for i in range(100):
            timestamp = datetime.utcnow() - timedelta(hours=i*1.5)
            
            temperature = 25 + random.uniform(-5, 10)
            humidity = 60 + random.uniform(-20, 20)
            soil_moisture = 50 + random.uniform(-30, 30)
            
            reading = SensorReading(
                farm_id=farm.id,
                temperature=round(temperature, 2),
                humidity=round(humidity, 2),
                soil_moisture=round(soil_moisture, 2),
                light_intensity=random.randint(100, 1000),
                timestamp=timestamp
            )
            readings.append(reading)
        
        db.session.add_all(readings)
        db.session.commit()
        
        print(f"✓ Generated 100 readings")
        print("\n" + "="*50)
        print("✅ MOCK DATA READY!")
        print("="*50)
        print(f"Email: demo@example.com")
        print(f"Password: demo123")
        print(f"Farm ID: {farm.id}")
        print("="*50)

if __name__ == '__main__':
    generate_mock_data()