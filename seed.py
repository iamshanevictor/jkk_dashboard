from app import create_app
from app.models import db, Property, Cluster


def seed_data():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        cluster_luxury_2br = Cluster(
            name='LUXURY_2BR',
            description='High-end, 2-bedroom properties in prime locations',
            competitor_urls=['http://comp1.com/luxury', 'http://comp2.com/luxury'],
        )
        cluster_beach_1br = Cluster(
            name='BEACH_1BR',
            description='Cozy, 1-bedroom properties with beach access',
            competitor_urls=['http://comp3.com/beach', 'http://comp4.com/beach'],
        )
        db.session.add_all([cluster_luxury_2br, cluster_beach_1br])
        db.session.flush()

        prop_a = Property(
            unit_id='UNIT_A',
            property_name='Luxury Downtown Apartment',
            bedrooms=2,
            bathrooms=2.5,
            max_guests=6,
            amenities='Pool, Gym, Balcony, City View',
            quality_keywords='Modern, Spacious, High-end finishes',
            cluster=cluster_luxury_2br,
        )

        prop_b = Property(
            unit_id='UNIT_B',
            property_name='Cozy Beachfront Condo',
            bedrooms=1,
            bathrooms=1.0,
            max_guests=3,
            amenities='Beach access, Ocean view, Free parking',
            quality_keywords='Charming, Relaxing, Coastal decor',
            cluster=cluster_beach_1br,
        )

        db.session.add_all([prop_a, prop_b])
        db.session.commit()
        print("Database seeded with sample clusters and properties.")


if __name__ == '__main__':
    seed_data()
