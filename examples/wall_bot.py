import asyncio
from rctogether import RestApiSession, bots, walls


async def main():
    async with RestApiSession() as session:

        builder = await bots.create(session, name="Bob", emoji="👷", x=160, y=1)

        wall = await walls.create(session, builder["id"], 160, 0, color="gray")
        print(wall)
        await walls.update(session, builder["id"], wall["id"], wall_text="!")
        await walls.delete(session, builder["id"], wall["id"])


asyncio.run(main())
