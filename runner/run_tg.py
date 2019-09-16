from runner import BaseRunner
from message_handler import on_tg_event
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.error import InvalidToken
import logging


class TgRunner(BaseRunner):
    def __init__(self, settings):
        super().__init__(settings['tg'])
        try:
            self.token = self.settings['token']
            self.updater = Updater(token=self.token, use_context=True)
            logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                level=logging.INFO)
        except InvalidToken:
            print('Telegram bot token is invalid!')

    # Telegram library is already async
    def _execute(self):
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(MessageHandler(Filters.text, on_tg_event))
        self.updater.start_polling()
