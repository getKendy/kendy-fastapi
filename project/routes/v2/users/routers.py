'''
ticker routers
'''
from ast import Try
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from requests import delete
import redis
import json
from project.auth import oauth2
from .models import UserModel, UserMeModel
from fastapi_pagination import Page, paginate
from project.celery_tasks import tasks
from project.auth.hashing import Hash
# r = redis.Redis(host="redis", port=6379, db=0)

router = APIRouter(
    prefix="/api/v2/user",
    tags=["User"]
)


@router.post("/", response_description="Add new user")
async def create_user(request: Request, user: UserModel = Body(...)):
    '''Add new user'''
    user = jsonable_encoder(user)
    print(user)
    user = {
        "_id": user['_id'],
        "date": user['date'],
        "name": user['name'],
        "email": user['email'],
        "password": Hash.bcrypt(user['password'])
    }
    print(user)
    new_user = await request.app.mongodb["users"].insert_one(user)
    created_user = await request.app.mongodb["users"].find_one({'_id': new_user.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user["_id"])


@router.get('/me', status_code=status.HTTP_200_OK, response_description="Get user by id", response_model=UserMeModel)
async def get_user(request: Request, current_user = Depends(oauth2.get_current_user)):
    '''Get current user'''
    # print(current_user)
    user = await request.app.mongodb["users"].find_one({'email': current_user.email})
    if not user:
        raise HTTPException(
            status_code=404, detail=f"{current_user.email} not found")
    # print(user)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"_id": user["_id"], "name": user["name"], "email": user["email"]})


@router.delete("/{id}", response_description="Delete user")
async def delete_user(id: str, request: Request, current_user=Depends(oauth2.get_current_user)):
    '''Delete user'''
    deleted_result = await request.app.mongodb["user"].delete_one({"_id": id})
    if deleted_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"user {id} not found")
