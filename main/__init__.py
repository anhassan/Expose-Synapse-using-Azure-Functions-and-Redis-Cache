import logging
from flask import Flask,redirect,jsonify,request
import azure.functions as func
import pyodbc
import os,pickle
import redis,json
from datetime import date, datetime, timedelta

app = Flask(__name__)


# Getting credentials for Synapse Persistance Store and In memory Redis Cache - mostly from Azure Key Vault
credentials = {
    "driver" : "{ODBC Driver 17 for SQL Server}",
    "server" : os.environ["FunctionAppSynapseServer"],
    "database" : "DedicatedSQLPool",
    "username" : os.environ["FunctionAppSynapseUser"],
    "password" : os.environ["FunctionAppSynapsePassword"],
    "redis_host" : os.environ["FunctionAppRedisHost"],
    "redis_access_key" : os.environ["FunctionAppRedisPassword"]
}

# Getting parameters for making requests to get data
params = {
    "schema" : "Patients",
    "table" : "Details"
}

# Utility function to get the synapse connection by providing arguments
def get_synapse_connection(credentials):

    conn_string = """DRIVER={};SERVER={};PORT=1433;DATABASE={};UID={};PWD={};"""\
                    .format(credentials["driver"],credentials["server"],credentials["database"]\
                    ,credentials["username"],credentials["password"])

    synapse_connection = pyodbc.connect(conn_string)

    return synapse_connection


# Utility function to get Redis Connection
def get_redis_connection(credentials):
    return redis.StrictRedis(host=credentials["redis_host"],port=6380,
                                db=0,password=credentials["redis_access_key"],ssl=True)


# Function which listens and performs action on Http based trigger
def main(req: func.HttpRequest,context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the WSGI handler.
    """
    logging.info('Python HTTP trigger function processed a request...')

    return func.WsgiMiddleware(app.wsgi_app).handle(req,context)


# Application route which returns patient names from synapse datawarehouse if the cache is empty otherwise returns value from cache
@app.route("/patientNames")
def get_patient_names():

    synapse_conn = get_synapse_connection(credentials)
    patient_names = []
    cache_expiration_time_sec = 60
    
    query = "SELECT * FROM [{}].[{}];".format(params["schema"],params["table"])

    redis_conn = get_redis_connection(credentials)

    if redis_conn.hget("PatientNames","NameKey") is None:

        synapse_cursor = synapse_conn.cursor()
        synapse_cursor.execute(query)

        patient_rows = synapse_cursor.fetchall()
        patient_names = [row[2] for row in patient_rows ]

        logging.info("Reading from Synapse and Populating the Cache....")
    
        patient_names_resp = {"patient_names" : patient_names}
        redis_conn.hset("PatientNames","NameKey",pickle.dumps(patient_names_resp))

        ttl = timedelta(seconds=cache_expiration_time_sec)
        redis_conn.expire(name="PatientNames",time=ttl)
    
    else:
        logging.info("Reading from the Cache....")

        patient_names_obj = pickle.loads(redis_conn.hget("PatientNames","NameKey"))
        patient_names_resp = {"patient_names":patient_names_obj["patient_names"]}
    

    logging.info("Returning the response to the user...")

    return jsonify(patient_names_resp)


@app.route("/patientDetails/<patient_attribute>",methods=["POST","GET"])
def get_patient_details(patient_attribute):
    
    request_filters =  request.get_json(force=True)

    if "department" in request_filters:

        patient_department = request_filters["department"]

        synapse_conn = get_synapse_connection(credentials)
        cache_expiration_time_sec = 60

        query = "SELECT {} FROM [{}].[{}] WHERE AdmitDepartment = '{}' ;"\
                 .format(patient_attribute,params["schema"],params["table"],patient_department)
        
        redis_conn = get_redis_connection(credentials)

        redis_map = "{}_Dept_{}".format(patient_attribute,patient_department)
        redis_key = str(patient_attribute)

        if redis_conn.hget(redis_map,redis_key) is None:

            synapse_cursor = synapse_conn.cursor()
            synapse_cursor.execute(query)

            patient_info_rows = synapse_cursor.fetchall()
            patient_attr_rows = [row[0] for row in patient_info_rows]

            logging.info("Reading from Synapse and Populating the Cache.....")

            patient_attr_resp = {"patient_{}_dept_{}".format(patient_attribute,patient_department) : patient_attr_rows}
            redis_conn.hset(redis_map,redis_key,pickle.dumps(patient_attr_resp))
            
            ttl = timedelta(seconds = cache_expiration_time_sec)
            redis_conn.expire(name=redis_map,time=ttl)
        
        else:
            logging.info("Reading from the Cache....")

            patient_attr_resp = pickle.loads(redis_conn.hget(redis_map,redis_key))
        
        logging.info("Returning response to the user......")
        
        return jsonify(patient_attr_resp)
            

    else:
        exception_statement = "Please provide necessary filter of dept while making request"
        return jsonify({"Error" : exception_statement})



    

