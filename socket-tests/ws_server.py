import asyncio
import websockets
import json

ADDRESS = '127.0.0.1'
PORT = 5001

class wsMessage:
    def __init__(self, type, data):
        self.type = type
        self.data = data

async def server(websocket, path):
    print('[+] Received connection...')
    await websocket.send('Connection established!')
    
    async for message in websocket:
        data = json.loads(message)
        print('message received from client: ' + str(data))

        response = wsMessage('info', 'Received ' + data['type'] + ' message!')
        await websocket.send(json.dumps(response.__dict__))

print('[+] Listening...')
start_server = websockets.serve(server, ADDRESS, PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()        