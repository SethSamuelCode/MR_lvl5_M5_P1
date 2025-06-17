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

# ----------------------- IMPORTS ---------------------- #

import typer
import json
from pymongo import MongoClient
from typing import Final
import keyring
import os

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
# Retrieve MongoDB connection details from system keyring
CONNECTION_STRING = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_CONNECTION_NAME)

if not CONNECTION_STRING:
    print("You have not set up your connection string. Please run 'dataSeeder setup'")
    raise typer.Exit()

try:
    # Initialize MongoDB connection and get database/collection references
    mongoConnection = MongoClient(CONNECTION_STRING)
    DATABASE_NAME = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_DATABASE_NAME)
    db = mongoConnection[DATABASE_NAME]  # type: ignore
    COLLECTION_NAME = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_COLLECTION_NAME)
    collection = db[COLLECTION_NAME]  # type: ignore
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise typer.Exit()

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
    collection.insert_one(dataToInsert)
    print("Data added")

@app.command("import-file")
def import_file(
    fileName: str = typer.Option(
        ...,
        "--file",
        "-f",
        help="File to load seed data from",
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
        userConnectionString:str = input("Enter your connection string:\n")
        keyring.set_password(KEYRING_SERVICE_NAME,KEYRING_CONNECTION_NAME,userConnectionString)
        userDatabaseName:str = input("Enter the database name: ")
        keyring.set_password(KEYRING_SERVICE_NAME,KEYRING_DATABASE_NAME,userDatabaseName)
        userCollectionName:str = input("Enter the collection name: ")
        keyring.set_password(KEYRING_SERVICE_NAME,KEYRING_COLLECTION_NAME,userCollectionName)
        print("Setup complete. You can now use the other commands.")
    else: 
        print(f"MongoDB connection string: {keyring.get_password(KEYRING_SERVICE_NAME,KEYRING_CONNECTION_NAME)}")
        print(f"MongoDB database name: {keyring.get_password(KEYRING_SERVICE_NAME,KEYRING_DATABASE_NAME)}")
        print(f"MongoDB collection name: {keyring.get_password(KEYRING_SERVICE_NAME,KEYRING_COLLECTION_NAME)}")

@app.command("delete")
def del_data(
    field: str = typer.Argument(..., help="The field name to match for deletion"),
    value: str = typer.Argument(..., help="The value to match for deletion"),
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
    if multiDelete:
        result = collection.delete_many({field: value})
        print(f"Deleted {result.deleted_count} items matching {field} = {value}")
    else:
        result = collection.delete_one({field: value})
        if result.deleted_count > 0:
            print(f"Deleted item with {field} = {value}")
        else:
            print("No matching item found to delete")