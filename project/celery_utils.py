from celery import current_app as current_celery_app
from celery.schedules import crontab

from project.config import settings


def create_celery():
    '''celert task settings'''
    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY")

    celery_app.conf.task_routes = {
        "project.celery_tasks.tasks.clean_old_tickers": "front",
        "project.celery_tasks.tasks.*": "celery"
    }

    celery_app.conf.beat_schedule = {
        "start_24h_ticker": {
            "task": "project.celery_tasks.tasks.start_24h_ticker",
            "schedule": crontab(minute="*/5"),
            "args": (),
        },
        "update_markets": {
            "task": "project.celery_tasks.tasks.update_markets",
            "schedule": crontab(minute="*/15"),
            "args": (),
        },
        # "CreateAllTickers": {
        #     "task": "project.celery_tasks.tasks.createAllTickers",
        #     "schedule": crontab(minute="*"),
        #     "args": (),
        # },
        "update_barometer": {
            "task": "project.celery_tasks.tasks.update_barometer",
            "schedule": crontab(minute="*"),
            "args": (),
        },
        "clean_old_tickers": {
            "task": "project.celery_tasks.tasks.clean_old_tickers",
            "schedule": crontab(minute="*/2"),
            "args": (),
        },
        "build_indicators_from_candles": {
            "task": "project.celery_tasks.tasks.build_indicators_from_candles",
            "schedule": crontab(minute="*"),
            "args": (),
        }
    }

    return celery_app
