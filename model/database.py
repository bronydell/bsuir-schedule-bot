from peewee import SqliteDatabase, Model
import functools

db = SqliteDatabase("database.sqlite")


class BaseModel(Model):
    class Meta:
        database = db


def db_session(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        did_open_connection = False
        if db.is_closed():
            did_open_connection = True
            db.connect()

        return_value = func(*args, **kwargs)

        if did_open_connection:
            db.close()
        return return_value

    return decorator
