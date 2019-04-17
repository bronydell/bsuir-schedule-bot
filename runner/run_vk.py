from runner import BaseRunner
from vk_api import VkApi, AuthError
from vk_api.bot_longpoll import VkBotLongPoll
from message_handler import on_vk_event
from requests.exceptions import ConnectionError


class VkRunner(BaseRunner):
    def __init__(self, settings):
        super().__init__(settings['vk'])
        try:
            self.token = self.settings['access_token']
            self.club_id = self.settings['club_id']
            self.session = VkApi(token=self.token, api_version="5.84")
            self.client = self.session.get_api()
        except AuthError as error_msg:
            print("Error while authorizing VK: {}".format(error_msg))

    def start_polling(self, vk_poll):
        print('Started polling')
        for event in vk_poll.listen():
            try:
                on_vk_event(self.client, event)
            except Exception as ex:
                print('Error: ', ex)
                pass

    def _execute(self):
        while 1:
            try:
                vk_long_poll = VkBotLongPoll(self.session, self.club_id, wait=900)

                self.start_polling(vk_long_poll)
            except ConnectionError:
                pass
