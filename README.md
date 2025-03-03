# **Marriage Matchmaking API Documentation**

## **Overview**
The Marriage Matchmaking API is a FastAPI-based application that allows users to create, retrieve, update, delete profiles, and find potential matches based on their preferences.

## **Installation & Setup**
1. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic[email]
   ```
2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## **Endpoints**
### **1. Create User**
- **Endpoint:** `POST /users/`
- **Request Body:**  
  ```json
  {
    "full_name": "John Doe",
    "gender": "Male",
    "date_of_birth": "1995-06-15",
    "age": 29,
    "mother_tongue": "English",
    "nationality": "Indian",
    "marital_status": "Single",
    "highest_qualification": "Bachelor's",
    "occupation": "Software Engineer",
    "work_location": "Mumbai",
    "religion": "Hindu",
    "caste": "Brahmin",
    "community": "North Indian",
    "height": 175,
    "weight": 70,
    "hobbies": "Reading, Traveling",
    "diet": "Veg",
    "drinking_habits": "Never",
    "smoking_habits": "Never",
    "languages_spoken": "English, Hindi",
    "interests": ["Music", "Movies"],
    "contact": {
      "mobile_number": "+919876543210",
      "email": "john.doe@example.com"
    },
    "preferences": {
      "preferred_age_min": 25,
      "preferred_age_max": 30,
      "preferred_religion": "Hindu",
      "preferred_location": "Mumbai",
      "preferred_diet": "Veg",
      "preferred_drinking_habits": "Never",
      "preferred_smoking_habits": "Never"
    }
  }
  ```
- **Response:**  
  Returns the created user profile.

---

### **2. Get All Users**
- **Endpoint:** `GET /users/`
- **Response:**  
  Returns a list of all user profiles.

---

### **3. Get User by ID**
- **Endpoint:** `GET /users/{user_id}`
- **Response:**  
  Returns a specific user profile.

---

### **4. Find Matches for a User**
# **Matchmaking Feature in FastAPI**  

The matchmaking feature helps users find potential partners based on their preferences and shared interests. The goal is to connect users who are compatible in terms of age, location, lifestyle choices, and hobbies.  

---

## **How It Works**  

When a user requests matches, the system follows these steps:  

### **1. Get User Profile & Preferences**  
First, the system fetches the user’s profile and their preferences for a potential match.  

For example, if a user prefers:  
- Age: **25-30 years**  
- Religion: **Hindu**  
- Location: **Mumbai**  
- Diet: **Vegetarian**  
- Lifestyle: **Non-smoker, doesn’t drink**  

Then, we only consider users who fit these criteria.  

```python
user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
if not user or not preferences:
    raise HTTPException(status_code=404, detail="User or preferences not found")
```

---

### **2. Find Users Who Meet These Preferences**  
The system then looks for profiles that match the preferences.  

```python
potential_matches = db.query(UserProfile).filter(
    UserProfile.gender != user.gender,
    UserProfile.age.between(preferences.preferred_age_min, preferences.preferred_age_max),
    (UserProfile.religion == preferences.preferred_religion) if preferences.preferred_religion else True,
    (UserProfile.work_location == preferences.preferred_location) if preferences.preferred_location else True,
    (UserProfile.diet == preferences.preferred_diet) if preferences.preferred_diet else True,
    (UserProfile.drinking_habits == preferences.preferred_drinking_habits) if preferences.preferred_drinking_habits else True,
    (UserProfile.smoking_habits == preferences.preferred_smoking_habits) if preferences.preferred_smoking_habits else True,
    UserProfile.id != user.id
).all()
```

---

### **3. Filter by Common Interests**  
Once we have a list of users who meet the preferences, we further filter them based on common interests.  

If a user loves **reading and traveling**, we prioritize matches who share at least one of these interests.  

```python
user_interests = set(json.loads(user.interests)) if user.interests else set()
matches = []

for match in potential_matches:
    match_interests = set(json.loads(match.interests)) if match.interests else set()
    if user_interests.intersection(match_interests):
        match.interests = list(match_interests)
        matches.append(match)
```

---

## **Final Output**  
The system returns a list of matched users with their profile details.  

### **Example Request**  
```http
GET /users/5/matches
```

### **Example Response**  
```json
[
    {
        "id": 8,
        "full_name": "Ananya Sharma",
        "gender": "Female",
        "age": 27,
        "religion": "Hindu",
        "work_location": "Mumbai",
        "diet": "Veg",
        "drinking_habits": "Never",
        "smoking_habits": "Never",
        "interests": ["Reading", "Traveling"]
    }
]
```

---

## **Why This Works Well**  
✅ **Accurate Matching** – Only shows profiles that fit the user’s criteria.  
✅ **Interest-Based Compatibility** – Ensures shared hobbies for better connections.  
✅ **Efficient Querying** – Uses database filters to keep the process fast.  

---

## **Future Enhancements**  
🔹 **AI Compatibility Score** – Rank matches based on deeper personality analysis.  
🔹 **Location-Based Matching** – Find people within a preferred distance.  
🔹 **Weighted Interest Matching** – Recommend users even if their interests don’t fully match but are similar.  

This feature ensures users get meaningful connections, making the matchmaking experience smooth and enjoyable! 🚀

### **5. Update User**
- **Endpoint:** `PUT /users/{user_id}`
- **Request Body:** (Same as `POST /users/`)
- **Response:**  
  Updates the user details.

---

### **6. Delete User**
- **Endpoint:** `DELETE /users/{user_id}`
- **Response:**  
  Returns a success message on deletion.

---

## **Database Models**
- **UserProfile**: Stores user details.
- **UserContact**: Stores email and phone.
- **UserPreferences**: Stores user’s matchmaking preferences.

## **Conclusion**
This API allows users to register, find matches, and manage their profiles efficiently.
