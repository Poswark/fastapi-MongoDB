from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId
from pymongo import MongoClient
from dotenv import dotenv_values
from database import get_mongo_client
import csv
from io import StringIO
from datetime import datetime

app = FastAPI()

# Configurar el middleware CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes ajustar esto según tus necesidades
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    Name: str
    ID_Empleado: str
    Cargo: str

class LiderInput(BaseModel):
    Users: list

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/metrics")
def metrics():
    client, database, collection_employee_details, collection_metrics = get_mongo_client()
    user_count = collection_employee_details.count_documents({})
    lider_count = collection_metrics.count_documents({})
    return {"UserCount": user_count, "LiderCount": lider_count}

@app.get("/metrics/user")
def user_metrics():
    client, database, collection_employee_details, _ = get_mongo_client() 
    user_count = collection_employee_details.count_documents({})
    users = list(collection_employee_details.find({}))
    return {"UserCount": user_count, "Users": users}

@app.post("/newuser")
def newuser(user: UserInput):
    client, database, collection_employee_details, collection_metrics = get_mongo_client()
    document = {
        "Name": user.Name,
        "ID_Empleado": user.ID_Empleado,
        "Cargo": user.Cargo
    }
    result = collection_employee_details.insert_one(document)
    inserted_id = result.inserted_id
    document['_id'] = str(inserted_id)
    return JSONResponse(content=document, headers={"X-Success": "Usuario agregado correctamente"}, status_code=201)

@app.post("/deleteuser")
def deleteuser(user: UserInput):
    client, database, collection_employee_details, collection_metrics = get_mongo_client()
    query = {"ID_Empleado": user.ID_Empleado}
    result = collection_employee_details.delete_one(query)
    return {"message": "Usuario eliminado correctamente"} if result.deleted_count else {"message": "Usuario no encontrado"}

@app.post("/lider")
def lider(lider: LiderInput):
    client, database, collection_employee_details, collection_metrics = get_mongo_client()
    document = {"Lider": lider.Users}
    result = collection_metrics.insert_one(document)
    inserted_id = result.inserted_id
    document['_id'] = str(inserted_id)
    return JSONResponse(content=document, status_code=201)

@app.get("/metrics/data.csv")
def download_csv():
    client, database, collection_employee_details, _ = get_mongo_client() 
    data_from_mongo = list(collection_employee_details.find({}))

    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    output = StringIO()
    
    fieldnames = list(data_from_mongo[0].keys()) if data_from_mongo else []
    
    csv_writer = csv.DictWriter(output, fieldnames=fieldnames)
    csv_writer.writeheader()

    for document in data_from_mongo:
        csv_writer.writerow(document)

    output.seek(0)

    response = JSONResponse(content={}, status_code=200)
    response.headers['Content-Disposition'] = f'attachment; filename=data-{fecha_actual}.csv'
    response.content = output.getvalue()

    return response
