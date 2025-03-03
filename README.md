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
- **Endpoint:** `GET /users/{user_id}/matches`
- **Response:**  
  Returns a list of potential matches based on user preferences.

---

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
