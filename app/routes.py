from flask import Blueprint, jsonify, render_template
from app.models import Property

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/property-performance')
def property_performance():
    properties = Property.query.all()
    return jsonify([p.to_dict() for p in properties])
