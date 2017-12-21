''' A Migration File '''
import os

from app.Migrations import Migrations
from app.Users import Users
from config import database

ENGINE = database.ENGINES['default']

ENGINE.drop_table(Users, True)
ENGINE.create_table(Users, True)

QUERY = Migrations.update(batch=1).where(
    Migrations.migration == os.path.basename(__file__))
QUERY.execute()
