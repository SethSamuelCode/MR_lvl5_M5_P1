# ------------------ IMPORTS AND SETUP ----------------- #

import typer
import json
from pymongo import MongoClient
import yaml
from typing import Final
import os
import keyring

app = typer.Typer()
# ----------------------- DEFINES ---------------------- #
KEYRING_SERVICE_NAME:Final = "dataSeeder"
KEYRING_CONNECTION_NAME:Final = "userConnectionString"
KEYRING_COLLECTION_NAME:Final ="userCollectionName"
# CONNECTION_STRING = "mongodb://fluffy:pass@localhost/m5Test"
CONNECTION_STRING = keyring.get_password(KEYRING_SERVICE_NAME,KEYRING_CONNECTION_NAME)
mongoConnection = MongoClient(CONNECTION_STRING)
DATABASE_NAME = "m5Test"
db = mongoConnection[DATABASE_NAME]
# COLLECTION_NAME = "testColl"
COLLECTION_NAME = keyring.get_password(KEYRING_SERVICE_NAME,KEYRING_COLLECTION_NAME)
# db.create_collection(COLLECTION_NAME)
collection = db[COLLECTION_NAME]


configBase = {
    "username":"user",
    "password": "pass",
    "server": "localhost",
    "database": "database"
}

# ---------------------- FUNCTIONS --------------------- #

def getDataFromFile():
    with open("dataToInput.json",'r') as data:

        return json.load(data)
# --------------------- ENTRYPOINT --------------------- #


@app.command("add")
def add_data(title: str,description: str,start_price: int, reserve_price: int):
    # print(f"data added: {data}")
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
    seedData = getDataFromFile()
    collection.insert_many(seedData["auction_items"])

# @app.command("checkData")
# def check_data():
#     getDataFromFile()
#     print(seedData["auction_items"])

@app.command("getAll")
def get_all():
    for item in collection.find():
        print(item)

@app.command("setupFile")
def setup_with_file():
    tempFilename: Final = "configFile.txt"
    with open(tempFilename,"w") as configFile:
        yaml.safe_dump(configBase,configFile)
    input("A file has been created in this directory pelase enter your details and press enter to continue")
    with open(tempFilename,"r") as configFile:
        data = yaml.safe_load(configFile)
        print(data)
    os.remove(tempFilename)
# prevent passwords being saved in history
@app.command("setup")
def setup_interactive(getSettings:bool = False):
    if not getSettings:
        userConnectionString:str = input("enter your connection string:\n")
        keyring.set_password(KEYRING_SERVICE_NAME,KEYRING_CONNECTION_NAME,userConnectionString)
        userCollectionName:str = input("enter the collection name: ")
        keyring.set_password(KEYRING_SERVICE_NAME,KEYRING_COLLECTION_NAME,userCollectionName)

    else: 
        print(f"mongo connection string: {keyring.get_password(KEYRING_SERVICE_NAME,KEYRING_CONNECTION_NAME)}")
        print(f"mongo connection string: {keyring.get_password(KEYRING_SERVICE_NAME,KEYRING_COLLECTION_NAME)}")



@app.command("delete")
def del_data(field: str, value:str):
    # Assuming 'data' is the name to delete
    collection.delete_one({field: value})
    print(f"data deleted if exists")

def main(name: str = "name" ):
    print(f"hello {name}")

if __name__ == "__main__":
    app()