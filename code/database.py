from pymongo import MongoClient
import os

def get_mongo_client():
    mongo_host = os.getenv("MONGO_HOST")
    mongo_port = os.getenv("MONGO_PORT")
    mongo_user = os.getenv("MONGO_USER")
    mongo_pass = os.getenv("MONGO_PASS")
    connection_url = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/?authSource=admin&readPreference=primary&ssl=false&directConnection=true"
    client = MongoClient(connection_url)
    database_name = "employee_db"
    database = client[database_name]
    collection_employee_details = database["employee_details"]
    collection_metrics = database["metrics"]
    return client, database, collection_employee_details, collection_metrics



