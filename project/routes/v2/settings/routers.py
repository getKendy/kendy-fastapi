'''
setting routers
'''
from fastapi import APIRouter, Body, HTTPException, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from project.auth import oauth2
from .models import SettingModel, SettingUpdateModel, ShowSetting
from fastapi_pagination import Page, paginate
import pandas as pd

router = APIRouter(
    prefix="/api/v2/settings",
    tags=["Settings"]
)


@router.post("/", response_description="Add new setting")
async def create_setting(request: Request, setting: SettingModel = Body(...), current_user=Depends(oauth2.get_current_user)):
    '''Add new setting'''
    # print(setting)
    setting = jsonable_encoder(setting)
    new_setting = await request.app.mongodb["settings"].insert_one(setting)
    created_setting = await request.app.mongodb["settings"].find_one({'_id': new_setting.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_setting["_id"])


@router.get("/", response_description="Get all settings", response_model=Page[ShowSetting])
async def list_settings(request: Request, current_user=Depends(oauth2.get_current_user)):
    '''Get all settings'''
    settings = []
    for doc in await request.app.mongodb["settings"].find().to_list(length=None):
        settings.append(doc)
    return paginate(settings[::-1])


@router.get("/{id}/{userid}", response_description="Get setting by id and userid")
async def show_setting(id: str, userid: str, request: Request, current_user=Depends(oauth2.get_current_user)):
    '''Get setting by id and userid'''
    if (setting := await request.app.mongodb["settings"].find_one({"_id": id, "userid": userid})) is not None:
        return setting
    raise HTTPException(
        status_code=404, detail=f"setting {id} not found for user {current_user._id}")


@router.put("/{id}", response_description="Update a task")
async def update_setting(id: str, request: Request, setting: SettingUpdateModel = Body(...), current_user=Depends(oauth2.get_current_user)):
    '''Update a setting'''
    setting = {k: v for k, v in setting.dict().items() if v is not None}

    if len(setting) >= 1:
        update_result = await request.app.mongodb["settings"].update_one(
            {"_id": id}, {"$set": setting}
        )

        if update_result.modified_count == 1:
            if (
                updated_setting := await request.app.mongodb["settings"].find_one({"_id": id})
            ) is not None:
                return updated_setting

    if (
        existing_setting := await request.app.mongodb["settings"].find_one({"_id": id})
    ) is not None:
        return existing_setting

    raise HTTPException(status_code=404, detail=f"setting {id} not found")


@router.delete("/{id}", response_description="Delete Task")
async def delete_setting(id: str, request: Request, current_user=Depends(oauth2.get_current_user)):
    '''Delete a setting'''
    delete_result = await request.app.mongodb["settings"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "setting deleted"})

    raise HTTPException(status_code=404, detail=f"setting {id} not found")
