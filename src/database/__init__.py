from database.database import database

from database.models import user_model
from database.models import game_model

from database.models.Minecraft import minecraft_world_model, minecraft_location_type_model, minecraft_location_model


UserModel = user_model.create_user_model(database)
GameModel = game_model.create_game_model(database)


MinecraftWorldModel = minecraft_world_model.create_minecraft_word_model(database)
MinecraftLocationTypeModel = minecraft_location_type_model.create_minecraft_location_type_model(database)
MinecraftLocationModel = minecraft_location_model.create_minecraft_location_model(database, MinecraftLocationTypeModel, MinecraftWorldModel)


database.generate_mapping(create_tables=True)
