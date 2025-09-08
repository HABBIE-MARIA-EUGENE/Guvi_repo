from fastapi import FastAPI

app = FastAPI()

@app.get("/")  #ep using get method
async def home():
    return {"message" : "hello FastAPI"}

@app.get("/iTems/{item_id}")
async def read_item(item_id: int):
    return {"item id": item_id}

#path params.

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return{"user": user_id}

#Q params

@app.get("/search")
async def search_items(q: str = None, limit: int = 10):
    return{"query": q, "limit": limit}


#Request body using pydantic models for body validation

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@app.post("/items")
async def create_item(item: Item):  #calling Item through item
    return{"message": "item created", "data": item}

#response mod.
class User(BaseModel):
    id: int
    name: str

@app.get("/user/{user_id}",response_model=User)
async def get_user(user_id: int):
    return{"id": user_id, "name": "Eugene"}

#Dependency Injection (Depends) to share logic like db conns , auth etc.,

from fastapi import Depends, HTTPException

def get_token_header(token: str = "secret"):
    if token != "secret":
        raise HTTPException(status_code=400, detail="Invalid Token")
    return token

@app.get("/protected")
def protected_route(token: str = Depends(get_token_header)):
    return{"message": "Access granted"}


#db with sqlalchemy
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import sessionmaker, declarative_base,

# DATABASE_URL = (
#     f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
#     f"?ssl_ca={SSL_CA}"
# )

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush= False)

