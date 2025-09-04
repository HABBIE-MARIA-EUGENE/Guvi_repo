# request body & pydantic
# Without Pydantic → you write manual validation for every field.

# With Pydantic → you just declare a BaseModel, and validation happens automatically.

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

class manf(BaseModel):
    company : str
    country: str






class items(BaseModel):
    name : str = Field(min_length=3,max_length=50, pattern="^[a-zA-Z]")
    price : float = Field(gt=0,lt=10000)
    availability: Optional[bool] = None
    manufacturer:manf



app = FastAPI()

@app.post("/display/")
def view(data: items):
    return {"message": "item received", "data":data}







# request body
#    To send structured data to the server , it might be either backend or server

# pydantic model
    # Validation
    # Serialization 
    # documentaion


