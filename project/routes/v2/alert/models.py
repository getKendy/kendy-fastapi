from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field


class AlertModel(BaseModel):
    '''AlertModel class'''
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    symbol: str = Field(...)
    market: str = Field(...)
    close: float = Field(...)
    volume: float = Field(...)
    quote: float = Field(...)
    bbl: float = Field(...)
    bbm: float = Field(...)
    bbu: float = Field(...)
    bbb: float = Field(...)
    stochk: float = Field(...)
    stockd: float = Field(...)
    date: datetime = Field(...)

    class Config:
        '''Task model config'''
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                'symbol': '',
                'market': '',
                'close': '',
                'volume': '',
                'quote': '',
                'bbl': '',
                'bbm': '',
                'bbu': '',
                'bbb': '',
                'stochk': '',
                'stockd': '',
                'date': ''
            }
        }


class ShowAlert(AlertModel):
    '''Show alert model'''
    class Config:
        '''Show alert model config'''
        orm_mode = True,
        schema_extra = {
            "example": {
                'symbol': '',
                'market': '',
                'close': '',
                'volume': '',
                'quote': '',
                'bbl': '',
                'bbm': '',
                'bbu': '',
                'bbb': '',
                'stochk': '',
                'stockd': '',
                'date': ''
            }
        }


class ShowBarosTime(BaseModel):
    '''Show baros time model'''
    date: str
    fiatBtcVolume: str
    fiatBnbVolume: str
    fiatEthVolume: str
    btcAltVolume: str
    ethAltVolume: str
    bnbAltVolume: str
    totalVolume: str
    altBtcStrength: str
    altEthStrength: str
    altBnbStrength: str

    class Config():
        '''Show baros time model config'''
        orm_mode = True


class BaroUpdateModel(BaseModel):
    '''Update task model'''
    fiatBtcVolume: Optional[float]
    fiatBnbVolume: Optional[float]
    fiatEthVolume: Optional[float]
    btcAltVolume: Optional[float]
    ethAltVolume: Optional[float]
    bnbAltVolume: Optional[float]
    totalVolume: Optional[float]
    altBtcStrength: Optional[float]
    altEthStrength: Optional[float]
    altBnbStrength: Optional[float]
    total_brl_alt_volume_usdt: Optional[float]
    total_bkrw_alt_volume_usdt: Optional[float]
    total_aud_alt_volume_usdt: Optional[float]
    total_doge_alt_volume_usdt: Optional[float]
    total_rub_alt_volume_usdt: Optional[float]
    total_trx_alt_volume_usdt: Optional[float]
    total_zar_alt_volume_usdt: Optional[float]
    total_bidr_alt_volume_usdt: Optional[float]
    total_try_alt_volume_usdt: Optional[float]
    total_ngn_alt_volume_usdt: Optional[float]
    total_xrp_alt_volume_usdt: Optional[float]
    total_bvnd_alt_volume_usdt: Optional[float]
    total_gyen_alt_volume_usdt: Optional[float]
    total_idrt_alt_volume_usdt: Optional[float]
    total_dot_alt_volume_usdt: Optional[float]
    total_vai_alt_volume_usdt: Optional[float]
    total_dai_alt_volume_usdt: Optional[float]
    total_pax_alt_volume_usdt: Optional[float]
    total_usds_alt_volume_usdt: Optional[float]
    total_uah_alt_volume_usdt: Optional[float]
    total_ust_alt_volume_usdt: Optional[float]
    total_eur_alt_volume_usdt: Optional[float]
    total_busd_alt_volume_usdt: Optional[float]
    total_usdc_alt_volume_usdt: Optional[float]
    total_usdp_alt_volume_usdt: Optional[float]
    total_gbp_alt_volume_usdt: Optional[float]

    date: Optional[datetime]

    class Config:
        '''Update task model config'''
        schema_extra = {
            "example": {
                "fiatBtcVolume": 0.0,
                "fiatBnbVolume": 0.0,
                "fiatEthVolume": 0.0,
                "btcAltVolume": 0.0,
                "ethAltVolume": 0.0,
                "bnbAltVolume": 0.0,
                "totalVolume": 0.0,
                "altBtcStrength": 0.0,
                "altEthStrength": 0.0,
                "altBnbStrength": 0.0,
                "total_brl_alt_volume_usdt": 0.0,
                "total_bkrw_alt_volume_usdt": 0.0,
                "total_aud_alt_volume_usdt": 0.0,
                "total_doge_alt_volume_usdt": 0.0,
                "total_rub_alt_volume_usdt": 0.0,
                "total_trx_alt_volume_usdt": 0.0,
                "total_zar_alt_volume_usdt": 0.0,
                "total_bidr_alt_volume_usdt": 0.0,
                "total_try_alt_volume_usdt": 0.0,
                "total_ngn_alt_volume_usdt": 0.0,
                "total_xrp_alt_volume_usdt": 0.0,
                "total_bvnd_alt_volume_usdt": 0.0,
                "total_gyen_alt_volume_usdt": 0.0,
                "total_idrt_alt_volume_usdt": 0.0,
                "total_dot_alt_volume_usdt": 0.0,
                "total_vai_alt_volume_usdt": 0.0,
                "total_dai_alt_volume_usdt": 0.0,
                "total_pax_alt_volume_usdt": 0.0,
                "total_usds_alt_volume_usdt": 0.0,
                "total_uah_alt_volume_usdt": 0.0,
                "total_ust_alt_volume_usdt": 0.0,
                "total_eur_alt_volume_usdt": 0.0,
                "total_busd_alt_volume_usdt": 0.0,
                "total_usdc_alt_volume_usdt": 0.0,
                "total_usdp_alt_volume_usdt": 0.0,
                "total_gbp_alt_volume_usdt": 0.0,
            }
        }
