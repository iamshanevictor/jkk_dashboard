import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            # Replace postgresql:// with postgresql+psycopg:// to use psycopg driver
            if database_url.startswith('postgresql://'):
                database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)
        return database_url
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        database_url = os.environ.get('DATABASE_URL') or 'postgresql://localhost:5432/airbnb_dashboard'
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
