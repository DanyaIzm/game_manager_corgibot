from pony import orm

from database import database


def create_minecraft_location_type_model(database: orm.Database) -> database.Entity:
    class MinecraftLocationTypeModel(database.Entity):
        # Название типа локации, e.g. "локация нижнего мира, деревня, шахта, пещера, локация энда"
        name = orm.Required(str)
        locations = orm.Set('MinecraftLocationModel')


    return MinecraftLocationTypeModel
