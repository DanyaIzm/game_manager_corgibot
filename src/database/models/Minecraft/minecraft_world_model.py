from pony import orm 

from database import database


def create_minecraft_word_model(database: orm.Database) -> database.Entity:
    class MinecraftWorldModel(database.Entity):
        # Название мира
        name = orm.Required(str)
        # Версия, e.g. 1.19.2
        version = orm.Required(str)
        # Описание мира и всякие дополнительные заметки, e.g. "Осень 2022"
        description = orm.Optional(str)

        locations = orm.Set('MinecraftLocationModel')

    return MinecraftWorldModel
