def create(session, bot_id, x=None, y=None, color="gray", wall_text=None):
    wall = {"color": color}
    if x is not None:
        wall['x'] = x
    if y is not None:
        wall['y'] = y
    if wall_text is not None:
        wall['wall_text'] = wall_text

    return session.post(
        "walls",
        {
            "bot_id": bot_id,
            "wall": wall,
        },
    )


def update(session, bot_id, wall_id, color=None, wall_text=None):
    return session.patch(
        "walls", wall_id, {"bot_id": bot_id, "color": color, "wall_text": wall_text}
    )


def delete(session, bot_id, wall_id):
    return session.delete("walls", wall_id, {"bot_id": bot_id})
