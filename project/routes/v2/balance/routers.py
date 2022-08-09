'''
baro routers
'''
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, paginate
import pandas as pd
from project.auth import oauth2
from .models import BalanceModel
from project.celery_tasks import tasks
router = APIRouter(
    prefix="/api/v2/balance",
    tags=["Balance"]
)


@router.post("/", response_description="Get all balances")
async def list_balance(form_data: BalanceModel = Body(...),  current_user=Depends(oauth2.get_current_user)):
    '''get balances'''
    # print(current_user)
    api = jsonable_encoder(form_data)
    # print(api)
    task = tasks.get_balance.delay(api['apikey'], api['apisecret'])
    return JSONResponse({"task_id": task.id})
