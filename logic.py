import locale_manager
from schedule.api import get_schedule
from schedule.prettify import prettify_schedule
from schedule.tools import get_today_schedule, get_tomorrow_schedule


def has_triggered_command(command_list, message):
    for phrase in command_list:
        if message.lower().startswith(phrase.lower()):
            return phrase


def parse_message(command_list, message):
    for command in command_list.keys():
        triggered_phrase = has_triggered_command(command_list[command], message)
        if triggered_phrase:
            return command, message.split(triggered_phrase)[1]


def perform_command(command, params, reply, locale):
    if command == "get_current_schedule":
        try:
            if len(params) == 0:
                schedule = get_schedule(881061)
            else:
                schedule = get_schedule(params[0])
            reply(get_prettified_schedule(locale, schedule, get_today_schedule))
        except Exception:
            reply(locale['group_not_found'])
    if command == "get_tomorrow_schedule":
        try:
            if len(params) == 0:
                schedule = get_schedule(881061)
            else:
                schedule = get_schedule(params[0])
            reply(get_prettified_schedule(locale, schedule, get_tomorrow_schedule))
        except Exception:
            reply(locale['group_not_found'])


def get_prettified_schedule(locale, schedule, selector):
    lesson_template = locale_manager.read_lesson_template(locale)
    lesson_types = locale_manager.read_lesson_types(locale)
    schedule = selector(schedule)
    return prettify_schedule(schedule, lesson_template, lesson_types)


def on_message(reply, message_text):
    locale = locale_manager.read_locale()
    command, params = parse_message(locale['commands'], message_text)
    if command:
        perform_command(command, list(filter(None, params.split(' '))), reply, locale)
