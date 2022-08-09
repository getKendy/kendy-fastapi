from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field


class TickerModel(BaseModel):
    '''Ticker class'''
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    date: datetime = Field(default_factory=datetime.now)
    symbol: str = Field(...)
    market: str = Field(...)
    close: float = Field(...)
    open: float = Field(...)
    high: float = Field(...)
    low: float = Field(...)
    volume: float = Field(...)
    quote: float = Field(...)

    class Config:
        '''Ticker model config'''
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "date": "2020-01-01T00:00:00.000000Z",
                "symbol": "BTCBUSD",
                "market": "BTC/BUSD",
                "close": 0.0,
                "open": 0.0,
                "high": 0.0,
                "low": 0.0,
                "volume": 0.0,
                "quote": 0.0
            }
        }
