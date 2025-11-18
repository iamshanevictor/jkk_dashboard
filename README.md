# Rentalytics - Vacation Rental Pricing Analytics Dashboard

A universal Flask-based dashboard for managing vacation rental property pricing data, competitor analysis, and booking insights. Perfect for Airbnb, Vrbo, Booking.com, and other short-term rental platforms.

## Features

- **Property Management**: Organize rental properties by clusters with detailed specifications
- **Price Logging**: Track daily pricing, booking status, and competitor pricing
- **Analytics Dashboard**: Visualize booking rates, pricing trends, and missed opportunities
- **Data Entry**: Easy-to-use forms for logging daily pricing and booking data
- **Management Interface**: Add/edit properties and clusters through a web interface

## Tech Stack

- **Backend**: Python 3.11, Flask 3.0.0, MongoEngine 0.28.2
- **Database**: MongoDB 5.0+
- **Frontend**: HTML5, Tailwind CSS, Chart.js
- **Deployment**: Render (Web Service + MongoDB)

## What's Changed

- Rebranded project to Rentalytics (universal vacation rental branding)
- Migrated database from PostgreSQL (SQLAlchemy) to MongoDB (MongoEngine)
- Removed pytest test suite and SQL migrations (Flask-Migrate)
- Updated routes and models to use MongoDB documents and queries
- Added seed script and MongoDB setup guide

## Quick Start

### Prerequisites

- Python 3.11+
- MongoDB 5.0+ (local installation or MongoDB Atlas account)
- Node.js 16+ (for Tailwind CSS compilation)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd jkk_dashboard
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up MongoDB**
   - **Local MongoDB**: Install MongoDB Community Server and start the service
   - **MongoDB Atlas**: Create a free cluster and get your connection string

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB connection string
   ```

5. **Initialize the database**
   ```bash
   python seed.py
   ```

6. **Run the development server**
   ```bash
   python -m flask run --host=0.0.0.0 --port=5000
   ```

7. **Open your browser**
   Navigate to `http://localhost:5000`

### Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
MONGODB_URI=mongodb://localhost:27017/rentalytics_dashboard_dev

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Render Production (set in Render dashboard)
# MONGODB_URI will be auto-injected by Render MongoDB
```

### MongoDB Setup Options

See the detailed guide: [MONGODB_SETUP.md](./MONGODB_SETUP.md)

#### Option 1: Local MongoDB
1. Install MongoDB Community Server
2. Start MongoDB service
3. Use the default connection string: `mongodb://localhost:27017/rentalytics_dashboard_dev`

#### Option 2: MongoDB Atlas
1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Get your connection string from the Atlas dashboard
4. Add your IP address to the whitelist
5. Use the Atlas connection string in your `.env` file

## Deployment

### Deploy to Render
1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Create Render Web Service**
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn wsgi:app`

3. **Add MongoDB Add-on**
   - In your Render dashboard, add the MongoDB add-on
   - The `MONGODB_URI` environment variable will be automatically injected

4. **Environment Variables**
   - Set `FLASK_ENV=production`
   - Set `SECRET_KEY` to a secure random string

### Manual Deployment

For other platforms, ensure:
- MongoDB is accessible from your application
- Set `MONGODB_URI` environment variable
- Install Python dependencies from `requirements.txt`
- Use a WSGI server like Gunicorn for production

### Render Setup

1. **Create Render services**:
   - Web Service: Connect to this repository
   - MongoDB Database: Create and attach to web service

2. **Configure environment variables in Render**:
   - `FLASK_ENV=production`
   - `SECRET_KEY=<generate-secure-key>`
   - `MONGODB_URI` (auto-injected by Render)

3. **Deploy**: Push to main branch triggers automatic deployment

### Production Commands

The render.yaml file configures:
- Build: `pip install -r requirements.txt`
- Start: `gunicorn wsgi:app`
- Health Check: `/`

## API Endpoints

### Data Entry
- `POST /api/log-price` - Log price entry
- `GET /api/properties` - Get properties for dropdown
- `DELETE /api/delete-booking/<booking_id>` - Delete a price/booking log by ID

### Insights  
- `GET /api/insights/<unit_id>` - Get per-unit analytics (date filtering supported via `start_date`/`end_date` query params)

### Management - Clusters
- `GET /api/clusters` - List clusters
- `POST /api/clusters` - Create cluster
- `PUT /api/clusters/<cluster_id>` - Update cluster
- `DELETE /api/clusters/<cluster_id>` - Delete cluster

### Management - Properties
- `GET /api/properties/all` - List all properties
- `POST /api/properties` - Create property
- `PUT /api/properties/<property_id>` - Update property
- `DELETE /api/properties/<property_id>` - Delete property

### Utilities
- `POST /api/reset-database` - Drops collections and recreates indexes (emergency use only)

## Database Schema

### Core Models
- **Cluster**: Property groupings (e.g., LUXURY_2BR, BEACH_1BR)
- **Property**: Individual rental units with characteristics
- **PriceLog**: Daily pricing decisions and outcomes

### Relationships
- Cluster → Properties (one-to-many)
- Property → PriceLogs (one-to-many)

## Development

### Available Commands

```bash
make install    # Set up virtual environment and install dependencies
make dev        # Start development server
make seed       # Seed database with sample data
make clean      # Clean up generated files
```

### Database Operations

- **Seed data**: `python seed.py`
- **Reset database**: Use the `/api/reset-database` endpoint (emergency use only)
- **View data**: Use MongoDB Compass or the MongoDB Atlas UI to inspect collections

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test manually
4. Submit a pull request

## Security

- All secrets managed via environment variables
- Security headers enabled (XSS, CSRF, etc.)
- Input validation using marshmallow schemas
- Database queries use MongoEngine ODM (prevents NoSQL injection)

## License

[Add your license here]
