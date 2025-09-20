from app import create_app

app = create_app()

if __name__ == '__main__':
    # Phase 1 - Precision Pricing Initiative CMS Testing Instructions:
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
    # 5. Seed the database with initial Cluster and Property data:
    #    (Ensure your virtual environment is activated and DATABASE_URL is set)
    #    python seed.py
    #    This will drop all existing tables, recreate them, and add sample clusters and properties.
    # 6. Run the Flask application:
    #    flask run
    # 7. Open your web browser and visit http://127.0.0.1:5000/
    #    - On the "Quick Log" page, select a Unit ID, enter date, prices, and notes, then click "Log Entry".
    #    - Submit several days of fake data for both UNIT_A and UNIT_B.
    # 8. Navigate to http://127.0.0.1:5000/insights
    #    - Select a Cluster ID from the dropdown and optionally a date range.
    #    - Verify that the average prices, booking rate, booking rate by day, missed opportunities, and the price comparison chart render correctly.
    # 9. Navigate to http://127.0.0.1:5000/manage
    #    - Verify that you can view the seeded clusters and properties.
    #    - Test adding new clusters and properties, and observe the tables update.
    #    - (Note: Edit/Delete functionality for tables is not fully implemented in frontend JS for this phase, but backend endpoints exist.)
    app.run()
