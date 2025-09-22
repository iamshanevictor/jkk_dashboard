import pytest
from datetime import date
from app.models import Property, Cluster, PriceLog

def test_cluster_creation(app, sample_data):
    """Test cluster model creation"""
    cluster = sample_data['cluster']
    assert cluster.name == 'TEST_CLUSTER'
    assert cluster.description == 'Test cluster'

def test_property_creation(app, sample_data):
    """Test property model creation"""
    property_obj = sample_data['property']
    assert property_obj.unit_id == 'TEST_UNIT'
    assert property_obj.bedrooms == 2
    assert property_obj.bathrooms == 1.5
    assert property_obj.max_guests == 4
    assert property_obj.cluster_id == 'TEST_CLUSTER'

def test_property_cluster_relationship(app, sample_data):
    """Test that property-cluster relationship works"""
    property_obj = sample_data['property']
    cluster = sample_data['cluster']
    assert property_obj.cluster == cluster
    assert property_obj in cluster.properties

def test_price_log_creation(app, sample_data):
    """Test price log creation"""
    from app.models import db
    property_obj = sample_data['property']
    
    price_log = PriceLog(
        property_id=property_obj.id,
        date=date.today(),
        our_listed_price=100.0,
        comp_avg_price=95.0,
        was_booked=True
    )
    
    db.session.add(price_log)
    db.session.commit()
    
    assert price_log.our_listed_price == 100.0
    assert price_log.comp_avg_price == 95.0
    assert price_log.was_booked is True
    assert price_log.day_of_week is not None
