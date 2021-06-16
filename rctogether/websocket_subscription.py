import os
import traceback
import json
import asyncio
import aiohttp
import websockets


class WebsocketSubscription:
    async def __aiter__(self):
        rc_app_id = os.environ["RC_APP_ID"]
        rc_app_secret = os.environ["RC_APP_SECRET"]
        rc_endpoint = os.environ.get("RC_ENDPOINT", "https://recurse.rctogether.com")

        origin = f"https://{rc_endpoint}"
        url = f"wss://{rc_endpoint}/cable?app_id={rc_app_id}&app_secret={rc_app_secret}"

        async with websockets.connect(url, ssl=True, origin=origin) as connection:
            subscription_identifier = json.dumps({"channel": "ApiChannel"})
            async for msg in connection:
                data = json.loads(msg)

                message_type = data.get("type")

                if message_type == "ping":
                    pass
                elif message_type == "welcome":
                    await connection.send(
                        json.dumps(
                            {
                                "command": "subscribe",
                                "identifier": subscription_identifier,
                            }
                        )
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
