import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost/airbnb_dashboard'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
