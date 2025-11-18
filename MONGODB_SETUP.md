# MongoDB Setup Guide for Rentalytics

## Quick Setup for Local MongoDB

### 1. Install MongoDB (if not already installed)

#### Option A: MongoDB Community Server (Recommended)
1. Download from: https://www.mongodb.com/try/download/community
2. Run the installer
3. Choose "Complete" installation
4. Install MongoDB Compass (included in installer)
5. Keep "Install MongoDB as a Windows Service" checked

#### Option B: Using Chocolatey (if you have it)
```bash
choco install mongodb
choco install mongodb-compass
```

### 2. Start MongoDB Service

#### Method 1: Using Services (Recommended)
1. Open Windows Services (Win+R, type `services.msc`)
2. Find "MongoDB" service
3. Right-click → Start (if not running)
4. Set Startup Type to "Automatic"

#### Method 2: Using Command Line
```bash
# Start MongoDB service
net start MongoDB

# Stop MongoDB service
net stop MongoDB
```

### 3. Connect with MongoDB Compass

1. Open MongoDB Compass (from Start Menu)
2. Use this connection string:
   ```
   mongodb://localhost:27017/
   ```
3. Click "Connect"
4. You should see the connection screen

### 4. Create the Database in Compass

1. In Compass, click "Create Database"
2. Database name: `rentalytics_dashboard_dev`
3. Collection name: `test` (temporary)
4. Click "Create Database"
5. You can delete the `test` collection later

### 5. Verify Connection in Your App

Run the test script:
```bash
.venv/Scripts/activate
python test_mongo.py
```

You should see: "🎉 All tests passed! MongoDB integration is working correctly."

### 6. Seed the Database

```bash
.venv/Scripts/activate
python seed.py
```

### 7. Run the Application

```bash
.venv/Scripts/activate
python -m flask run --host=0.0.0.0 --port=5000
```

## Troubleshooting

### "Connection refused" or "Can't connect"
- Make sure MongoDB service is running (check services.msc)
- Try restarting MongoDB service
- Check if port 27017 is blocked by firewall

### "Authentication failed"
- Default MongoDB installation doesn't require authentication
- If you set up authentication, update your connection string:
  ```
  mongodb://username:password@localhost:27017/rentalytics_dashboard_dev
  ```

### In Compass shows "No databases"
- Click the "+" button to create a database
- Name it `rentalytics_dashboard_dev`
- Or just run `python seed.py` - it will create the database automatically

## What You'll See in Compass

After running the app and seed script, Compass will show:

**Database: `rentalytics_dashboard_dev`**
- Collections:
  - `clusters` - Property groupings
  - `properties` - Individual rental units  
  - `price_logs` - Daily pricing data

You can click on any collection to view, edit, or add documents directly in Compass!

## Environment Variables

Your `.env` file should contain:
```env
MONGODB_URI=mongodb://localhost:27017/rentalytics_dashboard_dev
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-local-dev-secret-key-change-this
```

## Production (MongoDB Atlas)

For production, consider using MongoDB Atlas:
1. Create free account at https://www.mongodb.com/atlas
2. Create a free cluster
3. Get connection string
4. Update your `.env` with the Atlas connection string
5. Add your IP to the whitelist in Atlas dashboard
