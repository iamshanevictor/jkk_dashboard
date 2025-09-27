from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB # For PostgreSQL JSON type
import json

db = SQLAlchemy()

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.String(50), unique=True, nullable=False)
    property_name = db.Column(db.String(100), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Float, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    amenities = db.Column(db.Text, nullable=True)
    quality_keywords = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Property {self.unit_id} - {self.property_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'unit_id': self.unit_id,
            'property_name': self.property_name,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'max_guests': self.max_guests,
            'amenities': self.amenities,
            'quality_keywords': self.quality_keywords
        }


class PriceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    our_listed_price = db.Column(db.Float, nullable=False)
    comp_avg_price = db.Column(db.Float, nullable=False)
    was_booked = db.Column(db.Boolean, default=False, nullable=False)
    final_price_paid = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    day_of_week = db.Column(db.String(10), nullable=False)
    lead_time = db.Column(db.Integer, nullable=True)

    property = db.relationship('Property', backref=db.backref('price_logs', lazy=True))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.date and not self.day_of_week:
            self.day_of_week = self.date.strftime('%A')
        
        # Automatically calculate lead_time if not provided and date is available
        if self.date and not self.lead_time:
            from datetime import date
            today = date.today()
            # Lead time is the number of days between today and the check-in date
            self.lead_time = (self.date - today).days if self.date >= today else 0

    def __repr__(self):
        return f'<PriceLog {self.property.unit_id} - {self.date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'property_id': self.property_id,
            'unit_id': self.property.unit_id, # Include unit_id for easier frontend consumption
            'property_name': self.property.property_name, # Include property_name for easier frontend consumption
            'our_listed_price': self.our_listed_price,
            'comp_avg_price': self.comp_avg_price,
            'was_booked': self.was_booked,
            'final_price_paid': self.final_price_paid,
            'notes': self.notes,
            'day_of_week': self.day_of_week,
            'lead_time': self.lead_time
        }
