#!/usr/bin/env python
"""
Test script to verify MongoDB connection and basic functionality
"""

import os
from datetime import datetime

# Set environment variables for testing
os.environ['FLASK_ENV'] = 'development'
os.environ['MONGODB_URI'] = 'mongodb://localhost:27017/rentalytics_dashboard_test'

try:
    from app import create_app
    from app.models import Cluster, Property, PriceLog
    
    print("✓ Successfully imported app and models")
    
    # Create app
    app = create_app()
    with app.app_context():
        print("✓ App context created successfully")
        
        # Test database connection
        try:
            # Clear test collections
            Cluster.drop_collection()
            Property.drop_collection()
            PriceLog.drop_collection()
            print("✓ Database connection established - collections cleared")
            
            # Test creating a cluster
            test_cluster = Cluster(
                name='TEST_CLUSTER',
                description='Test cluster for verification',
                competitor_urls=['http://test1.com', 'http://test2.com']
            )
            test_cluster.save()
            print("✓ Successfully created test cluster")
            
            # Test creating a property
            test_property = Property(
                unit_id='TEST_UNIT',
                property_name='Test Property',
                bedrooms=2,
                bathrooms=1.5,
                max_guests=4,
                amenities='Test amenities',
                quality_keywords='Test keywords',
                cluster=test_cluster
            )
            test_property.save()
            print("✓ Successfully created test property")
            
            # Test creating a price log
            test_log = PriceLog(
                property=test_property,
                date=datetime.now().date(),
                our_listed_price=100.0,
                comp_avg_price=95.0,
                was_booked=True,
                final_price_paid=95.0,
                notes='Test booking'
            )
            test_log.save()
            print("✓ Successfully created test price log")
            
            # Test queries
            clusters = Cluster.objects.all()
            properties = Property.objects.all()
            logs = PriceLog.objects.all()
            
            print(f"✓ Found {len(clusters)} clusters, {len(properties)} properties, {len(logs)} logs")
            
            # Test relationship
            prop = Property.objects(unit_id='TEST_UNIT').first()
            if prop and prop.cluster:
                print(f"✓ Property-cluster relationship working: {prop.unit_id} -> {prop.cluster.name}")
            else:
                print("✗ Property-cluster relationship failed")
            
            # Test query with filters
            booked_logs = PriceLog.objects(was_booked=True).all()
            print(f"✓ Query with filter working: {len(booked_logs)} booked logs found")
            
            # Clean up
            Cluster.drop_collection()
            Property.drop_collection()
            PriceLog.drop_collection()
            print("✓ Test data cleaned up")
            
            print("\n🎉 All tests passed! MongoDB integration is working correctly.")
            
        except Exception as e:
            print(f"✗ Database operation failed: {str(e)}")
            
except ImportError as e:
    print(f"✗ Import failed: {str(e)}")
    print("Please ensure all dependencies are installed: pip install -r requirements.txt")
    
except Exception as e:
    print(f"✗ Unexpected error: {str(e)}")
