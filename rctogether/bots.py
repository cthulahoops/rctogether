import asyncio


def get(session):
    return session.get("bots")


def delete(session, bot_id):
    return session.delete("bots", bot_id)


def create(session, name, x, y, emoji="🤖", direction="right", can_be_mentioned=False):
    return session.post(
        "bots",
        json={
            "bot": {
                "name": name,
                "emoji": emoji,
                "x": x,
                "y": y,
                "direction": direction,
                "can_be_mentioned": can_be_mentioned,
            }
        },
    )


def update(session, bot_id, bot_attributes):
    return session.patch("bots", bot_id, json={"bot": bot_attributes})


async def delete_all(session):
    bots = await get(session)
    await asyncio.gather(*[delete(session, bot["id"]) for bot in bots])
