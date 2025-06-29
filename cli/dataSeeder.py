"""
MongoDB Auction Item Data Seeder CLI

This module provides a command-line interface for managing auction item data in MongoDB.
It supports operations such as adding individual items, bulk importing from JSON files,
retrieving all items, and deleting items based on field matches.

Features:
    - Secure credential storage using system keyring
    - Single item addition
    - Bulk import from JSON files
    - Data retrieval and deletion
    - Interactive setup for MongoDB connection

Usage:
    python dataSeeder.py setup              # Configure MongoDB connection
    python dataSeeder.py add                # Add a single item
    python dataSeeder.py import-file        # Bulk import from JSON
    python dataSeeder.py getAll             # Display all items
    python dataSeeder.py delete             # Delete items

Requirements:
    - MongoDB server running
    - Python packages: typer, pymongo, keyring
"""

# import sys
# print("Debug: Script starting")
# print(f"Debug: Python version: {sys.version}")
# print(f"Debug: Python executable: {sys.executable}")

# ----------------------- IMPORTS ---------------------- #

import typer
import json
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Final, Optional
import keyring
import os
import re

app = typer.Typer(
    name="dataSeeder",
    help="A CLI tool for seeding MongoDB with auction item data. Supports adding individual items, bulk imports, and data management.",
    short_help="MongoDB data seeder for auction items"
)

# ----------------------- DEFINES ---------------------- #
# Keyring service and key names for secure storage of MongoDB connection details
KEYRING_SERVICE_NAME: Final = "dataSeeder"
KEYRING_CONNECTION_NAME: Final = "userConnectionString"
KEYRING_DATABASE_NAME: Final = "userDatabaseName"
KEYRING_COLLECTION_NAME: Final = "userCollectionName"

# ------------------------ SETUP ----------------------- #
def getMongoCollection(collectionName: str|None) -> Optional[Collection]:
    try:
        # Retrieve MongoDB connection details from system keyring
        CONNECTION_STRING = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_CONNECTION_NAME)
        # Initialize MongoDB connection and get database/collection references
        mongoConnection = MongoClient(CONNECTION_STRING)
        DATABASE_NAME = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_DATABASE_NAME)
        db = mongoConnection[DATABASE_NAME]  # type: ignore
        if not collectionName:
            COLLECTION_NAME = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_COLLECTION_NAME)
        else:
            COLLECTION_NAME = collectionName
        # Return the specified collection from the database
        return db[COLLECTION_NAME]  # type: ignore
    except Exception as e:
        print(f"Failed to connect to MongoDB. Have you run setup? : {e}")
        return None

# ---------------------- FUNCTIONS --------------------- #


# --------------------- ENTRYPOINT --------------------- #

@app.command("add")
def add_data(
    title: str,
    description: str,
    start_price: int, 
    reserve_price: int
) -> None:
    """
    Add a single auction item to the MongoDB collection.

    Args:
        title (str): The title of the auction item.
        description (str): A detailed description of the item.
        start_price (int): The starting bid price for the item.
        reserve_price (int): The minimum price that must be met for the item to be sold.

    Example:
        $ python dataSeeder.py add "Vintage Watch" "A rare 1950s timepiece" 1000 1500
    """
    dataToInsert = {
      "title": title,
      "description": description,
      "start_price": start_price,
      "reserve_price": reserve_price
    }
    collection = getMongoCollection(None)
    if collection is None:
        return
    collection.insert_one(dataToInsert)
    print("Data added")

@app.command("import-file")
def import_file(
    fileName: str = typer.Option(
        ...,
        "--file",
        "-f",
        help="File to load seed data from",
    ),
    # Adding collection name as an option to specify where to import data
    # This allows flexibility in choosing the collection without hardcoding it
    # in the function, making it reusable for different collections
    collectionName: str = typer.Option(
        ...,
        "--collection",
        "-c",
        help="Name of the MongoDB collection to import data into",
    )
) -> None:
    """
    Bulk import auction items from a JSON file.
    
    The JSON file should contain an array of auction item objects with the following structure:
    [
        {
            "title": "Item Title",
            "description": "Item Description",
            "start_price": 1000,
            "reserve_price": 1500
        },
        ...
    ]

    Args:
        fileName (str): Path to the JSON file containing auction items.

    Example:
        $ python dataSeeder.py import-file -f data.json
    """
    if os.path.exists(fileName):
            with open(fileName,'r') as data:
                try:
                    seedData = json.load(data) 
                    collection = getMongoCollection(collectionName)
                    if collection is None:
                        raise ValueError("MongoDB collection not found. Have you run setup?")
                    collection.insert_many(seedData)
                    print("Data imported successfully")
                except Exception as e:
                    print("An error occurred: ",e)
    else:
        print("Please enter a valid filename")

