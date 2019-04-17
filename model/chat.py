from pony import orm
from model.database import db
from model.group import Group


class Chat(db.Entity):
    chat_id = orm.Required(str)
    chat_type = orm.Required(str)
    group = orm.Required(Group)

    def get_group(self):
        """
        Returns chat's group
        :return: Chat's group
        :rtype: Group
        """
        return self.group

    @staticmethod
    @orm.db_session
    def register_chat(chat_id, chat_type, group_id):
        """
        Binds chat with group
        :param chat_id: Bind chat ID
        :param chat_type: Chat type (social network/messenger)
        :param group_id: Group ID that will be bind together with chat
        :return: True if chat was just created, False if group was just replaced
        """
        chat = Chat.get_chat(chat_id, chat_type)
        if chat is None:
            Chat(
                chat_id=chat_id,
                chat_type=chat_type,
                group=Group.get_or_create_group(group_id)
            )
            return True

        chat.group = Group.get_or_create_group(group_id)
        return False

    @staticmethod
    @orm.db_session
    def get_chat(chat_id, chat_type):
        """
        Returns Chat for chat ID
        :param chat_id: Chat ID that you are looking for
        :param chat_type: Chat type that you are looking for
        :return: Chat for that Chat ID and type or None
        :rtype: Chat
        """
        return Chat.get(chat_id=chat_id, chat_type=chat_type)

    @orm.db_session
    def generate_absent_list(self, nothing_in_list_template, row_template):
        """
        Fills absent people to template
        :param nothing_in_list_template: Template for empty list
        :type nothing_in_list_template: str
        :param row_template: Template for filled list
        :type row_template: str
        :return: Filled template
        :rtype: str
        """
        student_list = '\n'.join(map(lambda student: row_template.format(
            id=student['student_id'],
            name=student['student_name'],
            reason=student['reason'],
        ), self.group.get_absent_list()))
        if student_list:
            return student_list, self.group.absent['date']
        return nothing_in_list_template, self.group.absent['date']

    @orm.db_session
    def remove_student(self, student_id):
        self.group.remove_student(student_id)

    @orm.db_session
    def add_student(self, student_name, student_id, reason=''):
        self.group.add_student(student_name, student_id, reason)

