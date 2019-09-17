from json import load
from abc import ABC

class BaseLocaleManager(ABC):
    def __init__(self, key):
        with open(file=key+'.json', encoding="UTF-8") as file:
            self.locale = load(file)

    def get_prefix(self):
        return self.locale['prefix']

    def get_commands(self):
        return self.locale['commands']

    def message_building_not_found(self):
        return self.locale['building_not_found']

    def localize_building(self, number : int):
        return self.locale['building_template'].format(number=number, name=self.locale['buildings'][number]['name'], google=self.locale['buildings'][number]['google'])

    def __getitem__(self, key):
        return self.locale[key]