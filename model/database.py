from pony import orm

db = orm.Database()


def generate_database():
    db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
    db.generate_mapping(create_tables=True)

