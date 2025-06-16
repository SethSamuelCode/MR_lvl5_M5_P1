# ----------------------- IMPORTS ---------------------- #

import typer
import json
from pymongo import MongoClient
from typing import Final
import os
import keyring

app = typer.Typer(
    name="dataSeeder",
    help="A CLI tool for seeding MongoDB with auction item data. Supports adding individual items, bulk imports, and data management.",
    short_help="MongoDB data seeder for auction items"
)

# ----------------------- DEFINES ---------------------- #
KEYRING_SERVICE_NAME:Final = "dataSeeder"
KEYRING_CONNECTION_NAME:Final = "userConnectionString"
KEYRING_COLLECTION_NAME:Final ="userCollectionName"

# ------------------------ SETUP ----------------------- #


# CONNECTION_STRING = "mongodb://fluffy:pass@localhost/m5Test"
CONNECTION_STRING = keyring.get_password(KEYRING_SERVICE_NAME,KEYRING_CONNECTION_NAME)

if not CONNECTION_STRING:
    print("you have not set up your connection string please run dataseeder setup")
    raise typer.Exit()

mongoConnection = MongoClient(CONNECTION_STRING)
DATABASE_NAME = "m5Test"
db = mongoConnection[DATABASE_NAME]
# COLLECTION_NAME = "testColl"
COLLECTION_NAME = keyring.get_password(KEYRING_SERVICE_NAME,KEYRING_COLLECTION_NAME)
# db.create_collection(COLLECTION_NAME)
collection = db[COLLECTION_NAME] # type: ignore

# ---------------------- FUNCTIONS --------------------- #

def getDataFromFile():
    """
    Read and parse the JSON data from dataToInput.json file.
    
    Returns:
        dict: The parsed JSON data containing auction items
    """
    with open("dataToInput.json",'r') as data:
        return json.load(data)

# --------------------- ENTRYPOINT --------------------- #

@app.command("add")
def add_data(
    title: str,
    description: str,
    start_price: int, 
    reserve_price: int
):
    """
    Add a single auction item to the MongoDB collection.

    Args:
        title: The title of the auction item
        description: A detailed description of the item
        start_price: The starting bid price for the item
        reserve_price: The minimum price that must be met for the item to be sold
    """
    dataToInsert = {
      "title": title,
      "description": description,
      "start_price": start_price,
      "reserve_price": reserve_price
    }
    collection.insert_one(dataToInsert)
    print("data added")

@app.command("importFile")
def import_file():
    """
    Bulk import auction items from the dataToInput.json file.
    
    The JSON file should contain an 'auction_items' array with objects having the following structure:
    {
        "title": str,
        "description": str,
        "start_price": int,
        "reserve_price": int
    }
    """
    seedData = getDataFromFile()
    collection.insert_many(seedData["auction_items"])

@app.command("getAll")
def get_all():
    """
    Display all auction items stored in the MongoDB collection.
    
    Prints each item with all its fields and the MongoDB-generated _id.
    """
    for item in collection.find():
        print(item)

@app.command("setup")
def setup_interactive(
    getSettings: bool = typer.Option(
        False,
        help="If True, displays current connection settings instead of setting new ones"
    )
):
    """
    Configure MongoDB connection settings securely using the system keyring.
    
    The connection string and collection name are stored securely in the system keyring
    and are not saved in command history.

    Args:
        getSettings: When True, displays current settings instead of prompting for new ones
    """
    if not getSettings:
        userConnectionString:str = input("enter your connection string:\n")
        keyring.set_password(KEYRING_SERVICE_NAME,KEYRING_CONNECTION_NAME,userConnectionString)
        userCollectionName:str = input("enter the collection name: ")
        keyring.set_password(KEYRING_SERVICE_NAME,KEYRING_COLLECTION_NAME,userCollectionName)
    else: 
        print(f"mongo connection string: {keyring.get_password(KEYRING_SERVICE_NAME,KEYRING_CONNECTION_NAME)}")
        print(f"mongo connection string: {keyring.get_password(KEYRING_SERVICE_NAME,KEYRING_COLLECTION_NAME)}")

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
):
    """
    Delete auction items from the MongoDB collection based on a field match.

    Args:
        field: The field name to match (e.g., 'title', 'description')
        value: The value to match against the field
        multiDelete: When True, deletes all matching documents; when False, deletes only the first match
    """
    if multiDelete:
        collection.delete_many({field: value})
    else:
        collection.delete_one({field: value})
    print(f"data deleted if exists")

if __name__ == "__main__":
    app()