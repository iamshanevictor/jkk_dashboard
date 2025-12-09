# Rentalytics - Vacation Rental Pricing Analytics Dashboard

Flask + PostgreSQL dashboard for property pricing, competitor tracking, and booking insights. Built for Airbnb/Vrbo/Booking.com style rentals.

## Features
- Property + cluster management
- Daily price/booking logging with lead-time and weekday auto-calculation
- Insights: booking rate, price comparisons, missed opportunities
- Admin endpoints for clusters/properties and emergency DB reset

## Tech Stack
- Backend: Python 3.11, Flask 3, SQLAlchemy + Flask-Migrate
- Database: PostgreSQL (local or cloud)
- Frontend: HTML5, Tailwind CSS, Chart.js
- Deployment: Render (Web Service + Render PostgreSQL)

## Quick Start (Local)
1) Install prerequisites: Python 3.11+, PostgreSQL 14+.
2) Clone & install deps:
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```
3) Create a Postgres DB (example `airbnb_dashboard`).
4) Copy env and set `DATABASE_URL`:
```bash
cp .env.example .env
# edit .env
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/airbnb_dashboard
SECRET_KEY=generate-a-secret
```
5) Seed sample data:
```bash
python seed.py
```
6) Run the app:
```bash
flask run
```
Visit http://127.0.0.1:5000/

## pgAdmin 4 setup (local)
- Create a new server: host `localhost`, port `5432`, username/password you set.
- Create database `airbnb_dashboard` (or match your `DATABASE_URL`).
- You do not need to create tables manually; `seed.py` or first app start will create them.

## Deployment (Render)
- Render will inject `DATABASE_URL` for the attached PostgreSQL instance.
- Build: `pip install -r requirements.txt`
- Start: `gunicorn wsgi:app`
- Set `SECRET_KEY` in Render env vars.

## Environment Variables
```
DATABASE_URL=postgresql://user:password@host:5432/airbnb_dashboard
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
```

## Database Schema (SQLAlchemy)
- Cluster: id, name (unique), description, competitor_urls (JSON)
- Property: id, unit_id (unique), property_name, bedrooms, bathrooms, max_guests, amenities, quality_keywords, cluster_id (FK)
- PriceLog: id, date, property_id (FK), our_listed_price, comp_avg_price, was_booked, final_price_paid, notes, day_of_week, lead_time

Relationships: Cluster 1–N Properties, Property 1–N PriceLogs.

## API Endpoints
- POST `/api/log-price` – add price log
- GET `/api/properties` – dropdown data
- DELETE `/api/delete-booking/<id>` – delete log
- GET `/api/insights/<unit_id>` – analytics with optional `start_date`/`end_date`
- GET/POST `/api/clusters`
- PUT/DELETE `/api/clusters/<cluster_id>`
- GET `/api/properties/all`
- POST `/api/properties`
- PUT/DELETE `/api/properties/<property_id>`
- POST `/api/reset-database` – drop & recreate tables (emergency)

## Maintenance
- Reset DB: `python init_db.py` (drops & recreates tables)
- Reseed sample data: `python seed.py`

## Security
- Secrets via env vars
- SQLAlchemy ORM to avoid SQL injection
- Basic security headers enabled

