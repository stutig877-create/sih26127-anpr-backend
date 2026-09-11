import asyncio


class LiveUpdateManager:
    def __init__(self):
        self._clients: set[asyncio.Queue] = set()

    def subscribe(self) -> asyncio.Queue:
        client_queue = asyncio.Queue()
        self._clients.add(client_queue)
        return client_queue

    def unsubscribe(self, client_queue: asyncio.Queue) -> None:
        self._clients.discard(client_queue)

    async def broadcast(self, event: dict) -> None:
        for client_queue in tuple(self._clients):
            await client_queue.put(event)


live_updates = LiveUpdateManager()