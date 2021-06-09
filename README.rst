RC Together
===========

An asyncio based client library for `RC Together <https://www.rctogether.com>`_. The API
docs are at: https://docs.rctogether.com

Authentication
--------------

You'll need to generate an app key and secret according to the instructions in the API
docs: https://docs.rctogether.com/#authentication

Provide these credentials as environment variables::

        export RC_APP_ID=<your_app_id>
        export RC_APP_SECRET=<your_app_secret>
        export RC_APP_ENDPOINT=<domain>

If not provided the endpoint defaults to `recurse.rctogether.com`.

Connecting to the Websocket
---------------------------

This example connects to the websocket and prints all messages received::

        import asyncio
        from rctogether import WebsocketSubscription

        async def main():
            async for message in WebsocketSubscription():
                print(message)

        asyncio.run(main())


Using the REST API
------------------

You can use the REST API to list all your bots like this::

        import asyncio
        from rctogether import bots, RestApiSession

        async def main():
            async with RestApiSession() as session:
                print(await bots.get(session))

        asyncio.run(main())
