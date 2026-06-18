
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class postbase(BaseModel):
    title:str
    content:str
    published:bool = True 

class postcreate(postbase):
    pass

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class userresponse(BaseModel):
    email:EmailStr
    id:int

    class Config:
        orm_mode = True

class postresponse(BaseModel):
    title:str
    content:str
    published:bool
    created_at:datetime
    Owner_id:int
    owner:userresponse


    class Config:
        orm_mode = True

class userlogin(BaseModel):
    email:EmailStr
    password:str

class token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)