from flask import Blueprint, jsonify, render_template, request
from app.models import db, Property, PriceLog, Cluster
from datetime import datetime, timedelta
from sqlalchemy import func
import json

main = Blueprint('main', __name__)
data_entry_bp = Blueprint('data_entry_bp', __name__)
insights_bp = Blueprint('insights_bp', __name__)
management_bp = Blueprint('management_bp', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/insights')
def insights():
    return render_template('insights.html')

@main.route('/manage')
def manage():
    return render_template('manage.html')

# Data Entry Blueprint Routes
@data_entry_bp.route('/api/properties', methods=['GET'])
def get_properties_for_dropdown():
    properties = Property.query.with_entities(Property.unit_id, Property.cluster_id).all()
    return jsonify([{'unit_id': p.unit_id, 'cluster_id': p.cluster_id} for p in properties])

@data_entry_bp.route('/api/log-price', methods=['POST'])
def log_price():
    data = request.get_json()
    unit_id = data.get('unit_id')
    date_str = data.get('date')
    our_price = data.get('our_price')
    comp_avg_price = data.get('comp_avg_price')
    notes = data.get('notes')
    was_booked = data.get('was_booked', False) # Default to False if not provided
    final_price_paid = data.get('final_price_paid', None)

    if not all([unit_id, date_str, our_price, comp_avg_price]):
        return jsonify({'error': 'Missing required fields'}), 400

    property_obj = Property.query.filter_by(unit_id=unit_id).first()
    if not property_obj:
        return jsonify({'error': f'Property with unit_id {unit_id} not found'}), 404

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    new_log = PriceLog(
        property_id=property_obj.id,
        date=date_obj,
        our_listed_price=our_price,
        comp_avg_price=comp_avg_price,
        was_booked=was_booked,
        final_price_paid=final_price_paid,
        notes=notes
    )
    db.session.add(new_log)
    db.session.commit()

    return jsonify({'message': 'Price log recorded successfully', 'log_id': new_log.id}), 201

# Insights Blueprint Routes
@insights_bp.route('/api/insights/<string:cluster_name>', methods=['GET'])
def get_insights(cluster_name):
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    cluster = Cluster.query.filter_by(name=cluster_name).first()
    if not cluster:
        return jsonify({'error': f'Cluster {cluster_name} not found'}), 404

    cluster_properties = Property.query.filter_by(cluster_id=cluster.name).all()
    cluster_property_ids = [p.id for p in cluster_properties]

    if not cluster_property_ids:
        return jsonify({'message': f'No properties found for cluster {cluster_name}', 'insights': {}}), 200

    # Default date range to last 7 days if not provided
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=7)

    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid start_date format. Use YYYY-MM-DD'}), 400
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid end_date format. Use YYYY-MM-DD'}), 400

    # Get price logs for the selected date range and cluster
    recent_logs = PriceLog.query.filter(
        PriceLog.property_id.in_(cluster_property_ids),
        PriceLog.date.between(start_date, end_date)
    ).all()

    if not recent_logs:
        return jsonify({'message': 'No price logs found for this cluster and date range.', 'insights': {}}), 200

    # Calculations
    total_our_price = sum(log.our_listed_price for log in recent_logs)
    total_comp_price = sum(log.comp_avg_price for log in recent_logs)
    total_entries = len(recent_logs)
    booked_entries = sum(1 for log in recent_logs if log.was_booked)

    avg_our_price = total_our_price / total_entries if total_entries > 0 else 0
    avg_comp_price = total_comp_price / total_entries if total_entries > 0 else 0
    booking_rate = (booked_entries / total_entries) * 100 if total_entries > 0 else 0

    # Booking Rate by Day of the Week
    booking_by_day = {'Monday': {'booked': 0, 'total': 0},
                      'Tuesday': {'booked': 0, 'total': 0},
                      'Wednesday': {'booked': 0, 'total': 0},
                      'Thursday': {'booked': 0, 'total': 0},
                      'Friday': {'booked': 0, 'total': 0},
                      'Saturday': {'booked': 0, 'total': 0},
                      'Sunday': {'booked': 0, 'total': 0}}

    for log in recent_logs:
        day = log.day_of_week
        booking_by_day[day]['total'] += 1
        if log.was_booked:
            booking_by_day[day]['booked'] += 1

    booking_rate_by_day = {
        day: (data['booked'] / data['total'] * 100) if data['total'] > 0 else 0
        for day, data in booking_by_day.items()
    }

    # Missed Opportunities
    missed_opportunities = []
    for log in recent_logs:
        if log.our_listed_price < (log.comp_avg_price * 0.90) and not log.was_booked:
            missed_opportunities.append({
                'date': log.date.isoformat(),
                'unit_id': log.property.unit_id,
                'our_price': log.our_listed_price,
                'comp_avg_price': log.comp_avg_price
            })

    # Data for Chart.js (Price Comparison)
    chart_data = [
        {
            'date': log.date.isoformat(),
            'our_price': log.our_listed_price,
            'comp_price': log.comp_avg_price
        } for log in sorted(recent_logs, key=lambda x: x.date)
    ]

    insights_data = {
        'avg_our_price': round(avg_our_price, 2),
        'avg_comp_price': round(avg_comp_price, 2),
        'booking_rate': round(booking_rate, 2),
        'booking_rate_by_day': booking_rate_by_day,
        'missed_opportunities': missed_opportunities,
        'chart_data': chart_data,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    }

    return jsonify({'insights': insights_data}), 200

