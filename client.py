import asyncio


class WeatherClientProtocol(asyncio.Protocol):
    def __init__(self):
        self.buffer = b''

    def connection_made(self, transport):
        print('Connected to server')

    def data_received(self, data):
        self.buffer += data
        if b'\n' in self.buffer:
            message = self.buffer.decode()
            print(message.strip())
            self.buffer = b''

    def connection_lost(self, exc):
        print('Connection lost')


async def main():
    loop = asyncio.get_running_loop()
    await loop.create_connection(lambda: WeatherClientProtocol(), '127.0.0.1', 8888)

    while True:
        await asyncio.sleep(1)


asyncio.run(main())
