from database.database import database

from database.models.user_model import create_user_model
from database.models.game_model import create_game_model

UserModel = create_user_model(database)
GameModel = create_game_model(database)


database.generate_mapping(create_tables=True)
