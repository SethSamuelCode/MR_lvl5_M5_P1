/**
 * Database API Server
 * This Express server provides a RESTful API interface to interact with MongoDB,
 * including features for exact matching, regex searching, and AI-assisted searching.
 * 
 * Required dependencies (npm install):
 * - dotenv: For environment variable management
 * - morgan: For HTTP request logging
 * - express: Web server framework
 * - cors: Cross-Origin Resource Sharing middleware
 * - mongodb: MongoDB driver
 * - openai: OpenAI API client
 */

// ------------------ SETUP AND DEPENDENCIES ----------------- //

require("dotenv").config(); // Load environment variables from .env file
const express = require("express"); // Express web server framework
const app = express();
const cors = require("cors"); // Cross-Origin Resource Sharing middleware
const PORT = process.env.SERVER_LISTEN_PORT; // Server port from environment variables
const assert = require("node:assert/strict"); // Node's strict assertion utility
const { MongoClient } = require("mongodb"); // MongoDB client
const OpenAI = require("openai"); // OpenAI API client

// ------------------ DATABASE CONFIGURATION ----------------- //

// MongoDB connection parameters from environment variables
const CONNECTION_STRING = process.env.CONNECTION_STRING;
const DATABASE_NAME = process.env.DATABASE_NAME;
const COLLECTION_NAME = process.env.COLLECTION_NAME;

// Global object to store database connection and related objects
const dbObject = {};

/**
 * Initializes the MongoDB database connection
 * @param {Object} dbObject - Global object to store database connection details
 * @returns {Promise<void>} A promise that resolves when the connection is established
 * @throws {Error} If connection fails
 */
async function setupDB(dbObject) {
  try {
    // Create new MongoDB client instance
    const client = new MongoClient(CONNECTION_STRING);
    dbObject.client = client;
    // Establish connection to MongoDB
    await dbObject.client.connect();
    // Get database and collection references
    dbObject.db = dbObject.client.db(DATABASE_NAME);
    dbObject.collection = dbObject.db.collection(COLLECTION_NAME);
  } catch (error) {
    console.error('Failed to connect to MongoDB:', error);
    throw error;
  }
}

// Initialize database connection
setupDB(dbObject);

// Initialize OpenAI client with API key from environment variables
const client = new OpenAI({
  apiKey: process.env.OPEN_API_KEY,
});

// --------------------- MIDDLEWARE SETUP -------------------- //

const morgan = require("morgan"); // HTTP request logging middleware
const { title } = require("node:process");
app.use(morgan("dev")); // Enable request logging in development format
app.use(express.json({ limit: "10MB" })); // Parse JSON request bodies (limit: 10MB)

/**
 * CORS Configuration
 * Configures Cross-Origin Resource Sharing to allow requests only from localhost
 */
const corsConfigs = {
  origin: (incomingOrigin, allowedAccess) => {
    // Allow requests only from localhost with any port number
    const allowedOrigins = [/^http:\/\/localhost:\d+$/];
    if (!incomingOrigin || allowedOrigins.some((testOrigin) => testOrigin.test(incomingOrigin))) {
      allowedAccess(null, true); // Allow the request
    } else {
      allowedAccess(null, false); // Deny the request
    }
  },
};
app.use(cors(corsConfigs));

// ----------------------- API ROUTES ----------------------- //

/**
 * Health check endpoint
 * @route GET /test
 * @returns {Object} Success message
 */
app.get("/test", (req, resp) => {
  resp.status(200).json({ status: "success", data: "youve hit /test" });
});

/**
 * Echo endpoint for testing POST requests
 * @route POST /postTest
 * @param {Object} req.body - Any JSON payload
 * @returns {Object} Echo of the request body
 */
app.post("/postTest", (req, resp) => {
  console.log(req.body);
  resp.status(200).json({ status: "success", data: req.body });
});

/**
 * Query documents by exact match
 * @route GET /get
 * @param {string} key - Field name to search in
 * @param {string} value - Value to match exactly
 * @returns {Object} Matching documents
 */
