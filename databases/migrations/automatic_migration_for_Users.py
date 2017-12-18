''' A Migration File '''
from app.Users import Users

from config import database

ENGINE = database.ENGINES['default']

ENGINE.drop_table(Users, True)
ENGINE.create_table(Users, True)
