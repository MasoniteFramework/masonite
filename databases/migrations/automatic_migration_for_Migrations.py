''' A Migration File '''
from app.Migrations import Migrations

from config import database

ENGINE = database.ENGINES['default']

ENGINE.drop_table(Migrations, True)
ENGINE.create_table(Migrations, True)

Migrations.create(migration='automatic_migration_for_Migrations.py', batch=1)
Migrations.create(migration='automatic_migration_for_Users.py')
