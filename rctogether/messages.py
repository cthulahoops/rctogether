def send(session, bot_id, message_text):
    return session.post("messages", json={"bot_id": bot_id, "text": message_text})
