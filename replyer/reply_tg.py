from .base_reply import BaseReply
from telegram.update import Update as TgUpdate
from telegram.ext.callbackcontext import CallbackContext


class TGReply(BaseReply):
    chat_type = "Telegram"

    def __init__(self, update: TgUpdate, context: CallbackContext):
        self.update = update
        self.context = context

    def send_text(self, text):
        self.update.effective_message.reply_text(text)

    def get_chat_id(self):
        return self.update.effective_chat.id

    def get_message_author(self):
        return  self.update.effective_user.id

    def get_message_author_name(self):
        return self.update.effective_user.full_name