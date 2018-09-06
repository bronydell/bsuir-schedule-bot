from vk_api.bot_longpoll import VkBotEventType
from core.logic import on_message


def reply_message_vk(client, peer_id):
    def send_text(text):
        client.messages.send(peer_id=peer_id, message=text)

    return send_text


def on_vk_event(client, event):
    if event.type in [VkBotEventType.MESSAGE_EDIT, VkBotEventType.MESSAGE_NEW]:
        on_message(reply_message_vk(client, event.object.peer_id), event.object.text)
