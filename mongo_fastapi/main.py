from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from database_nosql import profiles_collection
from schemas import ProfileUpdate, ProfileResponse
from bson import ObjectId

app = FastAPI()

# Helper function to convert MongoDB ObjectId
def serialize_profile(profile):
    profile["_id"] = str(profile["_id"])
    return profile

@app.get("/profile/{user_id}", response_model=ProfileResponse)
def get_profile(user_id: int):
    profile = profiles_collection.find_one({"userId": user_id}, {"_id": 0})
    if not profile:
        return ProfileResponse(status="error", profile=None, message="Profile not found")
    return ProfileResponse(status="success", profile=profile)

@app.post("/profile/{user_id}", response_model=ProfileResponse)
def update_profile(user_id: int, profile: ProfileUpdate):
    update_data = profile.dict()

    profiles_collection.update_one(
        {"userId": user_id}, {"$set": update_data}, upsert=True
    )

    updated_profile = profiles_collection.find_one({"userId": user_id}, {"_id": 0})
    return ProfileResponse(status="success", profile=updated_profile)
