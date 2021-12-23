import os
from tests import TestCase

from src.masonite.utils.location import (
    base_path,
    views_path,
    controllers_path,
    seeds_path,
    migrations_path,
    config_path,
    jobs_path,
    resources_path,
    models_path,
)


class TestLocation(TestCase):
    def test_base_path(self):
        base_dir = os.getcwd()
        location = base_path()
        self.assertEqual(base_dir, location)
        location = base_path("tests/integrations")
        self.assertEqual(os.path.join(base_dir, "tests/integrations"), location)

    def test_views_path(self):
        location = views_path("app.html")
        self.assertTrue(location.endswith("tests/integrations/templates/app.html"))
        location = views_path("account/app.html")
        self.assertTrue(
            location.endswith("tests/integrations/templates/account/app.html")
        )
        location = views_path("account/app.html", absolute=False)
        self.assertEqual("tests/integrations/templates/account/app.html", location)
        location = views_path(absolute=False)
        self.assertEqual(location, "tests/integrations/templates/")

    def test_controllers_path(self):
        location = controllers_path("MyController.py")
        self.assertTrue(
            location.endswith("tests/integrations/controllers/MyController.py")
        )
        location = controllers_path("account/MyController.py")
        self.assertTrue(
            location.endswith("tests/integrations/controllers/account/MyController.py")
        )
        location = controllers_path("MyController.py", absolute=False)
        self.assertEqual("tests/integrations/controllers/MyController.py", location)

    def test_config_path(self):
        location = config_path("app.py")
        self.assertTrue(location.endswith("tests/integrations/config/app.py"))
        location = config_path("package/base.py")
        self.assertTrue(location.endswith("tests/integrations/config/package/base.py"))
        location = config_path("app.py", absolute=False)
        self.assertEqual("tests/integrations/config/app.py", location)

    def test_migrations_path(self):
        location = migrations_path("create_users_table.py")
        self.assertTrue(
            location.endswith(
                "tests/integrations/databases/migrations/create_users_table.py"
            )
        )
        location = migrations_path("package/create_team_table.py")
        self.assertTrue(
            location.endswith(
                "tests/integrations/databases/migrations/package/create_team_table.py"
            )
        )
        location = migrations_path("create_users_table.py", absolute=False)
        self.assertEqual(
            "tests/integrations/databases/migrations/create_users_table.py", location
        )

    def test_seeds_path(self):
        location = seeds_path("create_users.py")
        self.assertTrue(
            location.endswith("tests/integrations/databases/seeds/create_users.py")
        )
        location = seeds_path("package/create_teams.py")
        self.assertTrue(
            location.endswith(
                "tests/integrations/databases/seeds/package/create_teams.py"
            )
        )
        location = seeds_path("create_users.py", absolute=False)
        self.assertEqual("tests/integrations/databases/seeds/create_users.py", location)

    def test_jobs_path(self):
        location = jobs_path("SomeTask.py")
        self.assertTrue(location.endswith("tests/integrations/jobs/SomeTask.py"))
        location = jobs_path("critical/SomeTask.py")
        self.assertTrue(
            location.endswith("tests/integrations/jobs/critical/SomeTask.py")
        )
        location = jobs_path("critical/SomeTask.py", absolute=False)
        self.assertEqual("tests/integrations/jobs/critical/SomeTask.py", location)
        location = jobs_path(absolute=False)
        self.assertEqual(location, "tests/integrations/jobs/")

    def test_resources_path(self):
        location = resources_path("js/Home.vue")
        self.assertTrue(location.endswith("tests/integrations/resources/js/Home.vue"))
        location = resources_path("js/Home.vue", absolute=False)
        self.assertEqual("tests/integrations/resources/js/Home.vue", location)
        location = resources_path(absolute=False)
        self.assertEqual(location, "tests/integrations/resources/")

    def test_models_path(self):
        location = models_path("User.py")
        self.assertTrue(location.endswith("tests/integrations/app/User.py"))
        location = models_path("admin/Log.py")
        self.assertTrue(location.endswith("tests/integrations/app/admin/Log.py"))
        location = models_path("admin/Log.py", absolute=False)
        self.assertEqual("tests/integrations/app/admin/Log.py", location)
        location = models_path(absolute=False)
        self.assertEqual(location, "tests/integrations/app/")
