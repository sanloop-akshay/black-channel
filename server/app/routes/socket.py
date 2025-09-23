from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from uuid import uuid4
from app.services.socket_services import check_room, add_client_to_room, remove_client_from_room

router = APIRouter()
active_connections = {}

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, password: str = Query(...)):
    await websocket.accept()
    client_id = str(uuid4())

    valid, room_or_msg = check_room(room_id, password)
    if not valid:
        await websocket.send_text(f"Connection rejected: {room_or_msg}")
        await websocket.close()
        return

    _, room = add_client_to_room(room_id, client_id)

    if room_id not in active_connections:
        active_connections[room_id] = {}
    active_connections[room_id][client_id] = websocket

    await websocket.send_text(f"Connected to room {room_id} as {client_id}")

    try:
        while True:
            data = await websocket.receive_text()
            for other_id, ws in active_connections[room_id].items():
                if other_id != client_id:
                    await ws.send_text(f"{client_id}: {data}")
    except WebSocketDisconnect:
        remove_client_from_room(room_id, client_id)
        del active_connections[room_id][client_id]
        if not active_connections[room_id]:
            del active_connections[room_id]
