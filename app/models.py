from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cluster(db.Model):
    __tablename__ = 'clusters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    competitor_urls = db.Column(db.JSON)

    properties = db.relationship('Property', back_populates='cluster', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Cluster {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'competitor_urls': self.competitor_urls or [],
        }


class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.String(50), unique=True, nullable=False)
    property_name = db.Column(db.String(100), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Float, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    amenities = db.Column(db.Text)
    quality_keywords = db.Column(db.Text)
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id'), nullable=True)

    cluster = db.relationship('Cluster', back_populates='properties')
    price_logs = db.relationship('PriceLog', back_populates='property', cascade='all, delete-orphan')

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
            'quality_keywords': self.quality_keywords,
            'cluster_id': self.cluster.id if self.cluster else None,
            'cluster_name': self.cluster.name if self.cluster else None,
        }


class PriceLog(db.Model):
    __tablename__ = 'price_logs'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    our_listed_price = db.Column(db.Float, nullable=False)
    comp_avg_price = db.Column(db.Float, nullable=False)
    was_booked = db.Column(db.Boolean, nullable=False, default=False)
    final_price_paid = db.Column(db.Float)
    notes = db.Column(db.Text)
    day_of_week = db.Column(db.String(10), nullable=False)
    lead_time = db.Column(db.Integer)

    property = db.relationship('Property', back_populates='price_logs')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.date and not self.day_of_week:
            self.day_of_week = self.date.strftime('%A')
        if self.date and self.lead_time is None:
            today = date.today()
            self.lead_time = max((self.date - today).days, 0)

    def __repr__(self):
        unit = self.property.unit_id if self.property else 'Unknown'
        return f'<PriceLog {unit} - {self.date}>'

    def to_dict(self):
        cluster = self.property.cluster if self.property else None
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'property_id': self.property.id if self.property else None,
            'unit_id': self.property.unit_id if self.property else None,
            'cluster_id': cluster.id if cluster else None,
            'cluster_name': cluster.name if cluster else None,
            'our_listed_price': self.our_listed_price,
            'comp_avg_price': self.comp_avg_price,
            'was_booked': self.was_booked,
            'final_price_paid': self.final_price_paid,
            'notes': self.notes,
            'day_of_week': self.day_of_week,
            'lead_time': self.lead_time,
        }
