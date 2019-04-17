from .base_reply import BaseReply


class VKReply(BaseReply):
    chat_type = "VK"

    def __init__(self, client, event):
        self.client = client
        self.event = event
        self.peer_id = event.object.peer_id

    def send_text(self, text):
        self.client.messages.send(peer_id=self.peer_id, message=text)

    def get_chat_id(self):
        return self.peer_id

    def get_message_author(self):
        return self.event.object.from_id

    def get_message_author_name(self):
        response = self.client.users.get(user_ids=self.event.object.from_id)
        return "{first_name} {last_name}".format(
            first_name=response[0]['first_name'],
            last_name=response[0]['last_name'],
        )