from fastapi import FastAPI

app=FastAPI()

# @app.get("/welcome/{name}")
# async def hello(name):
#     return {"Hello: "+ name +" Welcome to FastAPI"}

# @app.get("/books/{book_id}/{book_name}")
# async def hello(book_id: int, book_name):
#     return {"Book ID:" +str(book_id)+ " Book Name: " +book_name}

# books/default
# books/{book_name}


@app.get("/books/default")
async def books():
    return "Python programming"

@app.get("/books/{book_name}")
async def hello(book_name):
    return book_name