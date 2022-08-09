from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field



class BaroModel(BaseModel):
    '''Siahost class'''
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    fiatBtcVolume: float = Field(...)
    fiatBnbVolume: float = Field(...)
    fiatEthVolume: float = Field(...)
    btcAltVolume: float = Field(...)
    ethAltVolume: float = Field(...)
    bnbAltVolume: float = Field(...)
    totalVolume: float = Field(...)
    altBtcStrength: float = Field(...)
    altEthStrength: float = Field(...)
    altBnbStrength: float = Field(...)
    total_brl_alt_volume_usdt: float = Field(...)
    total_bkrw_alt_volume_usdt: float = Field(...)
    total_aud_alt_volume_usdt: float = Field(...)
    total_doge_alt_volume_usdt: float = Field(...)
    total_rub_alt_volume_usdt: float = Field(...)
    total_trx_alt_volume_usdt: float = Field(...)
    total_zar_alt_volume_usdt: float = Field(...)
    total_bidr_alt_volume_usdt: float = Field(...)
    total_try_alt_volume_usdt: float = Field(...)
    total_ngn_alt_volume_usdt: float = Field(...)
    total_xrp_alt_volume_usdt: float = Field(...)
    total_bvnd_alt_volume_usdt: float = Field(...)
    total_gyen_alt_volume_usdt: float = Field(...)
    total_idrt_alt_volume_usdt: float = Field(...)
    total_dot_alt_volume_usdt: float = Field(...)
    total_vai_alt_volume_usdt: float = Field(...)
    total_dai_alt_volume_usdt: float = Field(...)
    total_pax_alt_volume_usdt: float = Field(...)
    total_usds_alt_volume_usdt: float = Field(...)
    total_uah_alt_volume_usdt: float = Field(...)
    total_ust_alt_volume_usdt: float = Field(...)
    total_eur_alt_volume_usdt: float = Field(...)
    total_busd_alt_volume_usdt: float = Field(...)
    total_usdc_alt_volume_usdt: float = Field(...)
    total_usdp_alt_volume_usdt: float = Field(...)
    total_gbp_alt_volume_usdt: float = Field(...)
    date: datetime = Field(default_factory=datetime.now)

    class Config:
        '''Task model config'''
        allow_population_by_field_name = True
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


class ShowBaro(BaroModel):
    '''Show baro model'''
    class Config:
        '''Show baro model config'''
        orm_mode = True,
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
                "total_pax_alt_volume_usdt": 0.
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
