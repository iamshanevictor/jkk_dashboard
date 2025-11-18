from flask import Blueprint, jsonify, render_template, request
from marshmallow import Schema, fields, ValidationError
from app.models import Property, PriceLog, Cluster
from datetime import datetime, timedelta
from mongoengine import Q
import json

# Validation schemas
class PriceLogSchema(Schema):
    unit_id = fields.Str(required=True, validate=lambda x: len(x) <= 50)
    date = fields.Date(required=True)
    our_price = fields.Float(required=True, validate=lambda x: x > 0)
    comp_avg_price = fields.Float(required=True, validate=lambda x: x >= 0)
    notes = fields.Str(missing='', validate=lambda x: len(x) <= 1000)
    was_booked = fields.Bool(missing=False)
    final_price_paid = fields.Float(allow_none=True, validate=lambda x: x is None or x > 0)

class QuickLogSchema(Schema):
    unit_id = fields.Str(required=True, validate=lambda x: len(x) <= 50)
    date = fields.Date(required=True)
    listed_price = fields.Float(required=True, validate=lambda x: x > 0)
    was_booked = fields.Str(required=True, validate=lambda x: x in ['Y', 'N'])
    # lead_time will be calculated automatically, so we don't need it in the schema

main = Blueprint('main', __name__)
data_entry_bp = Blueprint('data_entry_bp', __name__)
insights_bp = Blueprint('insights_bp', __name__)
management_bp = Blueprint('management_bp', __name__)


def generate_unit_id():
    counter = Property.objects.count() + 1
    while True:
        candidate = f"UNIT_{counter:04d}"
        if not Property.objects(unit_id=candidate).first():
            return candidate
        counter += 1

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/insights')
def insights():
    return render_template('insights.html')

@main.route('/manage')
def manage():
    return render_template('manage.html')

