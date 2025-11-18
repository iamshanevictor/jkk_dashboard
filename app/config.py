import os
from dotenv import load_dotenv
from mongoengine import connect, disconnect

load_dotenv()

class Config:
    MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/rentalytics_dashboard')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    
    @staticmethod
    def init_app(app):
        # Initialize MongoDB connection
        connect(host=Config.MONGODB_URI, alias='default')
        
        @app.teardown_appcontext
        def cleanup_db(exception):
            # MongoDB connections are managed by MongoEngine
            pass

class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/rentalytics_dashboard_dev')

class ProductionConfig(Config):
    DEBUG = False
    MONGODB_URI = os.environ.get('MONGODB_URI')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        # Production-specific initialization
        
        # Log to stderr
        import logging
        file_handler = logging.StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Rentalytics production startup')

class TestingConfig(Config):
    TESTING = True
    MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/rentalytics_dashboard_test')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
