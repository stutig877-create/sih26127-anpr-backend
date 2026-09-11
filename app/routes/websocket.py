import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.live_updates import live_updates

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/live")
async def live_detection_updates(websocket: WebSocket):
    await websocket.accept()
    client_queue = live_updates.subscribe()
    receive_task = asyncio.create_task(websocket.receive_text())
    event_task = asyncio.create_task(client_queue.get())

    try:
        while True:
            done, _ = await asyncio.wait(
                {receive_task, event_task},
                return_when=asyncio.FIRST_COMPLETED,
            )

            if receive_task in done:
                receive_task.result()
                receive_task = asyncio.create_task(websocket.receive_text())

            if event_task in done:
                await websocket.send_json(event_task.result())
                event_task = asyncio.create_task(client_queue.get())
    except WebSocketDisconnect:
        pass
    finally:
        for task in (receive_task, event_task):
            if not task.done():
                task.cancel()
        live_updates.unsubscribe(client_queue)