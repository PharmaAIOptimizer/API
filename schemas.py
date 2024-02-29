from pydantic import BaseModel
from typing import Optional

# Define Pydantic models for data validation
class UserCreate(BaseModel):
    username: str
    password: str
    center: int
    permission: int
    employeeid: int
    islocked: bool

class GetUser(BaseModel):
    username: Optional[str] = None
    id: Optional[int] = None

class DeleteUser(BaseModel):
    id: int

class Login(BaseModel):
    username: str
    password: str

class SessionCookie(BaseModel):
    session_cookie: str

class FileUpload(BaseModel):
    url: str
    session_cookie: str

class FileDelete(BaseModel):
    id: int
    session_cookie: str

class FileGet(BaseModel):
    id: int
    session_cookie: str
