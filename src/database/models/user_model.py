from pony import orm

from database import database

def create_user_model(database: orm.Database) -> database.Entity:
    class UserModel(database.Entity):
        id = orm.PrimaryKey(int)
        username = orm.Optional(str, nullable=True)
        first_name = orm.Required(str, nullable=True)
        last_name = orm.Required(str, nullable=True)
        is_admin = orm.Required(bool, default=False)

    return UserModel
