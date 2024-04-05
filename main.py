from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import logging

from schemas import UserCreate, GetUser, DeleteUser, Login, SessionCookie, DrugReplacements, Favorite, UploadSnapshot
from userFunctions import create_user, get_user_data_by_name, get_user_data_by_id, delete_user
from loginFunctions import login, is_session_cookie_valid, logout
from replacmentsFunctions import replacements
from historyFunctions import getHistory, addToFavorites, removeFromFavorites, getFavorites
from s3Functions import upload_snapshot

# Setup logging
logging.basicConfig(filename='backend.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI(docs_url="/documentation", redoc_url=None)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup
@app.get("/api/test")
async def test():
    logging.info("Accessed the test endpoint")
    return "Hello World!"

# Hello World Call
@app.get("/")
async def hello_world():
    logging.info("Accessed the root endpoint")
    return {"about": "Welcome to PAPO API! -- See /documentation for more details"}

# User Calls (CRUD Operations)
@app.post("/user/create")  # Creating a new user
async def create_new_user(user: UserCreate):
    try:
        create_user(
            user.username,
            user.password,
            user.center,
            user.permission,
            user.employeeid,
            user.islocked
        )
        logging.info(f"User created: {user.username}")
        return {"message": "User created successfully."}
    except Exception as e:
        logging.error(f"Error creating user {user.username}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/user/get")  # Getting user by ID or username
async def get_user(get_user: GetUser):
    try:
        if get_user.username:
            user_data = get_user_data_by_name(get_user.username)
            if user_data:
                logging.info(f"Retrieved user by username: {get_user.username}")
                return user_data
            else:
                logging.warning(f"User not found by username: {get_user.username}")
                raise HTTPException(status_code=404, detail="User not found.")
        elif get_user.id:
            user_data = get_user_data_by_id(get_user.id)
            if user_data:
                logging.info(f"Retrieved user by ID: {get_user.id}")
                return user_data
            else:
                logging.warning(f"User not found by ID: {get_user.id}")
                raise HTTPException(status_code=404, detail="User not found.")
        else:
            logging.error("Invalid request for getting user")
            raise HTTPException(status_code=400, detail="Invalid request.")
    except Exception as e:
        logging.error(f"Error retrieving user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
@app.delete("/user/delete")  # Deleting a user by ID
async def delete_user_endpoint(delete_user_request: DeleteUser):
    try:
        user_id = delete_user_request.id
        if user_id:
            user_data = get_user_data_by_id(user_id)
            if user_data:
                delete_user(user_id)  # Assuming you have a function to delete a user by ID
                logging.info(f"User deleted successfully: {user_id}")
                return {"message": "User deleted successfully."}
            else:
                logging.warning(f"User not found for deletion: {user_id}")
                raise HTTPException(status_code=404, detail="User not found.")
        else:
            logging.error("Invalid request for deleting user")
            raise HTTPException(status_code=400, detail="Invalid request.")
    except Exception as e:
        logging.error(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Login Calls
@app.post("/session/login")  # Login function
async def user_login(login_data: Login):
    try:
        login_result = login(login_data.username, login_data.password)
        if login_result is not None:
            session_cookie, timestamp = login_result
            logging.info(f"User logged in: {login_data.username}")
            return {"session_cookie": session_cookie, "timestamp": timestamp}
        else:
            logging.warning(f"Invalid login attempt: {login_data.username}")
            raise HTTPException(status_code=401, detail="Invalid credentials.")
    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/session/is_session_cookie_valid")  # Check if the session cookie is valid
async def check_session_cookie(session_cookie: SessionCookie):
    if is_session_cookie_valid(session_cookie.session_cookie):
        logging.info("Session cookie validated successfully")
        return {"message": "Session cookie is valid."}
    else:
        logging.warning("Invalid or expired session cookie")
        raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")
    
@app.post("/session/logout")  # Logout function
async def user_logout(session_cookie: SessionCookie):
    try:
        if is_session_cookie_valid(session_cookie.session_cookie):
            logout(session_cookie.session_cookie)
            logging.info("User logged out successfully")
            return {"message": "User logged out successfully."}
        else:
            logging.warning("Attempted logout with invalid or expired session cookie")
            raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")
    except Exception as e:
        logging.error(f"Error during logout: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
# Drug Calls
@app.post("/drugs/replacements")  # Upload a file
async def get_drug_replacements(drug_replacements: DrugReplacements):
    try:
        if is_session_cookie_valid(drug_replacements.session_cookie):
            result = replacements(drug_replacements.session_cookie,
                                  drug_replacements.drugid, 
                                  drug_replacements.isMultiple,
                                  drug_replacements.w1, 
                                  drug_replacements.w2, 
                                  drug_replacements.w3)
            logging.info("Drug replacements retrieved successfully")
            return result
        else:
            logging.warning("Invalid or expired session cookie for drug replacements")
            raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")
    except Exception as e:
        logging.error(f"Error retrieving drug replacements: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
# History Calls
@app.post("/history/get")  # Get the history of a user
async def get_user_history(session_cookie: SessionCookie):
    try:
        if is_session_cookie_valid(session_cookie.session_cookie):
            history = getHistory(session_cookie.session_cookie)
            logging.info("User history retrieved successfully")
            return history
        else:
            logging.warning("Invalid or expired session cookie for getting history")
            raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")
    except Exception as e:
        logging.error(f"Error retrieving user history: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@app.post("/history/add_to_favorites")  # Add a history item to favorites
async def add_to_favorites(favorite_data: Favorite):
    try:
        if is_session_cookie_valid(favorite_data.session_cookie):
            addToFavorites(favorite_data.session_cookie, favorite_data.history_id)
            logging.info("Item added to favorites successfully")
            return {"message": "Item added to favorites."}
        else:
            logging.warning("Invalid or expired session cookie for adding to favorites")
            raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")
    except Exception as e:
        logging.error(f"Error adding item to favorites: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@app.post("/history/remove_from_favorites")  # Remove a history item from favorites
async def remove_from_favorites(favorite_data: Favorite):
    try:
        if is_session_cookie_valid(favorite_data.session_cookie):
            removeFromFavorites(favorite_data.session_cookie, favorite_data.history_id)
            logging.info("Item removed from favorites successfully")
            return {"message": "Item removed from favorites."}
        else:
            logging.warning("Invalid or expired session cookie for removing from favorites")
            raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")
    except Exception as e:
        logging.error(f"Error removing item from favorites: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@app.get("/history/get_favorites")  # Get the favorites of a user
async def get_user_favorites(session_cookie: SessionCookie):
    try:
        if is_session_cookie_valid(session_cookie.session_cookie):
            favorites = getFavorites(session_cookie.session_cookie)
            logging.info("User favorites retrieved successfully")
            return favorites
        else:
            logging.warning("Invalid or expired session cookie for getting favorites")
            raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")
    except Exception as e:
        logging.error(f"Error retrieving user favorites: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
# Snapshot Calls
@app.post("/snapshot/upload")  # Upload a snapshot
async def upload_snapshot_endpoint(snapshot: UploadSnapshot):
    try:
        if is_session_cookie_valid(snapshot.session_cookie):
            # Save the file
            with open("snapshot.csv", "wb") as file_object:
                file_object.write(snapshot.file.file.read())

            # Upload the snapshot
            upload_snapshot("snapshot.csv")

            logging.info("Snapshot uploaded successfully")
            return {"message": "Snapshot uploaded successfully."}
        else:
            logging.warning("Invalid or expired session cookie for uploading snapshot")
            raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")
    except Exception as e:
        logging.error(f"Error uploading snapshot: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Run the app
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # uvicorn.run(app, host="127.0.0.1", port=8000)
    
