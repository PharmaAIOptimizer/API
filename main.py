from fastapi import FastAPI, HTTPException, Request

from schemas import UserCreate, GetUser, DeleteUser, Login, SessionCookie, FileUpload, FileGet, FileDelete
from userFunctions import create_user, get_user_data_by_name, get_user_data_by_id, delete_user
from loginFunctions import login, is_session_cookie_valid, logout
from fileFunctions import upload_file, get_file_by_id, delete_file_by_id

app = FastAPI()

# Hello World Call
@app.get("/")
async def hello_world():
    return {"about": "Hello World!"}


# User Calls
@app.post("/user/create") # Creating a new user
async def create_new_user(user: UserCreate):
    create_user(user.username, user.password, user.email)
    return {"message": "User created successfully."}

@app.get("/user/get") # Getting user by ID or username
async def get_user(get_user: GetUser):
    if get_user.username:
        user_data = get_user_data_by_name(get_user.username)
        if user_data:
            return user_data
        else:
            raise HTTPException(status_code=404, detail="User not found.")
    elif get_user.id:
        user_data = get_user_data_by_id(get_user.id)
        if user_data:
            return user_data
        else:
            raise HTTPException(status_code=404, detail="User not found.")
    else:
        raise HTTPException(status_code=400, detail="Invalid request.")
    
    
@app.delete("/user/delete") # Deleting a user by ID
async def delete_user_endpoint(delete_user_request: DeleteUser):
    user_id = delete_user_request.id

    if user_id:
        user_data = get_user_data_by_id(user_id)
        if user_data:
            delete_user(user_id)  # Assuming you have a function to delete a user by ID
            return {"message": "User deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail="User not found.")
    else:
        raise HTTPException(status_code=400, detail="Invalid request.")


# Login Calls
@app.get("/session/login")  # Login function
async def user_login(login_data: Login):
    login_result = login(login_data.username, login_data.password)
    if login_result is not None:
        session_cookie, timestamp = login_result
        return {"session_cookie": session_cookie, "timestamp": timestamp}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

@app.post("/session/is_session_cookie_valid")  # Check if the session cookie is valid
async def check_session_cookie(session_cookie: SessionCookie):
    if is_session_cookie_valid(session_cookie.session_cookie):
        return {"message": "Session cookie is valid."}
    else:
        raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")
    
@app.post("/session/logout")  # Logout function
async def user_logout(session_cookie: SessionCookie):
    if is_session_cookie_valid(session_cookie.session_cookie):
        logout(session_cookie.session_cookie)
        return {"message": "User logged out successfully."}
    else:
        raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")


# File Calls
@app.post("/file/upload")  # Upload file
async def upload_file_endpoint(file_upload: FileUpload):
    if is_session_cookie_valid(file_upload.session_cookie):
        upload_file(file_upload.url, file_upload.session_cookie)
        return {"message": "File uploaded successfully."}
    else:
        raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")
    
@app.get("/file/get")  # Get file by ID
async def get_file(file_get: FileGet):
    if is_session_cookie_valid(file_get.session_cookie):
        file_data = get_file_by_id(file_get.id, file_get.session_cookie)
        if file_data:
            return file_data
        else:
            raise HTTPException(status_code=404, detail="File not found.")
    else:
        raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")
    
@app.delete("/file/delete")  # Delete file by ID
async def delete_file(file_delete: FileDelete):
    if is_session_cookie_valid(file_delete.session_cookie):
        delete_file_by_id(file_delete.id, file_delete.session_cookie)
        return {"message": "File deleted successfully."}
    else:
        raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
