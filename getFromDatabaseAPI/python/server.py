# ----------------------- IMPORTS ---------------------- #

from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# ------------------------ SETUP ----------------------- #

load_dotenv()
app = FastAPI()

mongoConnection = MongoClient(os.getenv("CONNECTION_STRING"))
db = mongoConnection[os.getenv("DATABASE_NAME")] # type: ignore
collection = db[os.getenv("COLLECTION_NAME")] # type: ignore



# ----------------------- ROUTES ----------------------- #


app.get("/api/get")
def get_from_mongo(key: str = "", value: str=""):
   print(f"key: {key} , value: {value}")
   results =  collection.find({key: value})
   return results