from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return{
        "message":"hello from fast api!"
    }

# @app.get("/items/{name}")
# def read_item(name):
#     return {"name": name}

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


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items")
def list_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip+limit]


from typing import Optional

@app.get("/items/{item_id}")
def get_item(item_id: str, q: str | None = None):
    if q:
        return{"item_id": item_id, "q": q}
    return{"item_id": item_id}

@app.get("/users/")
def read_user(name: str):
    return {"user_name": name}