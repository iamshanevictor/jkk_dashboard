import os
from datetime import datetime
from app import create_app
from app.models import Property, Cluster # Import models without db
from mongoengine import connect, disconnect

def seed_data():
    app = create_app()
    with app.app_context():
        # Clear existing data
        Cluster.drop_collection()
        Property.drop_collection()
        print("Existing data cleared.")

        # Sample Cluster Data
        cluster_luxury_2br = Cluster(
            name='LUXURY_2BR',
            description='High-end, 2-bedroom properties in prime locations',
            competitor_urls=['http://comp1.com/luxury', 'http://comp2.com/luxury']
        )
        cluster_beach_1br = Cluster(
            name='BEACH_1BR',
            description='Cozy, 1-bedroom properties with beach access',
            competitor_urls=['http://comp3.com/beach', 'http://comp4.com/beach']
        )
        cluster_luxury_2br.save()
        cluster_beach_1br.save()
        print("Cluster collection seeded with sample data.")

        # Sample Property Data from "Property DNA" sheet
        prop_a = Property(
            unit_id='UNIT_A',
            property_name='Luxury Downtown Apartment',
            bedrooms=2,
            bathrooms=2.5,
            max_guests=6,
            amenities='Pool, Gym, Balcony, City View',
            quality_keywords='Modern, Spacious, High-end finishes',
            cluster=cluster_luxury_2br # Linked to Cluster
        )

        prop_b = Property(
            unit_id='UNIT_B',
            property_name='Cozy Beachfront Condo',
            bedrooms=1,
            bathrooms=1.0,
            max_guests=3,
            amenities='Beach access, Ocean view, Free parking',
            quality_keywords='Charming, Relaxing, Coastal decor',
            cluster=cluster_beach_1br # Linked to Cluster
        )

        prop_a.save()
        prop_b.save()
        print("Property collection seeded with sample data.")

if __name__ == '__main__':
    if 'MONGODB_URI' not in os.environ:
        print("Error: MONGODB_URI environment variable not set.")
        print("Please set it (e.g., export MONGODB_URI='mongodb://localhost:27017/rentalytics_dashboard')")
    else:
        seed_data()
