import asyncio

from .api import parse_response, api_url

async def send_message(session, bot_id, message_text):
    async with session.post(
        url=api_url("messages"), json={"bot_id": bot_id, "text": message_text}
    ) as response:
        return await parse_response(response)
