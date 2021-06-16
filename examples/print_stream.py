import asyncio
from rctogether import WebsocketSubscription


async def main():
    async for message in WebsocketSubscription():
        print(message)


asyncio.run(main())
