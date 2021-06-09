
import os
import traceback
import json
import asyncio
import aiohttp
import websockets

from .api import RC_APP_ID, RC_APP_SECRET, RC_APP_ENDPOINT

RC_APP_ID = os.environ["RC_APP_ID"]
RC_APP_SECRET = os.environ["RC_APP_SECRET"]
RC_APP_ENDPOINT = os.environ.get("RC_ENDPOINT", "recurse.rctogether.com")

class WebsocketSubscription:
    async def __aiter__(self):
        origin = f"https://{RC_APP_ENDPOINT}"
        url = f"wss://{RC_APP_ENDPOINT}/cable?app_id={RC_APP_ID}&app_secret={RC_APP_SECRET}"

        async with websockets.connect(url, ssl=True, origin=origin) as connection:
            subscription_identifier = json.dumps({"channel": "ApiChannel"})
            async for msg in connection:
                data = json.loads(msg)

                message_type = data.get("type")

                if message_type == "ping":
                    pass
                elif message_type == "welcome":
                    await connection.send(
                        json.dumps({"command": "subscribe", "identifier": subscription_identifier})
                    )
                elif message_type == "confirm_subscription":
                    print("Subscription confirmed.")
                elif message_type == "reject_subscription":
                    raise ValueError("RcTogether: Subscription rejected.")
                elif (
                    "identifier" in data
                    and data["identifier"] == subscription_identifier
                    and "message" in data
                ):
                    message = data["message"]

                    if message["type"] == "world":
                        for entity in message["payload"]["entities"]:
                            yield entity
                    else:
                        yield message["payload"]
                else:
                    print("Unknown message type: ", message_type)

    async def handle_entity(self, entity):
        for callback in self.callbacks:
            await callback(entity)

        if entity["id"] in self.bots:
            callback = self.bots[entity["id"]].handle_entity
            if callback:
                await callback(entity)

    def add_callback(self, callback):
        self.callbacks.append(callback)
