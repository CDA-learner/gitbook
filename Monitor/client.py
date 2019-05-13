import websockets
import asyncio
import logging
from threading import Thread
import helper
from connect import Connect

class ClientConnect(Connect):
    def __init__(self, client, conn):
        super().__init__(conn)
        self.client =client
        self.clientThread = None
    def onMessage(self, data):
        self.client.onMessage(data)

    def onMsg(self, data):
        self.client.onMsg(data)

    def onDisconnect(self):
        self.client.onDisconnect()

class Client:
    def __init__(self, config):
        self.url = config['url']
        self.status = 0

    def connect(self):
        loop = asyncio.new_event_loop()
        self.loop = loop
        loop.run_until_complete(loop.create_task(self._connect()))
        self.conn = ClientConnect(self, self.ws)
    
    def run(self):
        self.loop.run_until_complete(self.loop.create_task(self.conn.start()))

    def onConnect(self):
        pass

    def start(self):
        try:
            self.connect()
            self.onConnect()
            self.clientThread = Thread(target=self.run, name="connect run")
            self.clientThread.start()
            self.status = 1
        except  Exception as e:
            logging.error(e)
        finally:
            self.status = 2
            return self

    async def _connect(self):
        self.ws = await websockets.connect(self.url)

    def onMessage(self, data):
        self.onMsg(data)

    def onMsg(self, data):
        logging.info(data)

    def update(self):
        pass

    def onDisconnect(self):
        pass

    def send(self, data):
        self.conn.send(data)

if __name__ == "__main__":
    c = Client({'url' : 'ws://localhost:8020/ro'})
    c.start()
    asyncio.get_event_loop().run_forever()