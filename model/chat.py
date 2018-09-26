from pony import orm
from datetime import date
from model.database import db


class Chat(db.Entity):
    chat_id = orm.PrimaryKey(str)
    group_id = orm.Required(str)
    absent = orm.Required(orm.Json)

    @staticmethod
    @orm.db_session
    def register_chat(chat_id, group_id):
        if Chat.exists(chat_id=chat_id):
            Chat[chat_id].group_id = group_id
            return False
        else:
            Chat(
                chat_id=chat_id,
                group_id=group_id,
                absent={
                    "absent": []
                }
            )
        return True

    @staticmethod
    @orm.db_session
    def get_chat_by_chat_id(chat_id):
        if Chat.exists(chat_id=chat_id):
            return Chat[chat_id]
        return None

    @staticmethod
    @orm.db_session
    def remove_student(chat_id, student_id):
        if Chat.exists(chat_id=chat_id):
            chat = Chat[chat_id]
            Chat.clean_absent(chat)
            chat.absent['absent'] = list(filter(
                lambda student: student['student_id'] != student_id,
                chat.absent.get('absent', [])
            ))
            return True
        return False

    @staticmethod
    @orm.db_session
    def clean_absent(chat):
        today = str(date.today())
        if today != chat.absent.get('date', ''):
            chat.absent['absent'] = []
            chat.absent['date'] = today

    @staticmethod
    @orm.db_session
    def generate_list(chat_id, nothing_in_list, row_template):
        if Chat.exists(chat_id=chat_id):
            chat = Chat[chat_id]
            student_list = '\n'.join(map(lambda student: row_template.format(
                id=student['student_id'],
                name=student['student_name'],
                reason=student['reason'],
            ), chat.absent['absent']))
            if student_list:
                return student_list, chat.absent['date']
            return nothing_in_list, chat.absent['date']

        return None, None

    @staticmethod
    @orm.db_session
    def add_student(chat_id, student_name, student_id, reason=''):
        if Chat.exists(chat_id=chat_id):
            chat = Chat[chat_id]
            Chat.clean_absent(chat)
            students = chat.absent.get('absent', [])
            students.append(
                {
                    "student_id": student_id,
                    "student_name": student_name,
                    "reason": reason,
                }
            )
            chat.absent['absent'] = students
            return True
        return False
