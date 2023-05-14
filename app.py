import json
from flask import Flask, json, Response, request, jsonify, render_template
from bson import json_util
from pymongo import MongoClient
from dotenv import dotenv_values, load_dotenv , find_dotenv
import logging, os
from database import get_mongo_client

app = Flask(__name__)

# Configurar el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configurar el formateo de los mensajes del logger
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Crear un manejador para escribir los mensajes en un archivo
file_handler = logging.FileHandler('apptest.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Agregar el manejador al logger
logger.addHandler(file_handler)


@app.route('/', methods=('GET', 'POST'))
def hello():
    logger.info('Se ha accedido a la ruta raiz')
    return render_template('home.html')


@app.route('/newuser', methods=['POST'])
def newuser():
    client, database, collection_employee_details, collection_metrics = get_mongo_client()

    data = request.json
    name = data.get('Name')
    employee_id = data.get('ID_Empleado')
    cargo = data.get('Cargo')
    
    document = {
        "Name": name,
        "ID_Empleado": employee_id,
        "Cargo": cargo
    }
    result = collection_employee_details.insert_one(document)
    inserted_id = result.inserted_id
    # Convertir el ObjectId en una representación serializable
    document['_id'] = str(inserted_id)

    logger.info(f"Se agrego un nuevo usuario con exito en el endpoint /newuser: {document}")
    return Response(json_util.dumps(document), status=201, mimetype='application/json')
    #return render_template('newuser.html')


@app.route('/listuser', methods=['POST'])
def listuser():
    client, database, collection_employee_details, collection_metrics = get_mongo_client()
    data = request.json
    name = data.get('Name')
    
    query = {"Name": name}
    results = list(collection_employee_details.find(query))
    # Convertir los ObjectId en representaciones serializables
    for result in results:
        result['_id'] = str(result['_id'])

    return jsonify(results)

    

@app.route('/deleteuser', methods=['POST'])
def deleteuser():
    client, database, collection_employee_details, collection_metrics = get_mongo_client()
    data = request.json
    employee_id = data.get('ID_Empleado')
    
    query = {"ID_Empleado": employee_id}
    results = collection_employee_details.delete_one(query)

    return Response("El usuario se elimino con exito", status=200, mimetype='application/json')

@app.route('/lider', methods=['POST'])
def lider():
    client, database, collection_employee_details, collection_metrics = get_mongo_client()
    data = request.json
    users = data.get('Users')

    document = {
        "Lider": users
    }
    result = collection_metrics.insert_one(document)
    inserted_id = result.inserted_id
    # Convertir el ObjectId en una representación serializable
    document['_id'] = str(inserted_id)

    logger.info(f"Listo /Lider: {document}")
    return Response(json_util.dumps(document), status=201, mimetype='application/json')



@app.route('/metrics', methods=['GET'])
def metrics():
    client, database, collection_employee_details, collection_metrics = get_mongo_client()

    # Obtener la cantidad de usuarios en la colección "employee_details"
    user_count = collection_employee_details.count_documents({})
    lider_count = collection_metrics.count_documents({})
    
    # Crear el objeto de métricas
    metrics = {
        "UserCount": user_count,
        "LiderCount": lider_count
    }
    logger.info(f"Metrics : {metrics}")
    return jsonify(metrics), 200
    #return render_template('metrics.html', UserCount=user_count, LiderCount=lider_count, status=200, mimetype='application/json')




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)