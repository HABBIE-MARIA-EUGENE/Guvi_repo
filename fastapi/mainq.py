from fastapi import FastAPI

app = FastAPI()

@app.get("/book/{book_id}")
async def book(book_id):
    books_data = {
        "1001" : "python",
        "1002" : "java",
        "1003" : "html",
        "1004" : "css",
        "1005" : "javascript"
    }
    return {"Book ID: {} and Book Name: {}".format(book_id, books_data[book_id])}

@app.get("/books")
async def books(limit: int):
    a = [
        {"1001" : "python"},
        {"1002" : "java"},
        {"1003" : "html"},
        {"1004" : "css"},
        {"1005" : "javascript"}
    ]
    return {"book data is : {}".format(a[:limit])}

# http://127.0.0.1:8000/books?limit=1
# http://127.0.0.1:8000/books?limit=2
# http://127.0.0.1:8000/books?limit=3