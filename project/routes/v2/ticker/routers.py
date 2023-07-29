'''
ticker routers
'''

from typing import List
from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from requests import delete
import redis
from datetime import timedelta, datetime
import json
from .models import TickerModel, ShowTickerModel
from fastapi_pagination import Page, paginate
from project.celery_tasks import tasks
from os import environ
from dateutil.parser import parse

# r = redis.Redis(host="redis", port=6379, db=0)
binanceRedis = redis.Redis(host=environ.get('REDIS_CACHE'),
                port=environ.get('REDIS_PORT'),
                db=environ.get('REDIS_DB_BINANCE'))

kucoinRedis = redis.Redis(host=environ.get('REDIS_CACHE'),
                port=environ.get('REDIS_PORT'),
                db=environ.get('REDIS_DB_KUCOIN'))

router = APIRouter(
    prefix="/api/v2/ticker",
    tags=["Ticker"]
)


# @router.post("/", response_description="Add new ticker")
# async def create_ticker(request: Request, ticker: TickerModel = Body(...)):
#     '''Add new ticker'''
#     ticker = jsonable_encoder(ticker)
#     new_ticker = await request.app.mongodb["tickers"].insert_one(ticker)
#     created_ticker = await request.app.mongodb["tickers"].find_one({'_id': new_ticker.inserted_id})

#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_ticker["_id"])


@router.post("s/", response_description="Add new tickers")
async def create_tickers(request: Request, tickers: List[TickerModel] = Body(...)):
    '''Add new tickers'''
    # print(tickers)
    tickers = jsonable_encoder(tickers)
    await request.app.mongodb["tickers"].insert_many(tickers)
    # created_tickers = await request.app.mongodb["tickers"].find({'_id': {'$in': new_tickers.inserted_ids}})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content="created_tickers")


@router.get("/", response_description="Get all tickers", response_model=Page[ShowTickerModel])
async def list_tickers(exchange: str, request: Request):
    '''Get all tickers'''
    tickers = []
    for doc in await request.app.mongodb["tickers"].find({'exchange': exchange}).to_list(length=None):
        tickers.append(doc)
    return paginate(tickers)


@router.get("expired/{hours}", response_description="Remove all expired ticker ids")
async def list_expired_tickers(hours: int, request: Request):
    '''Remove all expired tickers'''
    tickers = []
    data = await request.app.mongodb["tickers"].find().to_list(length=10000)
    # FIX ?
    # compare_date = 'Fri, 31 Jan 2020 09:59:34 +0000 (UTC)'
    # datetime.now().timestamp() > parse(compare_date).timestamp()
    for x in range(len(data) - 1):
        # print(type(datetime.strptime(data[x]['date'],
        #   '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%s')))
        # print(type((datetime.now() - timedelta(hours=hours)).strftime('%s')))
        if len(tickers) < 10000:
            # if float(datetime.strptime(data[x]['date'], '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%s')) < float((datetime.utcnow() - timedelta(hours=hours)).strftime('%s')):
            if parse(data[x]['date']).timestamp() < (datetime.now() - timedelta(hours=hours)).timestamp():
                # print('processing')
                await request.app.mongodb["tickers"].delete_one({"_id": data[x]["_id"]})
                tickers.append(data[x])
    return 'Deleted: ' + str(len(tickers)) + ' of ' + str(len(data)) + ' tickers'


@router.get('/{symbol}', status_code=status.HTTP_200_OK, response_description="Get ticker by symbol", response_model=TickerModel)
async def get_ticker(symbol: str, exchange: str, request: Request):
    '''Get ticker by symbol'''
    tickers = []
    for doc in await request.app.mongodb["tickers"].find({'symbol': symbol, 'exchange': exchange}).to_list(length=None):
        tickers.append(doc)

    if not tickers:
        raise HTTPException(
            status_code=404, detail=f"ticker {symbol} not found")
    return tickers[::-1][0]


@router.get('s/{symbol}', status_code=status.HTTP_200_OK, response_description="Get multiple tickers by symbol")
async def get_tickers_by_symbol(symbol: str, exchange: str, request: Request):
    '''Get tickers by symbol'''
    tickers = []
    for doc in await request.app.mongodb["tickers"].find({'symbol': symbol, 'exchange': exchange}).to_list(length=None):
        tickers.append(doc)

    if not tickers:
        raise HTTPException(
            status_code=404, detail=f"ticker {symbol} not found")
    return tickers


@router.delete("/{id}", response_description="Delete ticker")
async def delete_ticker(id: str, request: Request):
    '''Delete ticker'''
    deleted_result = await request.app.mongodb["tickers"].delete_one({"_id": id})
    if deleted_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"ticker {id} deleted")

    raise HTTPException(status_code=404, detail=f"ticker {id} not found")


@router.get('redis/{symbol}', status_code=status.HTTP_200_OK)
def get_redis(symbol:str, exchange: str):
    '''Get redis'''
    try:
        if exchange == 'binance':
            data = dict(json.loads(binanceRedis.get(symbol)))
        elif exchange == 'kucoin':
            data = dict(json.loads(kucoinRedis.get(symbol)))
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No tickers found")
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No tickers found")
    # tickers = []
    # for d in data['tickers']:
    #     # print(d)
    #     tickers.append(
    #         {'symbol': d['symbol'], 'market': d['market'], 'close': d['c'],
    #             'high': d['h'], 'low': d['l'], 'open': d['o'], 'volume': d['v'], 'quote': d['q']}
    #     )
    return data
