def create(session, bot_id, x=None, y=None, color="gray", wall_text=None):
    return session.post(
        "walls",
        {"bot_id": bot_id, "x": x, "y": y, "color": color, "wall_text": wall_text},
    )


def update(session, bot_id, wall_id, color=None, wall_text=None):
    return session.patch(
        "walls", wall_id, {"bot_id": bot_id, "color": color, "wall_text": wall_text}
    )


def delete(session, bot_id, wall_id):
    return session.delete("walls", wall_id, {"bot_id": bot_id})
