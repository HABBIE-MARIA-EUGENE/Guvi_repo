from pydantic import BaseModel

class ProfileUpdate(BaseModel):
    fullName: str
    dob: str
    age: int | None = None
    phone: str
    about: str

class ProfileResponse(BaseModel):
    status: str
    profile: dict | None = None
    message: str | None = None
