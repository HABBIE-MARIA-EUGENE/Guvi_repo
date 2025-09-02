from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return{
        "message":"hello from fast api!"
    }

@app.get("/items/{name}")
def read_item(name):
    return {"name": name}

@app.get("/date/{date}")
def read_item(date : int):
    return {"date": date}

@app.get("/user")
def user():
    return {"user": "user 1"}


# @app.get("/user")
# def user():
#     return {"user": "user 2"} # this wont be hitted since the path user hitted already above 


from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "deep learning ftw!"}
    
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
