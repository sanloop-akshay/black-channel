from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services import socket_services

#Test Phase without Security
router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    room_id = None

    try:
        data = await websocket.receive_json()
        code = data.get("code")
        if not code:
            await websocket.close()
            return

        room_id, other_ws = await socket_services.register_user(code, websocket)

        if room_id:
            await websocket.send_json({"status": "connected"})
            await other_ws.send_json({"status": "connected"})

        while True:
            message_data = await websocket.receive_text()
            if room_id:
                await socket_services.broadcast_message(room_id, websocket, message_data)

    except WebSocketDisconnect:
        if room_id:
            await socket_services.remove_user_from_room(room_id, websocket)
