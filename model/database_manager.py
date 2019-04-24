from model.group import Group
from model.chat import Chat
from model.database import db


def generate_database():
    db.create_tables([Chat, Group])