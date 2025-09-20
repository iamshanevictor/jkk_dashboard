from app import create_app

app = create_app()

if __name__ == '__main__':
    # Testing Instructions:
    # 1. Create a PostgreSQL database locally (e.g., named 'airbnb_dashboard').
    # 2. Set the DATABASE_URL environment variable:
    #    For Windows: $env:DATABASE_URL="postgresql://user:password@localhost/airbnb_dashboard"
    #    For Linux/macOS: export DATABASE_URL="postgresql://user:password@localhost/airbnb_dashboard"
    #    Replace 'user', 'password', and 'localhost' with your PostgreSQL credentials and host.
    # 3. Create a Python virtual environment:
    #    python -m venv .venv
    #    Activate it:
    #    For Windows: .venv\Scripts\activate
    #    For Linux/macOS: source .venv/bin/activate
    # 4. Install dependencies:
    #    pip install -r requirements.txt
    # 5. Initialize the database and insert sample data:
    #    (Ensure your virtual environment is activated)
    #    python
    #    >>> from app import create_app
    #    >>> from app.models import db, Property
    #    >>> app = create_app()
    #    >>> with app.app_context():
    #    ...     db.create_all()
    #    ...     prop1 = Property(name='Cozy Studio', occupancy_rate=0.85, revenue=1500.00)
    #    ...     prop2 = Property(name='Luxury Villa', occupancy_rate=0.70, revenue=5000.00)
    #    ...     prop3 = Property(name='Downtown Apartment', occupancy_rate=0.92, revenue=2200.00)
    #    ...     db.session.add_all([prop1, prop2, prop3])
    #    ...     db.session.commit()
    #    ...     print("Sample data inserted.")
    #    ...     exit()
    # 6. Run the Flask application:
    #    flask run
    # 7. Open your web browser and visit http://127.0.0.1:5000/ to see the chart rendered with sample data.
    app.run()
