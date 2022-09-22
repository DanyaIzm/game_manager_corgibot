from pony import orm

from database import database


def create_game_model(database: orm.Database) -> database.Entity:
    class GameModel(database.Entity):
        name = orm.Required(str)

    return GameModel
