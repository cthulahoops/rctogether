import asyncio
from rctogether import RestApiSession, bots, walls


async def main():
    async with RestApiSession() as session:

        builder = await bots.create(session, name="Bob", emoji="👷", x=160, y=1)

        wall = await walls.create(session, builder["id"], x=160, y=0)
        print(wall)
        await asyncio.sleep(5)
#        await walls.update(session, builder["id"], wall["id"], wall_text="!")
        await walls.delete(session, builder["id"], wall["id"])


asyncio.run(main())
