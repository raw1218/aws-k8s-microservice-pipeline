from fastapi import FastAPI
import datetime

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