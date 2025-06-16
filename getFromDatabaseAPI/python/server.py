# ----------------------- IMPORTS ---------------------- #

from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware 

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


@app.get("/api/get")
def get_from_mongo(key: str = "", value: str=""):
   print(f"key: {key} , value: {value}")
   documentStore = []
   for document in collection.find({key:value}):
      documentStore.append(document)
   return documentStore



@app.get("/")
def def_route():
   return "helloworld"