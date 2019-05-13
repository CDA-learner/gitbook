import logging
import websockets
import asyncio
from connect import Connect
import threading
from threading import Thread 
lock = threading.Lock()
class Server:
    def __init__(self):
        self.connects = {}

    async def connect(self, conn, path):
        try:
            logging.info('server connect...')
            connect = self.getConnCls()(conn , self)
            lock.acquire()
            self.connects[conn] = connect
            lock.release()
            await connect.start()
        finally:
            connect = self.connects[conn]
            lock.acquire()
            self.connects.pop(conn)
            lock.release()
            logging.info("服务器断开")

    def listen(self, port):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(websockets.serve(self.connect, '', port , ping_interval=None))
        loop.run_forever()

    def getConnCls(self):
        return Connect

    def run(self, port):
        def serverRun():
            self.listen(port)
        Thread(target=serverRun, name='ServerThread').start()

    def update(self):
        lock.acquire()
        for connect in self.connects.values():
            connect.update()
        lock.release()

    