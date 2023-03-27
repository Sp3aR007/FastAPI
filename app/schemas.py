from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class Post(BaseModel):
        title: str
        content: str
        published: bool = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
     
    class Config:
        orm_mode = True
        
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut #Return the pydantic model

    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id : int
    dir: conint(le=1)  

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