# Management Blueprint Routes
@management_bp.route('/api/clusters', methods=['GET', 'POST'])
def handle_clusters():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', None)
        competitor_urls_str = data.get('competitor_urls', None)

        if not name:
            return jsonify({'error': 'Cluster name is required'}), 400

        if Cluster.query.filter_by(name=name).first():
            return jsonify({'error': f'Cluster with name {name} already exists'}), 409
        
        competitor_urls = json.loads(competitor_urls_str) if competitor_urls_str else None

        new_cluster = Cluster(name=name, description=description, competitor_urls=competitor_urls)
        db.session.add(new_cluster)
        db.session.commit()
        return jsonify({'message': 'Cluster created successfully', 'cluster': new_cluster.to_dict()}), 201

    # GET request
    clusters = Cluster.query.all()
    return jsonify([c.to_dict() for c in clusters])

@management_bp.route('/api/clusters/<int:cluster_id>', methods=['PUT', 'DELETE'])
def handle_single_cluster(cluster_id):
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        return jsonify({'error': 'Cluster not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        cluster.name = data.get('name', cluster.name)
        cluster.description = data.get('description', cluster.description)
        competitor_urls_str = data.get('competitor_urls', None)
        cluster.competitor_urls = json.loads(competitor_urls_str) if competitor_urls_str else cluster.competitor_urls
        db.session.commit()
        return jsonify({'message': 'Cluster updated successfully', 'cluster': cluster.to_dict()})

    if request.method == 'DELETE':
        db.session.delete(cluster)
        db.session.commit()
        return jsonify({'message': 'Cluster deleted successfully'}), 204

@management_bp.route('/api/properties/all', methods=['GET'])
def get_all_properties():
    properties = Property.query.all()
    return jsonify([p.to_dict() for p in properties])

@management_bp.route('/api/properties', methods=['POST'])
def add_property():
    data = request.get_json()
    unit_id = data.get('unit_id')
    property_name = data.get('property_name')
    bedrooms = data.get('bedrooms')
    bathrooms = data.get('bathrooms')
    max_guests = data.get('max_guests')
    amenities = data.get('amenities', None)
    quality_keywords = data.get('quality_keywords', None)
    cluster_id = data.get('cluster_id')

    if not all([unit_id, property_name, bedrooms, bathrooms, max_guests, cluster_id]):
        return jsonify({'error': 'Missing required property fields'}), 400

    if Property.query.filter_by(unit_id=unit_id).first():
        return jsonify({'error': f'Property with unit_id {unit_id} already exists'}), 409

    # Check if cluster_id exists
    if not Cluster.query.filter_by(name=cluster_id).first():
        return jsonify({'error': f'Cluster with name {cluster_id} does not exist'}), 400

    new_property = Property(
        unit_id=unit_id,
        property_name=property_name,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        max_guests=max_guests,
        amenities=amenities,
        quality_keywords=quality_keywords,
        cluster_id=cluster_id
    )
    db.session.add(new_property)
    db.session.commit()
    return jsonify({'message': 'Property added successfully', 'property': new_property.to_dict()}), 201

@management_bp.route('/api/properties/<int:property_id>', methods=['PUT', 'DELETE'])
def handle_single_property(property_id):
    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({'error': 'Property not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        prop.unit_id = data.get('unit_id', prop.unit_id)
        prop.property_name = data.get('property_name', prop.property_name)
        prop.bedrooms = data.get('bedrooms', prop.bedrooms)
        prop.bathrooms = data.get('bathrooms', prop.bathrooms)
        prop.max_guests = data.get('max_guests', prop.max_guests)
        prop.amenities = data.get('amenities', prop.amenities)
        prop.quality_keywords = data.get('quality_keywords', prop.quality_keywords)
        new_cluster_id = data.get('cluster_id', prop.cluster_id)

        if new_cluster_id != prop.cluster_id:
            if not Cluster.query.filter_by(name=new_cluster_id).first():
                return jsonify({'error': f'Cluster with name {new_cluster_id} does not exist'}), 400
            prop.cluster_id = new_cluster_id

        db.session.commit()
        return jsonify({'message': 'Property updated successfully', 'property': prop.to_dict()})

    if request.method == 'DELETE':
        db.session.delete(prop)
        db.session.commit()
        return jsonify({'message': 'Property deleted successfully'}), 204
