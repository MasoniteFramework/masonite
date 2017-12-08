''' A Migration File '''
from playhouse.migrate import *
from app.Users import Users
from app.Migrations import Migrations
import os
from config import database

engine = database.engines['default']
migrator = MySQLMigrator(engine)

engine.drop_table(Users, True)
engine.create_table(Users, True)

query = Migrations.update(batch=1).where(
    Migrations.migration == os.path.basename(__file__))
query.execute()
