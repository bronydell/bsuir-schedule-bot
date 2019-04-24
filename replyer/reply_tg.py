from .base_reply import BaseReply
from telegram.update import Update as TgUpdate
from telegram.bot import Bot as TgClient


class TGReply(BaseReply):
    chat_type = "Telegram"

    def __init__(self, client: TgClient, event: TgUpdate):
        self.client = client
        self.event = event
        self.chat_id = event.effective_chat.id

    def send_text(self, text):
        self.event.effective_message.reply_text(text)

    def get_chat_id(self):
        return self.chat_id

    def get_message_author(self):
        return self.event.effective_user.id

    def get_message_author_name(self):
        return self.event.effective_user.full_name