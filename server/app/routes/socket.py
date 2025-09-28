from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from uuid import uuid4
import json
from app.services.socket_services import (
    check_room, add_client_to_room, remove_client_from_room,
    get_active_clients, add_active_client, remove_active_client,
    MAX_CLIENTS, websocket_connections, create_room
)

router = APIRouter()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, password: str = Query(...)):
    await websocket.accept()
    client_id = str(uuid4())

    valid, room_or_msg = check_room(room_id, password)
    if not valid:
        if room_or_msg == "Room does not exist":
            created, msg = create_room(room_id, password)
            if not created:
                await websocket.send_text(f"Connection rejected: {msg}")
                await websocket.close()
                return
        else:
            await websocket.send_text(f"Connection rejected: {room_or_msg}")
            await websocket.close()
            return

    valid, room = check_room(room_id, password)
    if not valid:
        await websocket.send_text(f"Connection rejected: {room}")
        await websocket.close()
        return

    active_clients = get_active_clients(room_id)
    if len(active_clients) >= MAX_CLIENTS:
        await websocket.send_text("Room full")
        await websocket.close()
        return

    _, room = add_client_to_room(room_id, client_id)
    add_active_client(room_id, client_id)

    if room_id not in websocket_connections:
        websocket_connections[room_id] = {}
    websocket_connections[room_id][client_id] = websocket

    await websocket.send_text(f"Connected to room {room_id} as {client_id}")

    try:
        while True:
            data = await websocket.receive_text()
            for other_id, ws in websocket_connections.get(room_id, {}).items():
                if other_id != client_id:
                    await ws.send_text(f"{client_id}: {data}")

    except WebSocketDisconnect:
        remove_client_from_room(room_id, client_id)
        remove_active_client(room_id, client_id)
        del websocket_connections[room_id][client_id]
        if not websocket_connections[room_id]:
            del websocket_connections[room_id]
