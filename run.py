from tools import read_json_file
from model.database import generate_database

from runner import VkRunner, TgRunner


def main():
    config = read_json_file("settings.json")
    generate_database()

    # vk_runner = VkRunner(config)
    # vk_runner.start()

    tg_runner = TgRunner(config)
    tg_runner.start()
    pass


if __name__ == '__main__':
    main()
