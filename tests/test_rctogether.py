import pytest
from rctogether import __version__, bots, messages, walls, notes

from .fixtures import server, session


def test_version():
    assert __version__ == "0.2.2"


@pytest.mark.asyncio
async def test_get_bots(server, session):
    request_context = server.create_request(bots.get(session))
    async with request_context as request:
        assert request.method == "GET"
        assert request.path == "/api/bots"

        request_context.send_json([{"emoji": "🐙", "name": "octopus"}])
    assert request_context.response == [{"emoji": "🐙", "name": "octopus"}]


@pytest.mark.asyncio
async def test_create_bot(server, session):
    async with server.create_request(
        bots.create(session, name="Octopus", emoji="🐙", x=4, y=5)
    ) as request:
        assert request.method == "POST"
        assert request.path == "/api/bots"

        data = await request.json()
        assert data == {
            "bot": {
                "name": "Octopus",
                "emoji": "🐙",
                "x": 4,
                "y": 5,
                "direction": "right",
                "can_be_mentioned": False,
            }
        }


@pytest.mark.asyncio
async def test_update_bot(server, session):
    async with server.create_request(
        bots.update(session, 5, {"x": 1, "y": 2})
    ) as request:
        assert request.method == "PATCH"
        assert request.path == "/api/bots/5"

        data = await request.json()
        assert data == {"bot": {"x": 1, "y": 2}}


@pytest.mark.asyncio
async def test_delete_bot(server, session):
    request_context = server.create_request(bots.delete(session, 17))
    async with request_context as request:
        assert request.method == "DELETE"
        assert request.path == "/api/bots/17"


@pytest.mark.asyncio
async def test_create_wall(server, session):
    async with server.create_request(
        walls.create(session, 18, x=1, y=2, color="blue", wall_text="!")
    ) as request:
        assert request.method == "POST"
        assert request.path == "/api/walls"

        data = await request.json()
        assert data == {"bot_id": 18, "x": 1, "y": 2, "color": "blue", "wall_text": "!"}


@pytest.mark.asyncio
async def test_update_wall(server, session):
    async with server.create_request(
        walls.update(session, 18, 12, wall_text="?")
    ) as request:
        assert request.method == "PATCH"
        assert request.path == "/api/walls/12"

        data = await request.json()
        assert data == {"bot_id": 18, "wall_text": "?", "color": None}


@pytest.mark.asyncio
async def test_delete_wall(server, session):
    async with server.create_request(
        walls.delete(session, bot_id=18, wall_id=12)
    ) as request:
        assert request.method == "DELETE"
        assert request.path == "/api/walls/12"

        data = await request.json()
        assert data == {
            "bot_id": 18,
        }


@pytest.mark.asyncio
async def test_create_note(server, session):
    async with server.create_request(
        notes.create(session, bot_id=18, x=2, y=3, note_text="Hello, world")
    ) as request:
        assert request.method == "POST"
        assert request.path == "/api/notes"

        data = await request.json()
        assert data == {"bot_id": 18, "x": 2, "y": 3, "note_text": "Hello, world"}


@pytest.mark.asyncio
async def test_update_note(server, session):
    async with server.create_request(
        notes.update(session, bot_id=18, note_id=4, note_text="Updated")
    ) as request:
        assert request.method == "PATCH"
        assert request.path == "/api/notes/4"

        data = await request.json()
        assert data == {"bot_id": 18, "note_text": "Updated"}


@pytest.mark.asyncio
async def test_delete_note(server, session):
    async with server.create_request(
        notes.delete(session, bot_id=18, note_id=7)
    ) as request:
        assert request.method == "DELETE"
        assert request.path == "/api/notes/7"

        data = await request.json()
        assert data == {
            "bot_id": 18,
        }


@pytest.mark.asyncio
async def test_send_message(server, session):
    async with server.create_request(
        messages.send(session, 17, "Hello, world")
    ) as request:
        assert request.method == "POST"
        assert request.path == "/api/messages"

        data = await request.json()
        assert data == {"bot_id": 17, "text": "Hello, world"}
