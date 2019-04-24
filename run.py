from tools import read_json_file
import time
from saver import save_global_pref
from model.database_manager import generate_database

from runner import VkRunner, TgRunner


def main():
    config = read_json_file("settings.json")
    generate_database()

    start_time = time.time()
    save_global_pref('start_time', start_time)

    vk_runner = VkRunner(config)
    vk_runner.start()

    tg_runner = TgRunner(config)
    tg_runner.start()
    pass


if __name__ == '__main__':
    main()
