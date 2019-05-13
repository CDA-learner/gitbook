#!/user/bin/env python
#
import asyncio
import json
import logging
import websockets
import threading
import mysql
from server import Server
from databaseConnect import GateConnect
from databaseConnect import RouteConnect

def run():
    Server().run(GateConnect, 9998)
    Server().run(RouteConnect, 9999)
    loop = asyncio.new_event_loop()
    loop.run_forever()

if __name__ == "__main__":
    run()


