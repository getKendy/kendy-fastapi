from celery.result import AsyncResult
from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse

from ..celery_tasks import tasks

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
)


@router.post("/", status_code=201)
def run_task(payload=Body(...)):
    task_type = payload["type"]
    task = tasks.create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@router.get("/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
