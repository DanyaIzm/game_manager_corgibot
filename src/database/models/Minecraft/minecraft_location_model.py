from tkinter import Y
from pony import orm

from database import database


def create_minecraft_location_model(database: orm.Database, location_type_model, world_model) -> database.Entity:
    class MinecraftLocationModel(database.Entity):
        name = orm.Required(str)
        # Координаты локации
        x = orm.Required(int)
        y = orm.Required(int)
        z = orm.Required(int)
        type = orm.Required(location_type_model)
        world = orm.Required(world_model)

    return MinecraftLocationModel
