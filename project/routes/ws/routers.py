'''
websocket
'''
from fastapi import APIRouter, WebSocket

router = APIRouter(
    prefix='/ws',
    tags=['WebSocket']
)
@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    '''websocket'''
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
