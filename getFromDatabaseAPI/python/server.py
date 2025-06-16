"""
FastAPI server for MongoDB interaction
This module provides a REST API interface to interact with a MongoDB database.
It includes endpoints for querying documents based on key-value pairs and retrieving all documents.
"""
# ----------------------- IMPORTS ---------------------- #


# Import required libraries
# FastAPI - Web framework for building APIs
# PyMongo - MongoDB driver for Python
# load_dotenv - Load environment variables from .env file
# CORS middleware - Handle Cross-Origin Resource Sharing
# BaseModel - For request body validation
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel

# ----------------------- DEFINES ---------------------- #


# Define the request schema for POST endpoints
class RequestSchema(BaseModel):
   key: str  # Field name to search by
   value: str | int  # Value to match (can be string or integer)

# ------------------------ SETUP ----------------------- #


# Initialize FastAPI app and setup MongoDB connection
load_dotenv()  # Load environment variables from .env file
app = FastAPI()

# Establish MongoDB connection using environment variables
mongoConnection = MongoClient(os.getenv("CONNECTION_STRING"))
db = mongoConnection[os.getenv("DATABASE_NAME")] # type: ignore
collection = db[os.getenv("COLLECTION_NAME")] # type: ignore

# --------------------- MIDDLEWARE --------------------- #


# Configure CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allow all origins
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# ----------------------- ROUTES ----------------------- #

# API Routes

@app.get("/api/get/{key}/{value}")
async def get_from_mongo(key, value):
    """
    GET endpoint to retrieve documents matching a key-value pair
    Args:
        key: Field name to search by
        value: Value to match
    Returns:
        List of matching documents with string-converted ObjectIDs
    """
    print(f"key: {key} , value: {value}")
    documentStore = []
    for document in collection.find({key: value}):
        document["_id"] = str(document["_id"])  # Convert ObjectId to string
        documentStore.append(document)
        print(document)
    return documentStore

@app.post("/api/getJson")
async def get_from_mongo_json(input: RequestSchema):
    """
    POST endpoint to retrieve documents using JSON request body
    Args:
        input: RequestSchema object containing key and value
    Returns:
        List of matching documents with string-converted ObjectIDs
    """
    key = input.key
    value = input.value
    print(f"key: {key} , value: {value}")
    documentStore = []
    for document in collection.find({key: value}):
        document["_id"] = str(document["_id"])
        documentStore.append(document)
    return documentStore

@app.get("/api/getAll")
def get_all_from_mongo():
    """
    GET endpoint to retrieve all documents from the collection
    Returns:
        List of all documents with string-converted ObjectIDs
    """
    documentStore = []
    for document in collection.find({}):
        document["_id"] = str(document["_id"])
        print(document)
        documentStore.append(document)
    return documentStore

@app.get("/")
def def_route():
    """
    Default route that returns a simple hello world message
    Returns:
        String: "helloworld"
    """
    return "helloworld"