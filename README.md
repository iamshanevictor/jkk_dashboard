# Rentalytics - Vacation Rental Pricing Analytics Dashboard

A universal Flask-based dashboard for managing vacation rental property pricing data, competitor analysis, and booking insights. Perfect for Airbnb, Vrbo, Booking.com, and other short-term rental platforms.

## Features

- **Property Management**: Manage property clusters and individual units
- **Price Logging**: Track daily pricing decisions and booking outcomes  
- **Analytics Dashboard**: View pricing trends, booking rates, and missed opportunities
- **Competitor Analysis**: Compare pricing against competitor averages
- **Insights by Cluster**: Analyze performance by property groupings

## Tech Stack

- **Backend**: Python 3.11, Flask 2.3.3, SQLAlchemy 2.0.23
- **Database**: PostgreSQL 13+
- **Frontend**: HTML5, Tailwind CSS, Chart.js
- **Deployment**: Render (Web Service + PostgreSQL)

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (local development)
- Git

### Local Development Setup

1. **Clone and navigate to project**:
   ```bash
   git clone <repository-url>
   cd airbnb_dashboard
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your local database credentials
   ```

3. **Install dependencies**:
   ```bash
   make install
   ```

4. **Set up database**:
   ```bash
   make migrate
   make seed
   ```

5. **Run the application**:
   ```bash
   make dev
   ```

6. **Visit**: http://localhost:5000

### Environment Variables

Create a `.env` file with:

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/rentalytics_dashboard
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

### Database Inspection

Use pgAdmin4 to inspect the local database:
- Host: `localhost`
- Port: `5432`
- Database: `rentalytics_dashboard`
- Username/Password: From your `DATABASE_URL`

## Deployment

### Render Setup

1. **Create Render services**:
   - Web Service: Connect to this repository
   - PostgreSQL Database: Create and attach to web service

2. **Configure environment variables in Render**:
   - `FLASK_ENV=production`
   - `SECRET_KEY=<generate-secure-key>`
   - `DATABASE_URL` (auto-injected by Render)

3. **Deploy**: Push to main branch triggers automatic deployment

### Production Commands

The render.yaml file configures:
- Build: `pip install -r requirements.txt`
- Start: `flask db upgrade && gunicorn wsgi:app`
- Health Check: `/`

## API Endpoints

### Data Entry
- `POST /api/log-price` - Log price entry
- `GET /api/properties` - Get properties for dropdown

### Insights  
- `GET /api/insights/<cluster_name>` - Get cluster analytics

### Management
- `GET/POST /api/clusters` - Manage clusters
- `GET/POST /api/properties/all` - Manage properties

## Database Schema

### Core Models
- **Cluster**: Property groupings (e.g., LUXURY_2BR, BEACH_1BR)
- **Property**: Individual rental units with characteristics
- **PriceLog**: Daily pricing decisions and outcomes

### Relationships
- Cluster → Properties (one-to-many)
- Property → PriceLogs (one-to-many)

## Development Commands

```bash
make install    # Set up virtual environment and install dependencies
make dev        # Start development server
make migrate    # Apply database migrations
make seed       # Seed database with sample data
make clean      # Clean up generated files
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test manually
4. Submit a pull request

## Security

- All secrets managed via environment variables
- Security headers enabled (XSS, CSRF, etc.)
- Input validation using marshmallow schemas
- Database queries use SQLAlchemy ORM (prevents SQL injection)

## License

[Add your license here]
