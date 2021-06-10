
import asyncio
from rctogether import RestApiSession, bots, messages

async def main():
    async with RestApiSession() as session:
        talker = await bots.create(session, name="Casper", emoji="👻", x=1, y=1)
        await messages.send(session, talker['id'], "Boo!")

asyncio.run(main())
