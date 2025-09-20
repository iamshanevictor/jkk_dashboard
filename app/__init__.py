import os
from flask import Flask
from app.config import Config
from app.models import db

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import main as main_blueprint, data_entry_bp, insights_bp, management_bp
    app.register_blueprint(main_blueprint)
    app.register_blueprint(data_entry_bp)
    app.register_blueprint(insights_bp)
    app.register_blueprint(management_bp)

    with app.app_context():
        db.create_all()

    return app
