from fastapi import FastAPI, HTTPException, Request, Depends

from schemas import UserCreate, GetUser, DeleteUser, Login, SessionCookie, FileUpload, FileGet, FileDelete
from userFunctions import create_user, get_user_data_by_name, get_user_data_by_id, delete_user
from loginFunctions import login, is_session_cookie_valid, logout
from fileFunctions import upload_file, get_file_by_id, delete_file_by_id
from sqlalchemy.orm import Session
from database import get_db

import asyncpg
import asyncio

app = FastAPI()

DB_HOST = "database-1.cx4iqu0qqry4.us-east-1.rds.amazonaws.com"
DB_NAME = "postgres" 
DB_USER = "postgres"
DB_PASS = "seniordesign"

# Database connection pool
async def get_db():
    pool = await asyncpg.create_pool(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )
    try:
        yield pool
    finally:
        await pool.close()

async def get_db(request: Request):
    return request.app.state.db

@app.on_event("startup")
async def startup_event():
    await connect_to_db(app)

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.db.close()


# Hello World Call
@app.get("/")
async def hello_world(db=Depends(get_db)):
    try:
        # Attempt to execute a simple select query or any lightweight operation
        async with db.acquire() as connection:
            # This is a simple, non-intrusive query used just to check connectivity
            await connection.execute('SELECT 1')
        return {"about": "Hello World, database connectivity verified!"}
    except Exception as e:
        # If there's an error, it likely means there's an issue with the database connectivity
        raise HTTPException(status_code=500, detail="Database connectivity failed.") from e

# Database Check: The function attempts to execute a simple query (SELECT 1) that
# is guaranteed to succeed if the database connection is properly established. 
# This is a common technique for checking database connectivity without affecting any data.
# Dependency Injection: It uses FastAPI's dependency injection system (Depends(get_db)) to get a 
# database connection from the connection pool, ensuring efficient management of database connections.
# Error Handling: In case of any exceptions (which might occur if the database connection fails), 
# an HTTP 500 error is returned, indicating a server-side issue with the database connectivity. 
# This provides clear feedback that the API-to-database communication is not functioning as expected.

# User Calls
@app.post("/user/create")
async def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # It's important to check if the username or email already exists in the database.
    if await userFunctions.check_user_exists(db, user.username, user.email):
        raise HTTPException(status_code=400, detail="Username or email already exists.")
    await userFunctions.create_user(db, user.username, user.password, user.email)
    return {"message": "User created successfully."}

@app.get("/user/get")
async def get_user(get_user: schemas.GetUser, db: Session = Depends(get_db)):
    if get_user.username:
        user_data = await userFunctions.get_user_data_by_name(db, get_user.username)
    elif get_user.id:
        user_data = await userFunctions.get_user_data_by_id(db, get_user.id)
    else:
        raise HTTPException(status_code=400, detail="Invalid request parameters.")

    if user_data:
        return user_data
    else:
        raise HTTPException(status_code=404, detail="User not found.")
    
@app.delete("/user/delete")
async def delete_user_endpoint(delete_user_request: schemas.DeleteUser, db: Session = Depends(get_db)):
    user_id = delete_user_request.id
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid request.")

    # Verify the user exists before attempting to delete.
    if not await userFunctions.check_user_exists_by_id(db, user_id):
        raise HTTPException(status_code=404, detail="User not found.")
    
    await userFunctions.delete_user(db, user_id)
    return {"message": "User deleted successfully."}



# Login Calls
@app.get("/session/login")
async def user_login(login_data: schemas.Login, db=Depends(get_db)):
    login_result = await loginFunctions.login(db, login_data.username, login_data.password)
    if login_result is not None:
        session_cookie, timestamp = login_result
        return {"session_cookie": session_cookie, "timestamp": timestamp}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

@app.post("/session/is_session_cookie_valid")
async def check_session_cookie(session_cookie: schemas.SessionCookie, db=Depends(get_db)):
    if await loginFunctions.is_session_cookie_valid(db, session_cookie.session_cookie):
        return {"message": "Session cookie is valid."}
    else:
        raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")
    
@app.post("/session/logout")
async def user_logout(session_cookie: schemas.SessionCookie, db=Depends(get_db)):
    if await loginFunctions.is_session_cookie_valid(db, session_cookie.session_cookie):
        await loginFunctions.logout(db, session_cookie.session_cookie)
        return {"message": "User logged out successfully."}
    else:
        raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")

@app.post("/file/upload")
async def upload_file_endpoint(file_upload: schemas.FileUpload, db=Depends(get_db)):
    if await loginFunctions.is_session_cookie_valid(db, file_upload.session_cookie):
        await fileFunctions.upload_file(db, file_upload.url, file_upload.session_cookie)
        return {"message": "File uploaded successfully."}
    else:
        raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")
    
@app.get("/file/get")
async def get_file(file_get: schemas.FileGet, db=Depends(get_db)):
    if await loginFunctions.is_session_cookie_valid(db, file_get.session_cookie):
        file_data = await fileFunctions.get_file_by_id(db, file_get.id, file_get.session_cookie)
        if file_data:
            return file_data
        else:
            raise HTTPException(status_code=404, detail="File not found.")
    else:
        raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")
    
@app.delete("/file/delete")
async def delete_file(file_delete: schemas.FileDelete, db=Depends(get_db)):
    if await loginFunctions.is_session_cookie_valid(db, file_delete.session_cookie):
        await fileFunctions.delete_file_by_id(db, file_delete.id, file_delete.session_cookie)
        return {"message": "File deleted successfully."}
    else:
        raise HTTPException(status_code=401, detail="Session cookie is invalid or expired.")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)