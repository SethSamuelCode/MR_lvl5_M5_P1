// npm i dotenv morgan express cors

// ------------------ SETUP AND INSTALL ----------------- //

require("dotenv").config(); // Load environment variables from .env
const express = require("express"); // Express web server
const app = express();
const cors = require("cors"); // CORS middleware
const PORT = process.env.SERVER_LISTEN_PORT; // Port from environment
const assert = require("node:assert/strict"); // Assertion utility for debugging
const { MongoClient } = require("mongodb");

// ------------------------ SETUP ----------------------- //

const CONNECTION_STRING = process.env.CONNECTION_STRING;
const DATABASE_NAME = process.env.DATABASE_NAME;
const COLLECTION_NAME = process.env.COLLECTION_NAME;

const dbObject = {};

async function setupDB(dbObject) {
  const client = new MongoClient(CONNECTION_STRING);
  dbObject.client = client;
  await dbObject.client.connect();
  dbObject.db = dbObject.client.db(DATABASE_NAME);
  dbObject.collection = dbObject.db.collection(COLLECTION_NAME);
}

setupDB(dbObject);

// --------------------- MIDDLEWARES -------------------- //

const morgan = require("morgan"); // HTTP request logger
app.use(morgan("dev")); // Log requests to console
app.use(express.json({ limit: "10MB" })); // Parse JSON bodies up to 10MB.

// Configure CORS to allow only specific origins
const corsConfigs = {
  origin: (incomingOrigin, allowedAccess) => {
    // Allow localhost (any port) and production domain
    const allowedOrigins = [/^http:\/\/localhost:\d+$/];
    // Allow requests with no origin (e.g., curl, server-to-server)
    if (!incomingOrigin || allowedOrigins.some((testOrigin) => testOrigin.test(incomingOrigin))) {
      allowedAccess(null, true); // Allow
    } else {
      allowedAccess(null, false); // Deny
    }
  },
};
app.use(cors(corsConfigs)); // Apply CORS policy

// ---------------------- FUNCTIONS --------------------- //

// ----------------------- ROUTES ----------------------- //

// Health check/test GET endpoint
app.get("/test", (req, resp) => {
  resp.status(200).json({ status: "success", data: "youve hit /test" });
});

// Test POST endpoint to echo received data
app.post("/postTest", (req, resp) => {
  console.log(req.body);
  resp.status(200).json({ status: "success", data: req.body });
});

app.get("/get", async (req, resp) => {
  const key = req.query.key
  const value = Number(req.query.value)
  console.log(`key: ${key}, value: ${value}`)
  const results = await dbObject.collection.find({ [key]: value }).toArray();
  resp.status(200).json({ status: "success", data: results });
});

app.post("/get", async (req, resp) => {
  const body= req.body
  console.log(body)
  console.log(`key: ${body.key}, value: ${body.value}`)
  const results = await dbObject.collection.find(req.body).toArray();
  resp.status(200).json({ status: "success", data: results });
});

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
