'''
baro routers
'''
from fastapi import APIRouter, Body, HTTPException, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .models import BaroModel, BaroUpdateModel, ShowBaro, ShowBarosTime
from fastapi_pagination import Page, paginate
from project.auth import oauth2
import pandas as pd

router = APIRouter(
    prefix="/api/v2/baro",
    tags=["Barometer"]
)


@router.post("/", response_description="Add new barometer")
async def create_baro(request: Request, baro: BaroModel = Body(...)):
    '''Add new barometer'''
    # print(baro)
    baro = jsonable_encoder(baro)
    new_baro = await request.app.mongodb["baros"].insert_one(baro)
    created_baro = await request.app.mongodb["baros"].find_one({'_id': new_baro.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_baro["_id"])


@router.get("/", response_description="Get all baros", response_model=Page[ShowBaro])
async def list_baros(request: Request):
    '''Get all baros'''
    baros = []
    for doc in await request.app.mongodb["baros"].find().to_list(length=None):
        baros.append(doc)
    return paginate(baros[::-1])


# @router.get("/{id}}", response_description="Get baro by id")
# async def show_baro(id: str, request: Request):
#     '''Get baro by id'''
#     if (task := await request.app.mongodb["baros"].find_one({"_id": id})) is not None:
#         return task
#     raise HTTPException(status_code=404, detail=f"baro {id} not found")

@router.get("/{timeframe}", response_description="Get baro by id", response_model=Page[ShowBarosTime])
async def show_baro_time(timeframe: str, request: Request):
    '''get baros time'''
    baros = []
    for doc in await request.app.mongodb["baros"].find().to_list(length=None):
        baros.append(doc)
    # print(baros)
    if timeframe == "1h":
        # print('1h')
        data = resample_baros("60T", baros)
        # print(data.id)
        return data
    if timeframe == "1d":
        data = resample_baros("D", baros)
        # print(data.id)
        return data
    if timeframe == "1w":
        data = resample_baros("W", baros)
        # print(data.id)
        return data
    if timeframe == "1m":
        data = resample_baros("M", baros)
        # print(data.id)
        return data


def resample_baros(timeframe, baros):
    '''resample baros'''
    df = pd.DataFrame(baros)
    df['date'] = pd.to_datetime(df['date'])
    # print(df.columns)
    # print(df)
    df = df.set_index('date')
    data = []
    # print(df)
    df = df.resample(timeframe).mean().interpolate()
    # df = df.resample(timeframe).mean().fillna(0)
    # print(df)
    # print(df.columns)
    # print(type(df))
    for index, row in df.iterrows():
        # print(index.strftime('%Y-%m-%d %H:%M:%S'))
        # print(row)
        data.append({
            "date": index.strftime('%m/%d/%Y, %H:%M'),
            "totalVolume": row['totalVolume'],
            "altBtcStrength": row['altBtcStrength'],
            "altEthStrength": row['altEthStrength'],
            "altBnbStrength": row['altBnbStrength'],
            "fiatBtcVolume": row['fiatBtcVolume'],
            "fiatEthVolume": row['fiatEthVolume'],
            "fiatBnbVolume": row['fiatBnbVolume'],
            "btcAltVolume": row['btcAltVolume'],
            "ethAltVolume": row['ethAltVolume'],
            "bnbAltVolume": row['bnbAltVolume']
        })
    data = data[::-1]
    return paginate(data)


@router.put("/{id}", response_description="Update a task")
async def update_baro(id: str, request: Request, baro: BaroUpdateModel = Body(...)):
    '''Update a baro'''
    baro = {k: v for k, v in baro.dict().items() if v is not None}

    if len(baro) >= 1:
        update_result = await request.app.mongodb["baros"].update_one(
            {"_id": id}, {"$set": baro}
        )

        if update_result.modified_count == 1:
            if (
                updated_baro := await request.app.mongodb["baros"].find_one({"_id": id})
            ) is not None:
                return updated_baro

    if (
        existing_baro := await request.app.mongodb["baros"].find_one({"_id": id})
    ) is not None:
        return existing_baro

    raise HTTPException(status_code=404, detail=f"baro {id} not found")


@router.delete("/{id}", response_description="Delete Task")
async def delete_baro(id: str, request: Request, current_user=Depends(oauth2.get_current_user)):
    '''Delete a baro'''
    delete_result = await request.app.mongodb["baros"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"baro {id} deleted")

    raise HTTPException(status_code=404, detail=f"baro {id} not found")
