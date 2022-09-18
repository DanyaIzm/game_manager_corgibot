from pony import orm

database = orm.Database()

database.bind(provider='sqlite', filename='database.sqlite', create_db=True)
