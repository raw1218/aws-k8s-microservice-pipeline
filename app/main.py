from fastapi import FastAPI
import datetime
from db_client import DbClient


app = FastAPI()

#defines a simple API. 
#The API doesnt matter, the kubernetes pipeline is the main focus of this project.

@app.get("/")
def root():
    return {"message": "Kubernetes microservice running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/time")
def time():
    return {"time": str(datetime.datetime.now())}


@app.get("/version")
def version():
    return {"version": "v2"}


#log to the database when the /log endpoint is hit. This is to demonstrate how to use the DbClient to log requests to the database.
@app.get("/log")
def log():
    #for now we will use a dummy ip, but we need to get the real client ip eventually. 
    server_ip = "1.1.1.1"
    client_ip = "2.2.2.2"

    db_client = DbClient()
    db_client.insert_request_log(server_ip, f"client_ip = {client_ip}")
    return {"message": "Logged request to database"}


@app.get("/read_logs")
def read_logs():
    db_client = DbClient()
    logs = db_client.read_request_logs(5)
    return {"logs": logs}
    