# New route for data entry form
@main.route('/log_entry', methods=['GET', 'POST'])
def log_entry():
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data provided'}), 400
                
            unit_id = data.get('unit_id')
            date_str = data.get('date')
            our_listed_price = data.get('listed_price')
            was_booked_raw = data.get('was_booked')
            was_booked = was_booked_raw == 'Y' if was_booked_raw else False
            
            # Debug logging
            print(f"Received data: {data}")
            
        except Exception as e:
            return jsonify({'error': f'Invalid JSON data: {str(e)}'}), 400

        if not all([unit_id, date_str, our_listed_price]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if data.get('was_booked') is None:
            return jsonify({'error': 'Booking status is required'}), 400

        property_obj = Property.objects(unit_id=unit_id).first()
        if not property_obj:
            return jsonify({'error': f'Property with unit_id {unit_id} not found'}), 404

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        # Lead time will be calculated automatically by the model

        try:
            new_log = PriceLog(
                property=property_obj,
                date=date_obj,
                our_listed_price=our_listed_price,
                was_booked=was_booked,
                # lead_time and day_of_week will be calculated automatically by the model
                # For simplicity, comp_avg_price and final_price_paid are omitted as they are not in the new form spec.
                # They can be added back if needed in the future or handled as part of the original log-price route.
                comp_avg_price=0.0, # Default value
                final_price_paid=our_listed_price if was_booked else None
            )
            new_log.save()

            return jsonify({'message': 'Price log entry created successfully'}), 201
            
        except Exception as e:
            print(f"Database error: {str(e)}")
            return jsonify({'error': f'Database error: {str(e)}'}), 500
    
    properties = Property.objects.only('unit_id', 'property_name').all()
    units = [
        {
            'unit_id': p.unit_id,
            'property_name': p.property_name
        } for p in properties
    ]
    return render_template('data_entry.html', units=units)


@main.route('/dashboard')
def dashboard():
    # Fetch all PriceLog entries, ordered by date descending
    price_logs = PriceLog.objects.order_by('-date').all()

    # Calculate summary statistics
    total_entries = len(price_logs)
    booked_entries = sum(1 for log in price_logs if log.was_booked)
    not_booked_entries = total_entries - booked_entries

    total_listed_price = sum(log.our_listed_price for log in price_logs)
    avg_listed_price = (total_listed_price / total_entries) if total_entries > 0 else 0

    # Prepare data for rendering
    dashboard_data = [
        {
            'id': str(log.id),
            'date': log.date.isoformat(),
            'unit_id': log.property.unit_id,
            'listed_price': log.our_listed_price,
            'was_booked': 'Yes' if log.was_booked else 'No',
            'lead_time': log.lead_time if log.lead_time is not None else '-',
            'day_of_week': log.day_of_week
        } for log in price_logs
    ]

    summary_stats = {
        'total_entries': total_entries,
        'booked_entries': booked_entries,
        'not_booked_entries': not_booked_entries,
        'avg_listed_price': round(avg_listed_price, 2)
    }

    return render_template('dashboard.html', dashboard_data=dashboard_data, summary_stats=summary_stats)


# Data Entry Blueprint Routes
@data_entry_bp.route('/api/properties', methods=['GET'])
def get_properties_for_dropdown():
    properties = Property.objects.only('unit_id').all()
    return jsonify([{'unit_id': p.unit_id} for p in properties])

@data_entry_bp.route('/api/unit-bookings/<string:unit_id>', methods=['GET'])
def get_unit_bookings(unit_id):
    """Get existing booking data for a specific unit"""
    property_obj = Property.objects(unit_id=unit_id).first()
    if not property_obj:
        return jsonify({'error': f'Property with unit_id {unit_id} not found'}), 404
    
    # Get all price logs for this property
    price_logs = PriceLog.objects(property=property_obj).all()
    
    bookings = []
    for log in price_logs:
        bookings.append({
            'date': log.date.isoformat(),
            'our_listed_price': log.our_listed_price,
            'was_booked': log.was_booked,
            'lead_time': log.lead_time
        })
    
    return jsonify(bookings)

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

    property_obj = Property.objects(unit_id=unit_id).first()
    if not property_obj:
        return jsonify({'error': f'Property with unit_id {unit_id} not found'}), 404

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    new_log = PriceLog(
        property=property_obj,
        date=date_obj,
        our_listed_price=our_price,
        comp_avg_price=comp_avg_price,
        was_booked=was_booked,
        final_price_paid=final_price_paid,
        notes=notes
    )
    new_log.save()

    return jsonify({'message': 'Price log recorded successfully', 'log_id': new_log.id}), 201

# Insights Blueprint Routes
@insights_bp.route('/api/insights/<string:unit_id>', methods=['GET'])
def get_insights(unit_id):
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    # Find the property by unit_id
    property_obj = Property.objects(unit_id=unit_id).first()
    if not property_obj:
        return jsonify({'error': f'Property with unit_id {unit_id} not found'}), 404

    # Initialize query to fetch all logs for this property
    logs_query = PriceLog.objects(property=property_obj)

    # Apply date range filter only if provided
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            logs_query = logs_query.filter(date__gte=start_date, date__lte=end_date)
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    else:
        # If no dates provided, get the min/max dates from available logs for display purposes
        min_date_log = logs_query.order_by('date').first()
        max_date_log = logs_query.order_by('-date').first()
        start_date = min_date_log.date if min_date_log else None
        end_date = max_date_log.date if max_date_log else None


    recent_logs = logs_query.all()

    if not recent_logs:
        return jsonify({'message': 'No price logs found for this property and date range.', 'insights': {}}), 200

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
        'start_date': start_date.isoformat() if start_date else None,
        'end_date': end_date.isoformat() if end_date else None
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

        if Cluster.objects(name=name).first():
            return jsonify({'error': f'Cluster with name {name} already exists'}), 409
        
        competitor_urls = json.loads(competitor_urls_str) if competitor_urls_str else None

        new_cluster = Cluster(name=name, description=description, competitor_urls=competitor_urls)
        new_cluster.save()
        return jsonify({'message': 'Cluster created successfully', 'cluster': new_cluster.to_dict()}), 201

    # GET request
    clusters = Cluster.objects.all()
    return jsonify([c.to_dict() for c in clusters])

@management_bp.route('/api/clusters/<string:cluster_id>', methods=['PUT', 'DELETE'])
def handle_single_cluster(cluster_id):
    cluster = Cluster.objects(id=cluster_id).first()
    if not cluster:
        return jsonify({'error': 'Cluster not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        cluster.name = data.get('name', cluster.name)
        cluster.description = data.get('description', cluster.description)
        competitor_urls_str = data.get('competitor_urls', None)
        cluster.competitor_urls = json.loads(competitor_urls_str) if competitor_urls_str else cluster.competitor_urls
        cluster.save()
        return jsonify({'message': 'Cluster updated successfully', 'cluster': cluster.to_dict()})

    if request.method == 'DELETE':
        cluster.delete()
        return jsonify({'message': 'Cluster deleted successfully'}), 204

@management_bp.route('/api/properties/all', methods=['GET'])
def get_all_properties():
    properties = Property.objects.all()
    return jsonify([p.to_dict() for p in properties])

@management_bp.route('/api/properties', methods=['POST'])
def add_property():
    data = request.get_json()
    property_name = data.get('property_name')
    bedrooms = data.get('bedrooms')
    bathrooms = data.get('bathrooms')
    max_guests = data.get('max_guests')
    amenities = data.get('amenities', None)
    quality_keywords = data.get('quality_keywords', None)

    if not all([property_name, bedrooms, bathrooms, max_guests]):
        return jsonify({'error': 'Missing required property fields'}), 400

    unit_id = generate_unit_id()
    if Property.objects(unit_id=unit_id).first():
        return jsonify({'error': f'Property with unit_id {unit_id} already exists'}), 409

    new_property = Property(
        unit_id=unit_id,
        property_name=property_name,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        max_guests=max_guests,
        amenities=amenities,
        quality_keywords=quality_keywords
    )
    new_property.save()
    return jsonify({'message': 'Property added successfully', 'property': new_property.to_dict()}), 201

@management_bp.route('/api/properties/<string:property_id>', methods=['PUT', 'DELETE'])
def handle_single_property(property_id):
    prop = Property.objects(id=property_id).first()
    if not prop:
        return jsonify({'error': 'Property not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        prop.property_name = data.get('property_name', prop.property_name)
        prop.bedrooms = data.get('bedrooms', prop.bedrooms)
        prop.bathrooms = data.get('bathrooms', prop.bathrooms)
        prop.max_guests = data.get('max_guests', prop.max_guests)
        prop.amenities = data.get('amenities', prop.amenities)
        prop.quality_keywords = data.get('quality_keywords', prop.quality_keywords)

        prop.save()
        return jsonify({'message': 'Property updated successfully', 'property': prop.to_dict()})

    if request.method == 'DELETE':
        prop.delete()
        return jsonify({'message': 'Property deleted successfully'}), 204

@data_entry_bp.route('/api/delete-booking/<string:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    """Delete a booking entry from the database"""
    try:
        # Find the booking entry
        booking = PriceLog.objects(id=booking_id).first()
        if not booking:
            return jsonify({'error': 'Booking entry not found'}), 404

        # Delete the booking
        booking.delete()
        return jsonify({'message': 'Booking deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': f'Failed to delete booking: {str(e)}'}), 500

@data_entry_bp.route('/api/reset-database', methods=['POST'])
def reset_database():
    """Reset the database schema (emergency use only)"""
    try:
        print("Manual database reset initiated...")
        # Drop all collections
        from app.models import Cluster, Property, PriceLog
        
        # Drop all documents in each collection
        Cluster.drop_collection()
        Property.drop_collection()
        PriceLog.drop_collection()
        
        # Recreate indexes
        Cluster.ensure_indexes()
        Property.ensure_indexes()
        PriceLog.ensure_indexes()
        
        return jsonify({'message': 'Database reset successfully!'}), 200
    except Exception as e:
        print(f"Error resetting database: {str(e)}")
        return jsonify({'error': f'Failed to reset database: {str(e)}'}), 500
