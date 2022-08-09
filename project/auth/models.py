from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field


class LoginModel(BaseModel):
    '''User class'''
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        '''User model config'''
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "username": "",
                "password": '',
            }
        }


class TokenData(BaseModel):
    email: Optional[str] = None
