#query parameter validation

from fastapi import FastAPI

emp = [
    {'id': 101, 'name': 'CSE', 'place': 'Chennai'},
    {'id': 102, 'name': 'ESC', 'place': 'Chen'}
]



app = FastAPI()

# @app.get("/display/{id}")
# def viewforpath(id: int):


@app.get("/display")
def viewforquery(id: int):
    for e in emp:
        if e['id']==id:
            return e
    