from xml.dom.minidom import Element
from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.encoders import jsonable_encoder

class Reservation(BaseModel):
    name : str
    time: int
    table_number: int
    
client = MongoClient('mongodb://localhost', 27017)

# TODO fill in database name
db = client["afternoon_assign"]

# TODO fill in collection name
collection = db["table"]

app = FastAPI()


# TODO complete all endpoint.
@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name:str):
    result = collection.find_one({"name":name},{"_id" :0})
    print(result)
    return {"result" : result}

@app.get("/reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    result = collection.find({"table_number" : table},{"_id": 0,"table_number":0})
    myre = []
    for r in result:
        myre.append(r)
    return {"result" : myre}


@app.post("/reservation")
def reserve(reservation : Reservation):
    check = collection.find_one({"time":reservation.time,"table_number" : reservation.table_number},{"_id":0})
    if (check == None):
        reservation = jsonable_encoder(reservation)
        collection.insert_one(reservation)
        return {"result" : "Finish"}
    else:
        return {"result" : "Cannot reserve"}

@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    check = collection.find_one({"time":reservation.time,"table_number" : reservation.table_number},{"_id":0})
    if (check == None):
        q = {"name":reservation.name}
        new = {"$set" : {"time":reservation.time,"table_number" : reservation.table_number}}
        collection.update_one(q, new)
        return {"result" : "Finish"}
    else:
        return {"result" : "Cannot reserve"}

@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number : int):
    q = {"name" : name, "table_number": table_number}
    collection.delete_one(q)
    return {"result" : "Finish"}

