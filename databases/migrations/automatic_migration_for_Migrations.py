''' A Migration File '''
from playhouse.migrate import *
from app.Migrations import Migrations

from config import database

engine = database.engines['default']
migrator = MySQLMigrator(engine)

engine.drop_table(Migrations, True)
engine.create_table(Migrations, True)

Migrations.create(migration='automatic_migration_for_Migrations.py', batch=1)
Migrations.create(migration='automatic_migration_for_Users.py')
