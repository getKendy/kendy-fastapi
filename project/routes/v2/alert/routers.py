'''
baro routers
'''
from fastapi import APIRouter, Body, HTTPException, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .models import AlertModel, ShowAlert
from fastapi_pagination import Page, paginate
from datetime import datetime, timedelta
from dateutil.parser import parse
from project.auth import oauth2
from typing import Annotated
from ..users.models import UserMeModel

# from project.auth import oauth2
# import pandas as pd

router = APIRouter(
    prefix="/api/v2/alert",
    tags=["Alert"]
)


@router.post("/", response_description="Add new alert")
async def create_alert(request: Request, current_user: Annotated[UserMeModel, Depends(oauth2.get_current_user)], alert: AlertModel = Body(...)):
    '''Add new alertmeter'''
    # print(alert)
    alert = jsonable_encoder(alert)
    new_alert = await request.app.mongodb["alerts"].insert_one(alert)
    created_alert = await request.app.mongodb["alerts"].find_one({'_id': new_alert.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_alert["_id"])


@router.get("/", response_description="Get all alerts", response_model=Page[ShowAlert])
async def list_alerts(exchange: str, request: Request, current_user: Annotated[UserMeModel, Depends(oauth2.get_current_user)]):
    '''Get all alerts'''
    alerts = []
    if exchange == 'all':
        for doc in await request.app.mongodb["alerts"].find().to_list(length=None):
            alerts.append(doc)
    else:
        for doc in await request.app.mongodb["alerts"].find({ "exchange": exchange }).to_list(length=None):
            alerts.append(doc)
    return paginate(alerts[::-1])


@router.get("expired/{hours}", response_description="Remove all expired alert ids")
async def list_expired_tickers(hours: int, request: Request, current_user: Annotated[UserMeModel, Depends(oauth2.get_current_user)]):
    '''Remove all expired tickers'''
    alerts = []
    data = await request.app.mongodb["alerts"].find().to_list(length=100)
    # FIX ?
    # compare_date = 'Fri, 31 Jan 2020 09:59:34 +0000 (UTC)'
    # datetime.now().timestamp() > parse(compare_date).timestamp()
    for x in range(len(data) - 1):
        # print(type(datetime.strptime(data[x]['date'],
        #   '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%s')))
        # print(type((datetime.now() - timedelta(hours=hours)).strftime('%s')))
        if len(alerts) < 100:
            # if float(datetime.strptime(data[x]['date'], '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%s')) < float((datetime.utcnow() - timedelta(hours=hours)).strftime('%s')):
            if parse(data[x]['date']).timestamp() < (datetime.now() - timedelta(hours=hours)).timestamp():
                # print('processing')
                await request.app.mongodb["alerts"].delete_one({"_id": data[x]["_id"]})
                alerts.append(data[x])
    return 'Deleted: ' + str(len(alerts)) + ' of ' + str(len(data)) + ' alerts'