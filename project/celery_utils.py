from celery import current_app as current_celery_app
from celery.schedules import crontab

from project.config import settings


def create_celery():
    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY")

    celery_app.conf.task_routes = {
        "project.celery_tasks.tasks.buildIndicatorsFromCandles": "front",
        "project.celery_tasks.tasks.*": "celery"
    }

    celery_app.conf.beat_schedule = {
        "StartTicker24h": {
            "task": "project.celery_tasks.tasks.Start24hTicker",
            "schedule": crontab(minute="*/5"),
            "args": (),
        },
        "UpdateBinanceMarkets": {
            "task": "project.celery_tasks.tasks.UpdateMarkets",
            "schedule": crontab(minute="*/15"),
            "args": (),
        },
        "CreateAllTickers": {
            "task": "project.celery_tasks.tasks.createAllTickers",
            "schedule": crontab(minute="*"),
            "args": (),
        },
        "UpdateBarometer": {
            "task": "project.celery_tasks.tasks.UpdateBarometer",
            "schedule": crontab(minute="*"),
            "args": (),
        },
        "CleanOldTickers": {
            "task": "project.celery_tasks.tasks.clean_old_tickers",
            "schedule": crontab(minute="*/2"),
            "args": (),
        },
        "BuildIndicatorsFromCandles": {
            "task": "project.celery_tasks.tasks.buildIndicatorsFromCandles",
            "schedule": crontab(minute="*"),
            "args": (),
        }
    }

    return celery_app
