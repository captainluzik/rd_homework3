import asyncio
import random


class WeatherServerProtocol(asyncio.Protocol):
    clients = []

    def __init__(self):
        super().__init__()
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        WeatherServerProtocol.clients.append(self)
        print('New client connected. Total clients:', len(WeatherServerProtocol.clients))

    def connection_lost(self, exc):
        WeatherServerProtocol.clients.remove(self)
        print('Client disconnected. Total clients:', len(WeatherServerProtocol.clients))

    def data_received(self, data):
        pass


async def generate_weather_data():
    while True:
        temperature = random.uniform(-30, 40)
        humidity = random.uniform(0, 100)
        weather_data = f'Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%\n'
        for client in WeatherServerProtocol.clients:
            client.transport.write(weather_data.encode())
        await asyncio.sleep(1)


async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda: WeatherServerProtocol(), '0.0.0.0', 8888)
    print('Weather server running on 0.0.0.0:8888')

    asyncio.create_task(generate_weather_data())

    async with server:
        await server.serve_forever()


asyncio.run(main())
