from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date

class UserProfileBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=50)
    gender: str = Field(..., pattern="^(Male|Female|Other)$")
    date_of_birth: date
    age: int = Field(..., ge=18, le=100)
    mother_tongue: str = Field(..., max_length=50)
    nationality: str = Field(..., max_length=50)
    marital_status: str = Field(..., max_length=20)
    highest_qualification: str = Field(..., max_length=100)
    occupation: str = Field(..., max_length=100)
    work_location: str = Field(..., max_length=100)
    religion: str = Field(..., max_length=50)
    caste: Optional[str] = Field(None, max_length=50)
    community: Optional[str] = Field(None, max_length=50)
    height: Optional[float] = Field(None, gt=100, lt=250)
    weight: Optional[float] = Field(None, gt=30, lt=200)
    hobbies: Optional[str] = Field(None, max_length=255)
    diet: Optional[str] = Field(None, pattern="^(Veg|Non-Veg|Vegan|Others)$")
    drinking_habits: Optional[str] = Field(None, pattern="^(Never|Occasionally|Frequently)$")
    smoking_habits: Optional[str] = Field(None, pattern="^(Never|Occasionally|Frequently)$")
    languages_spoken: Optional[str] = Field(None, max_length=255)
    interests: List[str] = Field(default=[])

class UserContactBase(BaseModel):
    mobile_number: str = Field(..., pattern=r"^\+\d{1,3}\d{10}$", max_length=15)
    email: EmailStr

class UserPreferencesBase(BaseModel):
    preferred_age_min: int = Field(..., ge=18, le=100)
    preferred_age_max: int = Field(..., ge=18, le=100)
    preferred_religion: Optional[str] = Field(None, max_length=50)
    preferred_location: Optional[str] = Field(None, max_length=100)
    preferred_diet: Optional[str] = Field(None, pattern="^(Veg|Non-Veg|Vegan|Others)$")
    preferred_drinking_habits: Optional[str] = Field(None, pattern="^(Never|Occasionally|Frequently)$")
    preferred_smoking_habits: Optional[str] = Field(None, pattern="^(Never|Occasionally|Frequently)$")

class UserProfileCreate(UserProfileBase):
    contact: UserContactBase
    preferences: UserPreferencesBase

class UserProfileResponse(UserProfileBase):
    id: int
    contact: UserContactBase
    preferences: UserPreferencesBase

    class Config:
        from_attributes = True
