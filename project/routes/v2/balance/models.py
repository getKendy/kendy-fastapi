from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field


class BalanceModel(BaseModel):
    '''balance class'''
    apikey: str = Field(...)
    apisecret: str = Field(...)

    class Config:
        '''balance model config'''
        # allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "apikey": '',
                "apisecret": '',
            }
        }
