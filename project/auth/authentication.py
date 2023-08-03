from fastapi import APIRouter, Depends, status, HTTPException, Request, Body

from . import JWTtoken
# from ..repository import users
# from .. import schemas
# from typing import List, Optional
from .hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm
from project.auth.models import LoginModel
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/api/v2/login",
    tags=['Authenication']

)


# @router.post('/')
# def login_test(request: schemas.Login, db: Session = Depends(database.get_db)):
#     print('login_test')
#     user = db.query(models.User).filter(
#         models.User.email == request.username).first()
#     if not user:
#         # print(user.password)
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail='invalid credentials')
#     if not Hash.verify(user.password, request.password):
#         # print(user.password)
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail='invalid credentials')
#     # jwt
#     # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     # access_token = create_access_token(
#     #     data={"sub": user.username}, expires_delta=access_token_expires
#     # )
#     access_token = JWTtoken.create_access_token(
#         data={"sub": user.email}
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


@router.post('/')
# async def login(request: Request, form_data: LoginModel = Body(...)):
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    '''Login user'''
    # user = jsonable_encoder(user)
    # print(form_data)
    user =  await request.app.mongodb["users"].find_one({'name': form_data.username})

    # user = db.query(models.User).filter(
    #     models.User.email == request.username).first()
    if not user:
        # print(user.username)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='invalid credentials')
    # print(users[0])
    # print(type(users[0]))
    if not Hash.verify(user['password'], form_data.password):
        # print(user['password'])
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='invalid credentials')
    # jwt
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={"sub": user.username}, expires_delta=access_token_expires
    # )
    access_token = JWTtoken.create_access_token(
        data={"sub": user['email']}
    )
    return {"access_token": access_token, "token_type": "bearer"}
