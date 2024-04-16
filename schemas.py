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

class DrugReplacements(BaseModel):
    session_cookie: str
    drugid: int
    isMultiple: bool
    w1: float
    w2: float
    w3: float

class Favorite(BaseModel):
    session_cookie: str
    history_id: int

class UploadSnapshot(BaseModel):
    session_cookie: str
    file: str
