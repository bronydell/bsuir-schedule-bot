from vk_api import VkApi, AuthError
from vk_api.bot_longpoll import VkBotLongPoll
from model.database import generate_database
from message_handler import on_vk_event
from requests.exceptions import ConnectionError
from saver import save_global_pref
import json
import time


def read_json_file(filename):
    """ Read file's content and convert json to dictionary """
    with open(file=filename, encoding="UTF-8") as file:
        return json.load(file)


def read_token(settings):
    """ Read token from settings """
    return settings['access_token']


def read_club_id(settings):
    """ Read token from settings """
    return settings['club_id']


def get_session(token):
    """ Get session with token """
    session = VkApi(token=token, api_version="5.84")
    return session


def get_client(session):
    """ Get client from session """
    client = session.get_api()
    return client


def start_polling(client, vk_poll):
    print('Started polling')
    for event in vk_poll.listen():
        try:
            on_vk_event(client, event)
        except Exception as ex:
            print('Error: ', ex)
            pass


def main():
    try:
        settings = read_json_file("settings.json")
        access_token = read_token(settings)
        vk_session = get_session(access_token)
        vk_client = get_client(vk_session)
        club_id = read_club_id(settings)
        generate_database()
        start_time = time.time()
        save_global_pref('start_time', start_time)
        while 1:
            try:
                vk_long_poll = VkBotLongPoll(vk_session, club_id, wait=900)

                start_polling(vk_client, vk_long_poll)
            except ConnectionError:
                pass
    except AuthError as error_msg:
        print("Error while authorizing: {}".format(error_msg))
        exit(-1)


if __name__ == "__main__":
    main()
