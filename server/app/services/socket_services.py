from fastapi import WebSocket
from typing import Dict

#Test Phase
pending_users: Dict[str, WebSocket] = {}

active_rooms: Dict[str, list] = {}

async def register_user(code: str, websocket: WebSocket):

    if code in pending_users:
        other_ws = pending_users.pop(code)
        room_id = code 
        active_rooms[room_id] = [other_ws, websocket]
        return room_id, other_ws
    else:
        pending_users[code] = websocket
        return None, None

async def remove_user_from_room(room_id: str, websocket: WebSocket):
    if room_id in active_rooms:
        active_rooms[room_id] = [ws for ws in active_rooms[room_id] if ws != websocket]
        if not active_rooms[room_id]:
            del active_rooms[room_id]

async def broadcast_message(room_id: str, sender: WebSocket, message: str):
    if room_id in active_rooms:
        for ws in active_rooms[room_id]:
            if ws != sender:
                await ws.send_text(message)
