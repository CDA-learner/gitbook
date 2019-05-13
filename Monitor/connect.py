
from threading import Thread
import websockets
import asyncio
import logging
import queue

class Connect:
    def __init__(self, conn):
        self.conn = conn
        self.q = queue.SimpleQueue()

    async def consumer_handler(self):
        try:
            async for message in self.conn:
                self.consumer(message)
        finally:
            print('consumer_handler end')

    def consumer(self, message):
        self.onMessage(message)

    def send(self, message):
        self.q.put(message, False)

    def onMessage(self, data):
        self.onMsg(data)

    def onMsg(self, data):
        print(data)

    async def producer(self):
        while True:
            if self.q.empty():
                await asyncio.sleep(0.4)
            else:
                return self.q.get(False)

    async def producer_handler(self):
        try:
            while True:
                message = await self.producer()
                if message:
                    await self.conn.send(message)
        finally:
            print('producer_handler end')

    async def start(self):
        consumer_task = asyncio.create_task(self.consumer_handler())
        producer_task = asyncio.create_task(self.producer_handler())
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,)

        for task in pending:
            task.cancel()

    def getTextInfo(self):
        pass