app.get("/get", async (req, resp) => {
  const key = req.query.key;
  try {
    const value = Number(req.query.value);
    console.log(`key: ${key}, value: ${value}`);
    const results = await dbObject.collection.find({ [key]: value }).toArray();
    resp.status(200).json({ status: "success", data: results });
  } catch (error) {
    resp.status(400).json({ status: "error", message: "Invalid value format" });
  }
});

/**
 * Query documents using regex pattern
 * @route GET /getRegex
 * @param {string} key - Field name to search in
 * @param {string} value - Regex pattern to match
 * @returns {Object} Matching documents
 */
app.get("/getRegex", async (req, resp) => {
  const key = req.query.key;
  const value = req.query.value;

  console.log(`key: ${key}, value: ${value}`);
  const results = await dbObject.collection
    .find({ [key]: { $regex: value, $options: "i" } })
    .toArray();
  resp.status(200).json({ status: "success", data: results });
});

/**
 * AI-assisted search endpoint
 * Uses OpenAI to process the search query and find relevant documents
 * @route GET /getAiAssist
 * @param {string} key - Field name to search in
 * @param {string} value - Search query to be processed by AI
 * @returns {Object} Matching documents based on AI-processed query
 */
app.get("/getAiAssist", async (req, resp) => {
  const key = req.query.key;
  const value = req.query.value;

  console.log(`key: ${key}, value: ${value}`);

  try {
    const response = await client.responses.create({
      prompt: {
        id: "pmpt_6850cf7bec008190a61a7ab27797c167041e322637ae4331",
        version: "3",
      },
      input: value,
    });

    const regex = new RegExp(response.output_text, "i");
    const results = await dbObject.collection
      .find({ [key]: { $regex: regex } })
      .toArray();
      console.log(results)
    resp.status(200).json({ status: "success", data: results });
  } catch (error) {
    resp.status(500).json({ status: "error", message: "AI processing failed" });
  }
});

/**
 * AI-assisted search in title and description fields
 * Uses OpenAI to process the search query and searches in both title and description
 * @route GET /getAiAssistTitleAndDescription
 * @param {string} value - Search query to be processed by AI
 * @returns {Object} Matching documents based on AI-processed query
 */
app.get("/getAiAssistTitleAndDescription", async (req, resp) => {
  const value = req.query.value;

  console.log(`value: ${value}`);

  try {
    const response = await client.responses.create({
      prompt: {
        id: "pmpt_6850cf7bec008190a61a7ab27797c167041e322637ae4331",
        version: "3",
      },
      input: value,
    });

    const regex = new RegExp(response.output_text, "i");
    const results = await dbObject.collection
      .find({ $or: [{ title: regex }, { description: regex }] })
      .toArray();
    resp.status(200).json({ status: "success", data: results });
  } catch (error) {
    resp.status(500).json({ status: "error", message: "AI processing failed" });
  }
});

/**
 * Complex query endpoint
 * @route POST /get
 * @param {Object} req.body - MongoDB query object
 * @returns {Object} Matching documents
 */
app.post("/get", async (req, resp) => {
  const body = req.body;
  console.log(`Received query:`, body);
  try {
    const results = await dbObject.collection.find(req.body).toArray();
    resp.status(200).json({ status: "success", data: results });
  } catch (error) {
    resp.status(400).json({ status: "error", message: "Invalid query format" });
  }
});

/**
 * Retrieve all documents
 * @route GET /getAll
 * @returns {Object} All documents in the collection
 */
app.get("/getAll", async (req, resp) => {
  try {
    const results = await dbObject.collection.find({}).toArray();
    resp.status(200).json({ status: "success", data: results });
  } catch (error) {
    resp.status(500).json({ status: "error", message: "Failed to retrieve documents" });
  }
});

// ------------------ SERVER INITIALIZATION ----------------- //

// Start the Express server and handle any startup errors
app
  .listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
  })
  .on("error", (error) => {
    console.error("Server failed to start:", error);
  });
