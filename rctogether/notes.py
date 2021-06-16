def create(session, bot_id, x=None, y=None, note_text=""):
    return session.post(
        "notes", {"bot_id": bot_id, "x": x, "y": y, "note_text": note_text}
    )


def update(session, bot_id, note_id, note_text=""):
    return session.patch("notes", note_id, {"bot_id": bot_id, "note_text": note_text})


def delete(session, bot_id, note_id):
    return session.delete("notes", note_id, {"bot_id": bot_id})
