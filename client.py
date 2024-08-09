import asyncio


class WeatherClientProtocol(asyncio.Protocol):
    def __init__(self, on_con_lost):
        self.buffer = b''
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        print('Connected to server')
        self.transport = transport

    def data_received(self, data):
        self.buffer += data
        if b'\n' in self.buffer:
            message = self.buffer.decode()
            print(message.strip())
            self.buffer = b''

    def connection_lost(self, exc):
        print('Connection lost')
        self.on_con_lost.set_result(True)


async def main():
    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()
    transport, protocol = await loop.create_connection(
        lambda: WeatherClientProtocol(on_con_lost), '127.0.0.1', 8888)

    try:
        await on_con_lost
    except RuntimeError as e:
        print(f'RuntimeError: {e}')
    finally:
        transport.close()


asyncio.run(main())
