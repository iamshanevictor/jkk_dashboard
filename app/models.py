from datetime import datetime, date
from mongoengine import Document, StringField, IntField, FloatField, BooleanField, DateField, ListField, ReferenceField, CASCADE
import json

class Cluster(Document):
    name = StringField(required=True, unique=True, max_length=50)  # e.g., 'LUXURY_2BR'
    description = StringField()
    competitor_urls = ListField(StringField())  # Storing a list of URLs
    
    meta = {
        'collection': 'clusters',
        'indexes': [
            'name'
        ]
    }

    def __repr__(self):
        return f'<Cluster {self.name}>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'competitor_urls': self.competitor_urls
        }

class Property(Document):
    unit_id = StringField(required=True, unique=True, max_length=50)
    property_name = StringField(required=True, max_length=100)
    bedrooms = IntField(required=True)
    bathrooms = FloatField(required=True)
    max_guests = IntField(required=True)
    amenities = StringField()
    quality_keywords = StringField()
    cluster = ReferenceField('Cluster', required=True, reverse_delete_rule=CASCADE)
    
    meta = {
        'collection': 'properties',
        'indexes': [
            'unit_id',
            'cluster'
        ]
    }

    def __repr__(self):
        return f'<Property {self.unit_id} - {self.property_name}>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'unit_id': self.unit_id,
            'property_name': self.property_name,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'max_guests': self.max_guests,
            'amenities': self.amenities,
            'quality_keywords': self.quality_keywords,
            'cluster_id': str(self.cluster.id) if self.cluster else None,
            'cluster_name': self.cluster.name if self.cluster else None
        }

class PriceLog(Document):
    date = DateField(required=True)
    property = ReferenceField('Property', required=True, reverse_delete_rule=CASCADE)
    our_listed_price = FloatField(required=True)
    comp_avg_price = FloatField(required=True)
    was_booked = BooleanField(required=True, default=False)
    final_price_paid = FloatField()
    notes = StringField()
    day_of_week = StringField(required=True, max_length=10)
    lead_time = IntField()
    
    meta = {
        'collection': 'price_logs',
        'indexes': [
            'date',
            'property',
            ('date', 'property')
        ]
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.date and not self.day_of_week:
            self.day_of_week = self.date.strftime('%A')
        
        # Automatically calculate lead_time if not provided and date is available
        if self.date and not self.lead_time:
            today = date.today()
            # Lead time is the number of days between today and the check-in date
            self.lead_time = (self.date - today).days if self.date >= today else 0

    def __repr__(self):
        return f'<PriceLog {self.property.unit_id if self.property else "Unknown"} - {self.date}>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'date': self.date.isoformat(),
            'property_id': str(self.property.id) if self.property else None,
            'unit_id': self.property.unit_id if self.property else None,
            'cluster_id': str(self.property.cluster.id) if self.property and self.property.cluster else None,
            'cluster_name': self.property.cluster.name if self.property and self.property.cluster else None,
            'our_listed_price': self.our_listed_price,
            'comp_avg_price': self.comp_avg_price,
            'was_booked': self.was_booked,
            'final_price_paid': self.final_price_paid,
            'notes': self.notes,
            'day_of_week': self.day_of_week,
            'lead_time': self.lead_time
        }
