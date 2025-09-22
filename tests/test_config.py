import os
import pytest
from app.config import config, DevelopmentConfig, ProductionConfig

def test_config_classes_exist():
    """Test that config classes are properly defined"""
    assert 'development' in config
    assert 'production' in config
    assert 'default' in config

def test_development_config():
    """Test development configuration"""
    dev_config = DevelopmentConfig()
    assert dev_config.DEBUG is True
    assert dev_config.SQLALCHEMY_TRACK_MODIFICATIONS is False

def test_production_config():
    """Test production configuration"""
    prod_config = ProductionConfig()
    assert prod_config.DEBUG is False
    assert prod_config.SQLALCHEMY_TRACK_MODIFICATIONS is False

def test_config_from_environment():
    """Test that config loads from environment variables"""
    os.environ['SECRET_KEY'] = 'test-secret-key'
    dev_config = DevelopmentConfig()
    assert dev_config.SECRET_KEY == 'test-secret-key'
    del os.environ['SECRET_KEY']
