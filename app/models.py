from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    occupancy_rate = db.Column(db.Float, nullable=False)
    revenue = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Property {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'occupancy_rate': self.occupancy_rate,
            'revenue': self.revenue,
            'date_created': self.date_created.isoformat()
        }
