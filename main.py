from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db,engine
import models, schemas
import json

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post("/users/", response_model=schemas.UserProfileResponse)
def create_user(user: schemas.UserProfileCreate, db: Session = Depends(get_db)):
    existing_contact = db.query(models.UserContact).filter(
        (models.UserContact.email == user.contact.email) |
        (models.UserContact.mobile_number == user.contact.mobile_number)
    ).first()
    
    if existing_contact:
        raise HTTPException(status_code=400, detail="Email or Phone number already registered")
    
    user_data = user.dict(exclude={"contact", "preferences"})
    user_data["interests"] = json.dumps(user.interests) if user.interests else "[]"
    
    db_user = models.UserProfile(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    db_contact = models.UserContact(user_id=db_user.id, **user.contact.dict())
    db.add(db_contact)
    
    db_preferences = models.UserPreferences(user_id=db_user.id, **user.preferences.dict())
    db.add(db_preferences)
    
    db.commit()
    db_user.interests = json.loads(db_user.interests)
    return db_user

@app.get("/users/", response_model=list[schemas.UserProfileResponse])
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.UserProfile).all()
    for user in users:
        user.interests = json.loads(user.interests) if user.interests else []
    return users

@app.get("/users/{user_id}", response_model=schemas.UserProfileResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.interests = json.loads(user.interests) if user.interests else []
    return user

@app.get("/users/{user_id}/matches", response_model=list[schemas.UserProfileResponse])
def find_matches(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()
    preferences = db.query(models.UserPreferences).filter(models.UserPreferences.user_id == user_id).first()

    if not user or not preferences:
        raise HTTPException(status_code=404, detail="User or preferences not found")

    # Filtering potential matches based on preferences
    potential_matches = db.query(models.UserProfile).filter(
        models.UserProfile.gender != user.gender,
        models.UserProfile.age.between(preferences.preferred_age_min, preferences.preferred_age_max),
        (models.UserProfile.religion == preferences.preferred_religion) if preferences.preferred_religion else True,
        (models.UserProfile.work_location == preferences.preferred_location) if preferences.preferred_location else True,
        (models.UserProfile.diet == preferences.preferred_diet) if preferences.preferred_diet else True,
        (models.UserProfile.drinking_habits == preferences.preferred_drinking_habits) if preferences.preferred_drinking_habits else True,
        (models.UserProfile.smoking_habits == preferences.preferred_smoking_habits) if preferences.preferred_smoking_habits else True,
        models.UserProfile.id != user.id
    ).all()

    user_interests = set(json.loads(user.interests)) if user.interests else set()
    
    # matching according to interests
    matches = []
    for match in potential_matches:
        match_interests = set(json.loads(match.interests)) if match.interests else set()
        if user_interests.intersection(match_interests):
            match.interests = list(match_interests)
            matches.append(match)

    return matches

@app.put("/users/{user_id}", response_model=schemas.UserProfileResponse)
def update_user(user_id: int, user_update: schemas.UserProfileCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_update.model_dump(exclude={"contact", "preferences"}).items():
        setattr(db_user, key, json.dumps(value) if key == "interests" else value)
    
    db_contact = db.query(models.UserContact).filter(models.UserContact.user_id == user_id).first()
    if db_contact:
        for key, value in user_update.contact.model_dump().items():
            setattr(db_contact, key, value)
    
    db_preferences = db.query(models.UserPreferences).filter(models.UserPreferences.user_id == user_id).first()
    if db_preferences:
        for key, value in user_update.preferences.model_dump().items():
            setattr(db_preferences, key, value)
    
    db.commit()
    db.refresh(db_user)
    db_user.interests = json.loads(db_user.interests)
    return db_user

@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.query(models.UserContact).filter(models.UserContact.user_id == user_id).delete()
    db.query(models.UserPreferences).filter(models.UserPreferences.user_id == user_id).delete()
    db.delete(db_user)
    db.commit()
    
    return {"message": "User deleted successfully"}