@app.command("getAll")
def get_all() -> None:
    """
    Display all auction items stored in the MongoDB collection.
    
    Prints each item with all its fields including the MongoDB-generated _id.
    Items are displayed in the order they were added to the collection.

    Example:
        $ python dataSeeder.py getAll
    """
    collection = getMongoCollection(None)
    if collection is None:
        return
    for item in collection.find():
        print(item)

@app.command("setup")
def setup_interactive(
    getSettings: bool = typer.Option(
        False,
        help="If True, displays current connection settings instead of setting new ones"
    )
) -> None:
    """
    Configure MongoDB connection settings securely using the system keyring.
    
    The connection string, database name, and collection name are stored securely
    in the system keyring and are not saved in command history. This ensures
    sensitive connection details remain protected.

    Args:
        getSettings (bool): When True, displays current settings instead of
            prompting for new ones.

    Example:
        Set new connection details:
        $ python dataSeeder.py setup

        View current settings:
        $ python dataSeeder.py setup --getSettings
    """
    if not getSettings:
        print("\n=== MongoDB Connection Setup ===")
        print("Please enter your MongoDB connection details below (press Enter to keep current value):")
        
        print("\nStep 1: Connection String")
        current_connection = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_CONNECTION_NAME) or ""
        prompt = f"Enter your connection string [{current_connection if current_connection else 'not set'}]: "
        userConnectionString = input(prompt)
        if userConnectionString.strip():  # Only update if user entered a value
            keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_CONNECTION_NAME, userConnectionString)
            print("✓ Connection string updated successfully")
        else:
            userConnectionString = current_connection
            print("✓ Keeping existing connection string")
        
        print("\nStep 2: Database Name")
        current_database = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_DATABASE_NAME) or ""
        prompt = f"Enter the database name [{current_database if current_database else 'not set'}]: "
        userDatabaseName = input(prompt)
        if userDatabaseName.strip():  # Only update if user entered a value
            keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_DATABASE_NAME, userDatabaseName)
            print("✓ Database name updated successfully")
        else:
            userDatabaseName = current_database
            print("✓ Keeping existing database name")
        
        print("\nStep 3: Collection Name")
        current_collection = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_COLLECTION_NAME) or ""
        prompt = f"Enter the collection name [{current_collection if current_collection else 'not set'}]: "
        userCollectionName = input(prompt)
        if userCollectionName.strip():  # Only update if user entered a value
            keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_COLLECTION_NAME, userCollectionName)
            print("✓ Collection name updated successfully")
        else:
            userCollectionName = current_collection
            print("✓ Keeping existing collection name")
        
        print("\n=== Setup Complete! ===")
        print("All connection details have been saved securely.")
        print("You can now use other commands like 'add', 'import-file', 'getAll', etc.")
        print("To view your settings, run: dataSeeder setup --getSettings")
    else: 
        print("\n=== Current MongoDB Settings ===")
        print(f"Connection string: {keyring.get_password(KEYRING_SERVICE_NAME,KEYRING_CONNECTION_NAME)}")
        print(f"Database name: {keyring.get_password(KEYRING_SERVICE_NAME,KEYRING_DATABASE_NAME)}")
        print(f"Collection name: {keyring.get_password(KEYRING_SERVICE_NAME,KEYRING_COLLECTION_NAME)}")
        print("\nTo change these settings, run: dataSeeder setup")

@app.command("delete")
def del_data(
    field: str = typer.Argument(..., help="The field name to match for deletion"),
    value: str = typer.Argument(..., help="The value to match for deletion"), # type: ignore
    multiDelete: bool = typer.Option(
        False,
        "--multi",
        "-m",
        help="If True, deletes all matching documents instead of just the first one"
    )
) -> None:
    """
    Delete auction items from the MongoDB collection based on a field match.

    Args:
        field (str): The field name to match (e.g., 'title', 'description')
        value (str): The value to match against the field
        multiDelete (bool): When True, deletes all matching documents;
            when False, deletes only the first match

    Examples:
        Delete first item with matching title:
        $ python dataSeeder.py delete title "Vintage Watch"

        Delete all items with matching description:
        $ python dataSeeder.py delete description "Rare" --multi
    """
    try:
        value = int(value) #type: int
    except:
        print()    

    collection = getMongoCollection(None)
    if collection is None:
        return
        
    if multiDelete:
        result = collection.delete_many({field: value})
        print(f"Deleted {result.deleted_count} items matching {field} = {value}")
    else:
        result = collection.delete_one({field: value})
        if result.deleted_count > 0:
            print(f"Deleted item with {field} = {value}")
        else:
            print("No matching item found to delete")

if __name__ == "__main__":
    app()