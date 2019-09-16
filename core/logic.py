from time import time
from saver import open_global_pref
from schedule.exceptions import NoSchedule
from schedule.api import get_schedule
from schedule.prettify import prettify_schedule
from schedule.tools import get_today_schedule, get_tomorrow_schedule
from model.chat import Chat
from replyer import BaseReply
from json import load

#constant for now
loc = 'ru'

def help_command(command, explanation, template):
    return template.format(
        command=command,
        explanation=explanation,
    )


def has_triggered_command(command_list, message):
    for phrase in command_list:
        if message.startswith(phrase.lower()):
            return phrase


def parse_message(command_list, message):
    lowercase_message = message.lower()
    for command in command_list.keys():
        triggered_phrase = has_triggered_command(command_list[command]["commands"], lowercase_message)
        if triggered_phrase:
            params = message[len(triggered_phrase):].strip()
            return command, params
    return None, None


def perform_command(command: str, params: str, reply: BaseReply, locale):
    try:
        chat = Chat.get_chat(str(reply.get_chat_id()), str(reply.get_chat_type()))
        if command == "get_current_schedule":
            if len(params) == 0:
                if chat:
                    schedule = get_schedule(chat.get_group().group_id)
                else:
                    reply.send_text(locale['chat_is_not_registered'])
                    return
            else:
                schedule = get_schedule(params[0])
            reply.send_text(get_prettified_schedule(locale, schedule, get_today_schedule))

        if command == "get_tomorrow_schedule":
            if chat:
                schedule = get_schedule(chat.get_group().group_id)
            else:
                reply.send_text(locale['chat_is_not_registered'])
                return
            reply.send_text(get_prettified_schedule(locale, schedule, get_tomorrow_schedule))

        if command == "building_info":
            if len(params) == 0:
                reply.send_text(locale['building_not_found'])
            else:
                try:
                    # TODO: Fix bug with commands here
                    building = locale['buildings'][params[0]]
                    reply.send_text(locale['building_template'].format(number=params[0], name=building['name'], google=building['google']))
                except KeyError:
                    reply.send_text(locale['building_not_found'])

        if command == "uptime":
            start_time = open_global_pref('start_time', None)
            diff_time = time() - start_time
            hours = int(diff_time / 3600)
            minutes = int((diff_time - hours * 3600) / 60)
            seconds = int((diff_time - hours * 3600 - minutes * 60))
            reply.send_text(locale['uptime_template'].format(hours=hours, minutes=minutes, seconds=seconds))

        if command == "absent":
            is_done = chat.add_student(reply.get_message_author_name(),
                                                   reply.get_message_author(),
                                                   reason=params)
            if is_done:
                reply.send_text(locale['done_absent'])
            else:
                reply.send_text(locale['cant_absent'])

        if command == "deabsent":
            is_done = chat.remove_student(reply.get_message_author())
            if is_done:
                reply.send_text(locale['done_deabsent'])
            else:
                reply.send_text(locale['didnt_deabsent'])

        if command == "absent_list":
            resp_list, date = chat.generate_absent_list(locale['default_list_content'],
                                                        locale['row_template'])
            if resp_list:
                reply.send_text(locale['list_template'].format(
                    date=date,
                    content=resp_list
                ))
            else:
                reply.send_text(locale['cant_make_list'])

        if command == "register_chat":
            group_id = params.strip()

            if Chat.register_chat(str(reply.get_chat_id()), reply.get_chat_type(), group_id):
                reply.send_text(locale['registered'].format(group_id=group_id))
            else:
                reply.send_text(locale['group_has_changed'].format(group_id=group_id))

        if command == "help":
            content = '\n'.join(map(lambda command:
                                    help_command(locale["commands"][command]["commands"][0],
                                                 locale["commands"][command]["explanation"],
                                                 locale["row_help_template"]),
                                    locale["commands"].keys()))
            reply.send_text(locale['help_message'].format(
                help_message=content
            ))

        if command == "group":
            reply.send_text(locale["group_template"].format(group=chat.get_group().group_id))

    except NoSchedule:
        reply.send_text(locale['group_not_found'])


def get_prettified_schedule(locale, schedule, selector):
    lesson_template = locale['lesson_template']
    subgroup_template = locale['subgroup_template']
    lesson_types = locale['lesson_types']
    nothing = locale['nope']
    schedule = selector(schedule)

    return prettify_schedule(schedule,
                             lesson_template,
                             lesson_types,
                             subgroup_template,
                             nothing)


def on_message(reply: BaseReply, message_text):
    with open(file=loc+'.json', encoding="UTF-8") as file:
        locale = load(file)
    if message_text.startswith(locale['prefix']):
        # We should remove prefix
        message = message_text[1:]
        command, params = parse_message(locale['commands'], message)
        if command:
            perform_command(command, params, reply, locale)
