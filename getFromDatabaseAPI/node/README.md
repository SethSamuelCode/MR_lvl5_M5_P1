# MongoDB REST API Server

A Node.js Express server providing a RESTful API interface for MongoDB with AI-assisted search capabilities using OpenAI.

## Features

- 🔍 Multiple search endpoints (exact match, regex, AI-assisted)
- 🤖 AI-powered intelligent search using OpenAI
- 🔒 CORS protection with localhost validation
- 📝 Comprehensive error handling
- 🚀 Fast and efficient MongoDB queries
- 📊 Request logging with Morgan

## Prerequisites

- Node.js (v20 or higher)
- MongoDB instance
- OpenAI API key
- npm or yarn package manager

## Installation

1. Clone the repository or navigate to the project directory
2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the root directory with the following variables:
```env
SERVER_LISTEN_PORT=<your_port_number>
CONNECTION_STRING=<your_mongodb_connection_string>
DATABASE_NAME=<your_database_name>
COLLECTION_NAME=<your_collection_name>
OPEN_API_KEY=<your_openai_api_key>
```

## API Endpoints

### Health Check
```http
GET /test
```
Returns a success message to verify the API is working.

### Exact Match Search
```http
GET /get?key=<field>&value=<value>
```
Searches for documents where the specified field exactly matches the given value.

### Regex Search
```http
GET /getRegex?key=<field>&value=<pattern>
```
Searches for documents using regex pattern matching.

### AI-Assisted Search
```http
GET /getAiAssist?key=<field>&value=<search_query>
```
Uses OpenAI to process the search query and find relevant documents.

### AI-Assisted Title and Description Search
```http
GET /getAiAssistTitleAndDescription?value=<search_query>
```
Uses OpenAI to search in both title and description fields.

### Complex Query
```http
POST /get
Content-Type: application/json

{
  "field1": "value1",
  "field2": "value2"
}
```
Accepts a MongoDB query object for flexible searching.

### Get All Documents
```http
GET /getAll
```
Retrieves all documents in the collection.

## Response Format

All endpoints return JSON responses in the following format:

```json
{
  "status": "success|error",
  "data": [/* array of documents */] | /* error message */
}
```

## Error Handling

The API implements comprehensive error handling:

- Invalid requests return 400 status code
- Server errors return 500 status code
- All errors include a descriptive message

## Security

- CORS is configured to only accept requests from localhost
- Request body size is limited to 10MB
- Environment variables are used for sensitive configuration

## Development

To start the server in development mode:

```bash
npm start
```

The server will start on the configured port with Morgan logging in 'dev' format.

## Logging

The application uses Morgan for HTTP request logging in development format:
```
:method :url :status :response-time ms - :res[content-length]
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| SERVER_LISTEN_PORT | Port number for the server |
| CONNECTION_STRING | MongoDB connection string |
| DATABASE_NAME | Name of the MongoDB database |
| COLLECTION_NAME | Name of the MongoDB collection |
| OPEN_API_KEY | OpenAI API key |

## Dependencies

- `express`: Web server framework
- `mongodb`: MongoDB driver
- `openai`: OpenAI API client
- `cors`: Cross-Origin Resource Sharing middleware
- `dotenv`: Environment variable management
- `morgan`: HTTP request logger

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[MIT](https://choosealicense.com/licenses/mit/)
