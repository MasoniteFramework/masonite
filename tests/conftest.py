"""
pytest session-scoped fixtures that manage the test SQLite database.

The database.sqlite3 file is created fresh at the start of every test
session (migrations + seeds applied) and deleted when the session ends.
It is not committed to version control.
"""

import os
import pathlib
import pytest

# Absolute path to the SQLite file so it is always resolved relative to
# the repo root regardless of where pytest is invoked from.
_REPO_ROOT = pathlib.Path(__file__).parent.parent
_DB_PATH = _REPO_ROOT / "database.sqlite3"

_MIGRATION_DIR = "tests/integrations/databases/migrations"
_SEED_PATH = "tests/integrations/databases/seeds"
_DB_CONFIG_PATH = "tests/integrations/config/database"
_CONNECTION = "sqlite"


def _build_db():
    """Run migrations and seeds against a fresh SQLite database."""
    from masoniteorm.migrations import Migration
    from masoniteorm.seeds import Seeder
    from tests.integrations.databases.seeds.database_seeder import DatabaseSeeder

    migration = Migration(
        connection=_CONNECTION,
        migration_directory=_MIGRATION_DIR,
        config_path=_DB_CONFIG_PATH,
    )
    migration.create_table_if_not_exists()
    migration.migrate(output=False)

    seeder = Seeder(connection=_CONNECTION, seed_path=_SEED_PATH)
    seeder.call(DatabaseSeeder)


def _destroy_db():
    """Remove the SQLite database file."""
    if _DB_PATH.exists():
        _DB_PATH.unlink()


@pytest.fixture(scope="session", autouse=True)
def test_database():
    """
    Session-scoped fixture: create the SQLite database before any test
    runs and tear it down once the entire session finishes.

    The DB_CONFIG_PATH env var is set first so masonite-orm can locate
    the connection config when QueryBuilder.on() calls load_config().
    """
    os.environ.setdefault("DB_CONFIG_PATH", _DB_CONFIG_PATH)

    # Always start from a clean slate so tests are deterministic.
    _destroy_db()
    _build_db()

    yield
    # leave database in place for after test examination
