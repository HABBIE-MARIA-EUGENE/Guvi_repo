# main.py - FastAPI main application
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, validator
from passlib.context import CryptContext
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our database connections
from database.connections import get_mysql_connection, get_redis_client, get_mongo_client
from auth.password_utils import hash_password

app = FastAPI(title="Your App API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:5500"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    
    @validator('name')
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserResponse(BaseModel):
    message: str
    user_id: str

# Register endpoint
@app.post("/auth/register", response_model=UserResponse)
async def register_user(user_data: UserRegister):
    try:
        # Get database connections
        mysql_conn = await get_mysql_connection()
        redis_client = await get_redis_client()
        mongo_client = get_mongo_client()
        
        # Check if user already exists in MySQL
        cursor = mysql_conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE email = %s", (user_data.email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Insert user into MySQL
        insert_query = """
            INSERT INTO users (name, email, password_hash, created_at) 
            VALUES (%s, %s, %s, NOW())
        """
        cursor.execute(insert_query, (user_data.name, user_data.email, hashed_password))
        mysql_conn.commit()
        
        # Get the inserted user ID
        user_id = cursor.lastrowid
        cursor.close()
        mysql_conn.close()
        
        # Store additional user data in MongoDB (optional)
        mongo_db = mongo_client.get_database("your_app_db")
        users_collection = mongo_db.users
        
        mongo_user_data = {
            "mysql_user_id": user_id,
            "email": user_data.email,
            "name": user_data.name,
            "profile_data": {},
            "created_at": asyncio.get_event_loop().time()
        }
        
        result = users_collection.insert_one(mongo_user_data)
        
        # Cache user info in Redis (optional)
        user_cache = {
            "id": str(user_id),
            "name": user_data.name,
            "email": user_data.email
        }
        redis_client.hset(f"user:{user_id}", mapping=user_cache)
        redis_client.expire(f"user:{user_id}", 3600)  # 1 hour cache
        
        return UserResponse(
            message="User registered successfully",
            user_id=str(user_id)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)