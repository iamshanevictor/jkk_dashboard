import os
from flask import Flask
from app.config import config
from mongoengine import connect, disconnect

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Security headers
    @app.after_request
    def after_request(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    from app.routes import main as main_blueprint, data_entry_bp, insights_bp, management_bp
    app.register_blueprint(main_blueprint)
    app.register_blueprint(data_entry_bp)
    app.register_blueprint(insights_bp)
    app.register_blueprint(management_bp)

    with app.app_context():
        try:
            # Test MongoDB connection
            from app.models import Cluster, Property, PriceLog
            
            # Try to ensure indexes exist
            Cluster.ensure_indexes()
            Property.ensure_indexes()
            PriceLog.ensure_indexes()
            
            print("MongoDB connection and indexes are ready!")
            
        except Exception as e:
            print(f"MongoDB connection issue detected: {e}")
            raise

    return app
