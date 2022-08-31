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

# from project.auth import oauth2
# import pandas as pd

router = APIRouter(
    prefix="/api/v2/alert",
    tags=["Alert"]
)


@router.post("/", response_description="Add new alert")
async def create_alert(request: Request, alert: AlertModel = Body(...)):
    '''Add new alertmeter'''
    # print(alert)
    alert = jsonable_encoder(alert)
    new_alert = await request.app.mongodb["alerts"].insert_one(alert)
    created_alert = await request.app.mongodb["alerts"].find_one({'_id': new_alert.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_alert["_id"])


@router.get("/", response_description="Get all alerts", response_model=Page[ShowAlert])
async def list_alerts(request: Request):
    '''Get all alerts'''
    alerts = []
    for doc in await request.app.mongodb["alerts"].find().to_list(length=None):
        alerts.append(doc)
    return paginate(alerts[::-1])


# @router.get("/{id}}", response_description="Get baro by id")
# async def show_baro(id: str, request: Request):
#     '''Get baro by id'''
#     if (task := await request.app.mongodb["baros"].find_one({"_id": id})) is not None:
#         return task
#     raise HTTPException(status_code=404, detail=f"baro {id} not found")

# @router.get("/{timeframe}", response_description="Get baro by id", response_model=Page[ShowBarosTime])
# async def show_baro_time(timeframe: str, request: Request):
#     '''get baros time'''
#     baros = []
#     for doc in await request.app.mongodb["baros"].find().to_list(length=None):
#         baros.append(doc)
#     # print(baros)
#     if timeframe == "1h":
#         # print('1h')
#         data = resample_baros("60T", baros)
#         # print(data.id)
#         return data
#     if timeframe == "1d":
#         data = resample_baros("D", baros)
#         # print(data.id)
#         return data
#     if timeframe == "1w":
#         data = resample_baros("W", baros)
#         # print(data.id)
#         return data
#     if timeframe == "1m":
#         data = resample_baros("M", baros)
#         # print(data.id)
#         return data


# def resample_baros(timeframe, baros):
#     '''resample baros'''
#     df = pd.DataFrame(baros)
#     df['date'] = pd.to_datetime(df['date'])
#     # print(df.columns)
#     # print(df)
#     df = df.set_index('date')
#     data = []
#     # print(df)
#     df = df.resample(timeframe).mean().interpolate()
#     # df = df.resample(timeframe).mean().fillna(0)
#     # print(df)
#     # print(df.columns)
#     # print(type(df))
#     for index, row in df.iterrows():
#         # print(index.strftime('%Y-%m-%d %H:%M:%S'))
#         # print(row)
#         data.append({
#             "date": index.strftime('%m/%d/%Y, %H:%M'),
#             "totalVolume": row['totalVolume'],
#             "altBtcStrength": row['altBtcStrength'],
#             "altEthStrength": row['altEthStrength'],
#             "altBnbStrength": row['altBnbStrength'],
#             "fiatBtcVolume": row['fiatBtcVolume'],
#             "fiatEthVolume": row['fiatEthVolume'],
#             "fiatBnbVolume": row['fiatBnbVolume'],
#             "btcAltVolume": row['btcAltVolume'],
#             "ethAltVolume": row['ethAltVolume'],
#             "bnbAltVolume": row['bnbAltVolume']
#         })
#     data = data[::-1]
#     return paginate(data)


# @router.put("/{id}", response_description="Update a task")
# async def update_baro(id: str, request: Request, baro: BaroUpdateModel = Body(...)):
#     '''Update a baro'''
#     baro = {k: v for k, v in baro.dict().items() if v is not None}

#     if len(baro) >= 1:
#         update_result = await request.app.mongodb["baros"].update_one(
#             {"_id": id}, {"$set": baro}
#         )

#         if update_result.modified_count == 1:
#             if (
#                 updated_baro := await request.app.mongodb["baros"].find_one({"_id": id})
#             ) is not None:
#                 return updated_baro

#     if (
#         existing_baro := await request.app.mongodb["baros"].find_one({"_id": id})
#     ) is not None:
#         return existing_baro

#     raise HTTPException(status_code=404, detail=f"baro {id} not found")


# @router.delete("/{id}", response_description="Delete Task")
# async def delete_baro(id: str, request: Request, current_user=Depends(oauth2.get_current_user)):
#     '''Delete a baro'''
#     delete_result = await request.app.mongodb["baros"].delete_one({"_id": id})

#     if delete_result.deleted_count == 1:
#         return JSONResponse(status_code=status.HTTP_200_OK, content=f"baro {id} deleted")

#     raise HTTPException(status_code=404, detail=f"baro {id} not found")


@router.get("expired/{hours}", response_description="Remove all expired alert ids")
async def list_expired_tickers(hours: int, request: Request):
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