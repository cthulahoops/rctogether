import asyncio
from rctogether import bots, RestApiSession


async def main():
    async with RestApiSession() as session:
        print(await bots.get(session))


asyncio.run(main())
