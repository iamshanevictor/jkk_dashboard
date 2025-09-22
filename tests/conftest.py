import pytest
import tempfile
import os
from app import create_app
from app.models import db, Property, Cluster

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app('development')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_data(app):
    with app.app_context():
        cluster = Cluster(name='TEST_CLUSTER', description='Test cluster')
        property_obj = Property(
            unit_id='TEST_UNIT',
            property_name='Test Property',
            bedrooms=2,
            bathrooms=1.5,
            max_guests=4,
            cluster_id='TEST_CLUSTER'
        )
        db.session.add_all([cluster, property_obj])
        db.session.commit()
        return {'cluster': cluster, 'property': property_obj}
