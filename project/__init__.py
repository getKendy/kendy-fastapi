from fastapi import FastAPI
# from project.celery_utils import create_celery
from fastapi_pagination import add_pagination
from motor.motor_asyncio import AsyncIOMotorClient
from os import environ
from project.routes import task
from project.routes.v2.barometer import routers as baro_router
from project.routes.v2.ticker import routers as ticker_router
from project.routes.v2.users import routers as user_router
from project.routes.v2.settings import routers as settings_router
from project.routes.v2.balance import routers as balance_router
from project.routes.v2.alert import routers as alert_router
from project.auth import authentication as auth_router
# from project.routes.ws import routers as webSocket_router

def create_app() -> FastAPI:
    app = FastAPI()

    # Celery before routes!
    # app.celery_app = create_celery()
    
    
    # Routers

    app.include_router(user_router.router)
    app.include_router(auth_router.router)
    app.include_router(settings_router.router)
    app.include_router(task.router)
    app.include_router(ticker_router.router)
    app.include_router(baro_router.router)
    # app.include_router(balance_router.router)fastapifast
    app.include_router(alert_router.router)
    # app.include_router(webSocket_router.router)
    add_pagination(app)

    @app.on_event("startup")
    async def startup_db_client():
        app.mongodb_client = AsyncIOMotorClient(environ.get('MONGO_CLIENT', 'mongodb://user:password@server:port/db')
                                                )
        app.mongodb = app.mongodb_client[environ.get('MONGO_DB', '')]
    # app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    # app.mongodb = app.mongodb_client[settings.DB_NAME]

    @app.on_event("shutdown")
    async def shutdown_db_client():
        app.mongodb_client.close()

    return app
