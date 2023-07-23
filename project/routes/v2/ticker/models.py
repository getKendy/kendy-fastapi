# from datetime import datetime
from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field


class TickerModel(BaseModel):
    '''Ticker class'''
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    date: datetime = Field(...)
    exchange: str = Field(...)
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
                "date": 0,
                "exchange": "binance",
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

class ShowTickerModel(TickerModel):
    '''Show alert model'''
    class Config:
        '''Show alert model config'''
        orm_mode = True,
        schema_extra = {
            "example": {
                "date": 0,
                "exchange": "binance",
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