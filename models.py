from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    age = Column(Integer, nullable=False)
    mother_tongue = Column(String(50), nullable=False)
    nationality = Column(String(50), nullable=False)
    marital_status = Column(String(20), nullable=False)
    highest_qualification = Column(String(100), nullable=False)
    occupation = Column(String(100), nullable=False)
    work_location = Column(String(100), nullable=False)
    religion = Column(String(50), nullable=False)
    caste = Column(String(50), nullable=True)
    community = Column(String(50), nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    hobbies = Column(String(255), nullable=True)
    diet = Column(String(20), nullable=True)
    drinking_habits = Column(String(20), nullable=True)
    smoking_habits = Column(String(20), nullable=True)
    languages_spoken = Column(String(255), nullable=True)
    interests = Column(String, nullable=True)

    contact = relationship("UserContact", uselist=False, back_populates="user", cascade="all, delete-orphan")
    preferences = relationship("UserPreferences", uselist=False, back_populates="user", cascade="all, delete-orphan")

class UserContact(Base):
    __tablename__ = "user_contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"), unique=True, nullable=False)
    mobile_number = Column(String(15), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    user = relationship("UserProfile", back_populates="contact")

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"), unique=True, nullable=False)
    preferred_age_min = Column(Integer, nullable=False)
    preferred_age_max = Column(Integer, nullable=False)
    preferred_religion = Column(String(50), nullable=True)
    preferred_location = Column(String(100), nullable=True)
    preferred_diet = Column(String(20), nullable=True)
    preferred_drinking_habits = Column(String(20), nullable=True)
    preferred_smoking_habits = Column(String(20), nullable=True)

    user = relationship("UserProfile", back_populates="preferences")