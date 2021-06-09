
import asyncio
from rctogether import RestApiSession, bots, notes
from rctogether import WebsocketSubscription

async def main():
    async with RestApiSession() as session:

        writer = await bots.create(
                session,
                name="Bill",
                emoji="✍️",
                x=156,
                y=0)

        note = await notes.create(
            session,
            writer['id'],
            x=155,
            y=0,
            note_text="To be, or not to be...")

        await notes.update(
            session,
            writer['id'],
            note['id'],
            note_text="...that is the question.")

asyncio.run(main())
