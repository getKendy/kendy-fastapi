from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field


class SettingModel(BaseModel):
    '''setting class'''
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str = Field(...)
    apikey: str = Field(...)
    apisecret: str = Field(...)
    createdAt: datetime = Field(...)
    modified: datetime = Field(...)
    
    class Config:
        '''setting model config'''
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "userid": '',
                "apikey": '',
                "apisecret": '',
            }
        }


class ShowSetting(SettingModel):
    '''Show setting model'''
    class Config:
        '''Show setting model config'''
        orm_mode = True,
        schema_extra = {
            "example": {
                "userid": '',
                "apikey": '',
                "apisecret": '',
            }
        }



class SettingUpdateModel(BaseModel):
    '''Update setting model'''
    userid: Optional[str]
    apikey: Optional[str]
    apisecret: Optional[str]
    modified: Optional[datetime]

    class Config:
        '''Update setting model config'''
        schema_extra = {
            "example": {
                "userid": '',
                "apikey": '',
                "apisecret": '',
            }
        }
