# Auction System Project

This project consists of multiple components that work together to create a backend for a auction website with MongoDB integration. Each component serves a specific purpose in the overall system architecture and serves as a testing ground before starting the final project.

## Components

### 1. MongoDB Database Server
Located in `/mongoDB`

A containerized MongoDB instance using Docker Compose for easy deployment and management.

Key files:
- `docker-compose.yaml` - Docker configuration for MongoDB server

### 2. Data Seeder CLI Tool
Located in `/cli` - [View Documentation](cli/README.md)

A Python-based command-line interface for managing auction item data in MongoDB. Features include:
- Secure credential storage
- Single item addition
- Bulk import from JSON files
- Data retrieval and deletion
- Interactive setup for MongoDB connection

### 3. Database API Server
Located in `/getFromDatabaseAPI/node` - [View Documentation](getFromDatabaseAPI/node/README.md)

A Node.js Express server providing a RESTful API interface for MongoDB with AI-assisted search capabilities. Features include:
- Multiple search endpoints (exact match, regex, AI-assisted)
- AI-powered intelligent search using OpenAI
- CORS protection
- Comprehensive error handling
- Request logging

### 4. Python API Server Alternative
Located in `/getFromDatabaseAPI/python`

A Python-based alternative to the Node.js API server (currently in development).

## Project Structure

```
.
├── cli/                    # Data Seeder CLI Tool
├── getFromDatabaseAPI/     # API Servers
│   ├── node/              # Node.js Implementation
│   └── python/            # Python Implementation
└── mongoDB/               # Database Server Configuration
```

## Getting Started

1. Start the MongoDB server:
   ```bash
   cd mongoDB
   docker-compose up -d
   ```

2. Set up the Data Seeder CLI:
   ```bash
   cd cli
   pip install -r requirements.txt
   python dataSeeder.py setup
   ```

3. Start the API server (Node.js version):
   ```bash
   cd getFromDatabaseAPI/node
   npm install
   npm start
   ```

## Documentation

For detailed information about each component, please refer to their respective README files:
- [Data Seeder CLI Documentation](cli/README.md)
- [Node.js API Server Documentation](getFromDatabaseAPI/node/README.md)
