import asyncio
import websockets

class Client:

    async def connect(self):
        async with websockets.connect(uri = "wss://esportsproject-sandbox.mxapps.io/localwebsocket") as self.ws:
            try:
                print(self.ws.open)
                loop = asyncio.get_event_loop()
                await self.ws.send("Connected")
            except websockets.ConnectionClosed:
                print("Connection closed")
        print(self.ws.open)
            # await self.ws.recv()

    async def sendMessage(self, message):
        async with websockets.connect("wss://esportsproject-sandbox.mxapps.io/localwebsocket") as self.ws:
            await self.ws.send(message)
