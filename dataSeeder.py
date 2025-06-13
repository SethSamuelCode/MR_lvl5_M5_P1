# ------------------ IMPORTS AND SETUP ----------------- #

import typer
from pymongo import MongoClient

app = typer.Typer()
# ----------------------- DEFINES ---------------------- #
CONNECTION_STRING = "mongodb://fluffy:pass@localhost/m5Test"
mongoConnection = MongoClient(CONNECTION_STRING)
DATABASE_NAME = "m5Test"
db = mongoConnection[DATABASE_NAME]
COLLECTION_NAME = "testColl"
# db.create_collection(COLLECTION_NAME)
collection = db[COLLECTION_NAME]

# ---------------------- FUNCTIONS --------------------- #

# --------------------- ENTRYPOINT --------------------- #


@app.command("add")
def add_data(name: str,age: int):
    # print(f"data added: {data}")
    dataToInsert = {"name": name, "age": age }
    collection.insert_one(dataToInsert)
    print("data added")

@app.command("getAll")
def get_all():
    for item in collection.find():
        print(item)

@app.command("delete")
def del_data(data: str):
    print(f"data deleted: {data}")

def main(name: str = "name" ):
    print(f"hello {name}")

if __name__ == "__main__":
    app()