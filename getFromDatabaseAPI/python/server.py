# ----------------------- IMPORTS ---------------------- #

from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
import re

# ----------------------- DEFINES ---------------------- #

class RequestSchema(BaseModel):
   key: str
   value: str | int 

# ------------------------ SETUP ----------------------- #

load_dotenv()
app = FastAPI()

mongoConnection = MongoClient(os.getenv("CONNECTION_STRING"))
db = mongoConnection[os.getenv("DATABASE_NAME")] # type: ignore
collection = db[os.getenv("COLLECTION_NAME")] # type: ignore

# --------------------- MIDDLEWARES -------------------- #
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------- ROUTES ----------------------- #


@app.get("/api/get/{key}/{value}")
async def get_from_mongo(key, value):
   print(f"key: {key} , value: {value}")
   documentStore = []
   for document in collection.find({key: value}):
      document["_id"] = str(document["_id"])
      documentStore.append(document)
      print(document)
   return documentStore

@app.post("/api/getJson")
async def get_from_mongo_json(input: RequestSchema):
   key = input.key
   value = input.value
   print(f"key: {key} , value: {value}")
   documentStore = []
   for document in collection.find({key: value}):
      document["_id"] = str(document["_id"])
      documentStore.append(document)
      # print(document)
   return documentStore

@app.get("/api/getAll")
def get_all_from_mongo():
   documentStore = []
   for document in collection.find({}):
      document["_id"] = str(document["_id"])
      print(document)
      documentStore.append(document)
   return documentStore

@app.get("/")
def def_route():
   return "helloworld"