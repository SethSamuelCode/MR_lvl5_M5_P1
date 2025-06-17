// npm i dotenv morgan express cors

// ------------------ SETUP AND INSTALL ----------------- //

require("dotenv").config(); // Load environment variables from .env
const express = require("express"); // Express web server
const app = express();
const cors = require("cors"); // CORS middleware
const PORT = process.env.SERVER_LISTEN_PORT; // Port from environment
const assert = require("node:assert/strict"); // Assertion utility for debugging
const { MongoClient } = require("mongodb");
const OpenAI = require("openai");

// ------------------------ SETUP ----------------------- //

// MongoDB connection configuration from environment variables
const CONNECTION_STRING = process.env.CONNECTION_STRING;
const DATABASE_NAME = process.env.DATABASE_NAME;
const COLLECTION_NAME = process.env.COLLECTION_NAME;

// Object to store database connection and related objects
const dbObject = {};

/**
 * Sets up the MongoDB database connection
 * @param {Object} dbObject - Object to store database connection details
 */
async function setupDB(dbObject) {
  // Create new MongoDB client
  const client = new MongoClient(CONNECTION_STRING);
  dbObject.client = client;
  // Connect to MongoDB
  await dbObject.client.connect();
  // Get database and collection references
  dbObject.db = dbObject.client.db(DATABASE_NAME);
  dbObject.collection = dbObject.db.collection(COLLECTION_NAME);
}

// Initialize database connection
setupDB(dbObject);

const client = new OpenAI({
  apiKey: process.env.OPEN_API_KEY,
});

// --------------------- MIDDLEWARES -------------------- //

const morgan = require("morgan"); // HTTP request logger
app.use(morgan("dev")); // Log requests to console
app.use(express.json({ limit: "10MB" })); // Parse JSON bodies up to 10MB.

// CORS configuration for handling cross-origin requests
const corsConfigs = {
  origin: (incomingOrigin, allowedAccess) => {
    // Define allowed origins (localhost with any port)
    const allowedOrigins = [/^http:\/\/localhost:\d+$/];
    // Allow requests with no origin or from allowed origins
    if (!incomingOrigin || allowedOrigins.some((testOrigin) => testOrigin.test(incomingOrigin))) {
      allowedAccess(null, true); // Allow the request
    } else {
      allowedAccess(null, false); // Deny the request
    }
  },
};
// Apply CORS configuration
app.use(cors(corsConfigs));

// ---------------------- FUNCTIONS --------------------- //

// ----------------------- ROUTES ----------------------- //

/**
 * Health check endpoint
 * GET /test - Returns a success message to verify API is working
 */
app.get("/test", (req, resp) => {
  resp.status(200).json({ status: "success", data: "youve hit /test" });
});

/**
 * Test POST endpoint
 * POST /postTest - Echoes back the received request body
 */
app.post("/postTest", (req, resp) => {
  console.log(req.body);
  resp.status(200).json({ status: "success", data: req.body });
});

/**
 * GET endpoint for querying documents by exact match
 * GET /get?key=<field>&value=<value> - Returns documents where field matches value
 */
app.get("/get", async (req, resp) => {
  const key = req.query.key;
  try {
    const value = Number(req.query.value);
  } catch {}
  console.log(`key: ${key}, value: ${value}`);
  const results = await dbObject.collection.find({ [key]: value }).toArray();
  resp.status(200).json({ status: "success", data: results });
});

/**
 * GET endpoint for querying documents using regex
 * GET /getRegex?key=<field>&value=<pattern> - Returns documents where field matches regex pattern
 */
app.get("/getRegex", async (req, resp) => {
  const key = req.query.key;
  const value = req.query.value;

  console.log(`key: ${key}, value: ${value}`);
  const results = await dbObject.collection.find({ [key]: { $regex: value, $options: "i" } }).toArray();
  resp.status(200).json({ status: "success", data: results });
});

app.get("/getAiAssist", async (req, resp) => {
  const key = req.query.key;
  const value = req.query.value;

  console.log(`key: ${key}, value: ${value}`);

  const response = await client.responses.create({
    prompt: {
      id: "pmpt_6850cf7bec008190a61a7ab27797c167041e322637ae4331",
      version: "2",
    },
    input: value,
  });

  console.log(response.output_text);
  regex = new RegExp(response.output_text,"i")
  const results = await dbObject.collection.find({ [key]: { $regex: regex } }).toArray();
  resp.status(200).json({ status: "success", data: results });
});

/**
 * POST endpoint for complex queries
 * POST /get - Accepts query object in request body for flexible searching
 */
app.post("/get", async (req, resp) => {
  const body = req.body;
  console.log(body);
  console.log(`key: ${body.key}, value: ${body.value}`);
  const results = await dbObject.collection.find(req.body).toArray();
  resp.status(200).json({ status: "success", data: results });
});

/**
 * GET endpoint to retrieve all documents
 * GET /getAll - Returns all documents in the collection
 */
app.get("/getAll", async (req, resp) => {
  const results = await dbObject.collection.find({}).toArray();
  resp.status(200).json({ status: "success", data: results });
});

// Start the Express server
app
  .listen(PORT, () => {
    console.log(`server is listening at http://localhost:${PORT}`);
  })
  .on("error", (error) => {
    console.log("server error !!!!", error);
  });
