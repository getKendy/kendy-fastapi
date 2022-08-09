from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field


class UserModel(BaseModel):
    '''User class'''
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    date: datetime = Field(default_factory=datetime.now)
    name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        '''User model config'''
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "date": "2020-01-01T00:00:00.000000Z",
                "name": "",
                "email": "",
                "password": '',
            }
        }


class UserMeModel(BaseModel):
    '''User class'''
    id: str
    date: datetime
    name: str
    email: str
    # password: str = Field(...)

    class Config:
        '''User model config'''
        orm_mode = True
