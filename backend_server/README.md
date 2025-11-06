# Backend Server

## Overview
Express.js backend server with MongoDB integration using ES6 modules.

## Features
- ✅ Express.js server
- ✅ MongoDB connection with Mongoose
- ✅ CORS enabled for frontend communication
- ✅ Environment variables with dotenv
- ✅ ES6 import/export syntax

## Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Environment Variables
Create a `.env` file with:
```
mongo_url = your_mongodb_connection_string
Port = 5050
```

### 3. Start Server
```bash
npm start
# or
npm run dev
```

## API Endpoints

### Root Endpoint
- **GET** `/`
- Returns server status and timestamp

### Health Check
- **GET** `/api/health`
- Returns health status of server and database

### Test Endpoint
- **GET** `/api/test`
- Tests frontend-backend connection
- Returns server info and database status

## Project Structure
```
backend_server/
├── index.js          # Main server file
├── db.js             # MongoDB connection
├── models/           # Mongoose models (empty for now)
├── scripts/          # Utility scripts (empty for now)
├── .env              # Environment variables
└── package.json      # Dependencies and scripts
```

## Technologies
- **Express.js** - Web framework
- **Mongoose** - MongoDB ODM
- **CORS** - Cross-origin resource sharing
- **dotenv** - Environment variable management

## Notes
- Server runs on port 5050 by default
- CORS is configured for localhost:5173 (Vite default)
- All imports use ES6 syntax
