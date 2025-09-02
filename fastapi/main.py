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




