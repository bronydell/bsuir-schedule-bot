from vk_api.bot_longpoll import VkBotEventType
from core.logic import on_message


class VKReply:
    def __init__(self, client, event):
        self.client = client
        self.event = event
        self.peer_id = event.object.peer_id

    def send_text(self, text):
        self.client.messages.send(peer_id=self.peer_id, message=text)

    def get_chat_id(self):
        return self.peer_id

    def get_event(self):
        return self.event

    def get_message_author(self):
        return self.event.object.from_id

    def get_message_author_name(self):
        response = self.client.users.get(user_ids=self.event.object.from_id)
        return "{first_name} {last_name}".format(
            first_name=response[0]['first_name'],
            last_name=response[0]['last_name'],
        )


def on_vk_event(client, event):
    if event.type in [VkBotEventType.MESSAGE_EDIT, VkBotEventType.MESSAGE_NEW]:
        on_message(VKReply(client, event), event.object.text)
