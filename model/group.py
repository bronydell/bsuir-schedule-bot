from pony import orm
from datetime import date
from model.database import db


class Group(db.Entity):
    group_id = orm.PrimaryKey(str)
    chats = orm.Set("Chat")
    absent = orm.Required(orm.Json)

    @staticmethod
    @orm.db_session
    def get_or_create_group(group_id):
        """
        Creates or returns already existed group
        :param group_id: Group ID
        :return: Returns group that was exited or just created
        :rtype: Group
        """
        if Group.exists(group_id=group_id):
            return Group[group_id]
        else:
            return Group(group_id=group_id,
                         absent={
                             "absent": []
                         })

    def remove_student(self, student_id):
        """
        Removes student with student_id from absent list
        :param student_id: Student ID that you are about ot delete
        :return: True if successful
        :rtype: bool
        """
        self.absent['absent'] = list(filter(
            lambda student: student['student_id'] != student_id,
            self.get_absent_list()
        ))
        return True

    def add_student(self, student_name, student_id, reason=''):
        """
        Adds student to student list
        :param student_name: Student's full name
        :param student_id: Student's ID
        :param reason: Reason
        """

        absent_student_list = self.get_absent_list()

        absent_student_list = list(filter(
            lambda student: student['student_id'] != student_id,
            absent_student_list
        ))

        absent_student_list.append(
            {
                "student_id": student_id,
                "student_name": student_name,
                "reason": reason,
            }
        )
        self.absent['absent'] = absent_student_list

    @orm.db_session
    def clean_absent_list(self):
        today = str(date.today())
        if today != self.absent.get('date', ''):
            self.absent['absent'] = []
            self.absent['date'] = today

    def get_absent_list(self):
        """
        Get filtered absent students
        :return: List of absent students
        :rtype: list
        """
        self.clean_absent_list()
        return self.absent.get('absent', [])
