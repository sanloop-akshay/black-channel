import asyncio
import websockets

ROOM_ID = "room1"
PASSWORD = "mypassword"
URL = f"ws://localhost:8000/ws/{ROOM_ID}?password={PASSWORD}"

async def send_messages(ws):
    while True:
        msg = await asyncio.get_event_loop().run_in_executor(None, input, "")
        await ws.send(msg)

async def receive_messages(ws):
    while True:
        try:
            msg = await ws.recv()
            print(msg)
        except websockets.ConnectionClosed:
            print("Connection closed")
            break

async def main():
    async with websockets.connect(URL) as ws:
        response = await ws.recv()
        print(response)

        if "Connection rejected" in response:
            return

        # Run send and receive concurrently
        await asyncio.gather(
            send_messages(ws),
            receive_messages(ws)
        )

asyncio.run(main())
