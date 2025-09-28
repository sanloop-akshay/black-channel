import json
from app.core.security import redis_client

websocket_connections = {} 

REDIS_ACTIVE_KEY = "active_connections" 
MAX_CLIENTS = 2


def get_active_clients(room_id: str):
    data = redis_client.hget(REDIS_ACTIVE_KEY, room_id)
    return json.loads(data) if data else []

def add_active_client(room_id: str, client_id: str):
    clients = get_active_clients(room_id)
    if client_id not in clients:
        clients.append(client_id)
        redis_client.hset(REDIS_ACTIVE_KEY, room_id, json.dumps(clients))

def remove_active_client(room_id: str, client_id: str):
    clients = get_active_clients(room_id)
    if client_id in clients:
        clients.remove(client_id)
        if clients:
            redis_client.hset(REDIS_ACTIVE_KEY, room_id, json.dumps(clients))
        else:
            redis_client.hdel(REDIS_ACTIVE_KEY, room_id)

# ------------------- Room Handling -------------------

def create_room(room_id: str, password: str):
    if redis_client.exists(f"room:{room_id}"):
        return False, "Room already exists"
    room_data = {"password": password, "clients": []}
    redis_client.set(f"room:{room_id}", json.dumps(room_data))
    return True, "Room created"

def check_room(room_id: str, password: str):
    room_json = redis_client.get(f"room:{room_id}")
    if not room_json:
        return False, "Room does not exist"

    room = json.loads(room_json)

    if room["password"] != password:
        return False, "Invalid password"

    if len(room["clients"]) >= MAX_CLIENTS:
        return False, "Room full"

    return True, room

def add_client_to_room(room_id: str, client_id: str):
    room_json = redis_client.get(f"room:{room_id}")
    if not room_json:
        return False, "Room not found"
    room = json.loads(room_json)
    if client_id not in room["clients"]:
        room["clients"].append(client_id)
        redis_client.set(f"room:{room_id}", json.dumps(room))
    return True, room

def remove_client_from_room(room_id: str, client_id: str):
    room_json = redis_client.get(f"room:{room_id}")
    if not room_json:
        return False, "Room not found"
    room = json.loads(room_json)
    if client_id in room["clients"]:
        room["clients"].remove(client_id)
        redis_client.set(f"room:{room_id}", json.dumps(room))
    return True, room
