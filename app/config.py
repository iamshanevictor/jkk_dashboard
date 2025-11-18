import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    @classmethod
    def get_database_uri(cls):
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            # Replace postgresql:// with postgresql+psycopg:// to use psycopg driver
            if database_url.startswith('postgresql://'):
                database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)
        return database_url
    
    SQLALCHEMY_DATABASE_URI = None  # Will be set dynamically
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    
    @staticmethod
    def init_app(app):
        # Set the database URI dynamically
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_database_uri()

class DevelopmentConfig(Config):
    DEBUG = True
    
    @classmethod
    def get_database_uri(cls):
        database_url = os.environ.get('DATABASE_URL') or 'postgresql://localhost:5432/rentalytics_dashboard'
        # Replace postgresql:// with postgresql+psycopg:// to use psycopg driver
        if database_url.startswith('postgresql://'):
            database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)
        return database_url

class ProductionConfig(Config):
    DEBUG = False
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        # Log to stderr in production
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
