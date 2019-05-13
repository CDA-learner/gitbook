from routeClient import RouteClient
import asyncio
class ClientMgr:
    def __init__(self):
        self.clients = []

    def add(self, client):
        self.clients.append(client)

    def init(self , configs):
        for config in configs:
            self.add(RouteClient(config).start())

    def update(self):
        for client in self.clients:
            client.update()
