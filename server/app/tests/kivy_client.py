import asyncio
import websockets

def create_client(room_id: str, password: str, host: str = "localhost", port: int = 8000):
    return f"ws://{host}:{port}/ws/{room_id}?password={password}"

async def send_messages(ws):
    loop = asyncio.get_event_loop()
    while True:
        msg = await loop.run_in_executor(None, input, "")
        await ws.send(msg)

async def receive_messages(ws):
    while True:
        try:
            msg = await ws.recv()
            print(msg)
        except websockets.ConnectionClosed:
            print("Connection closed")
            break

async def connect_client(room_id: str, password: str):
    url = create_client(room_id, password)
    try:
        async with websockets.connect(url) as ws:
            response = await ws.recv()
            print(response)

            if "Connection rejected" in response:
                return

            await asyncio.gather(
                send_messages(ws),
                receive_messages(ws)
            )
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    ROOM_ID = input("Enter room name: ")
    PASSWORD = input("Enter password: ")
    asyncio.run(connect_client(ROOM_ID, PASSWORD))
