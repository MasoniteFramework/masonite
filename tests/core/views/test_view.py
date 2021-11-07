from src.masonite.configuration import config
from src.masonite.helpers import url
from tests import TestCase


class TestView(TestCase):
    def setUp(self):
        super().setUp()
        # keep this to have a "fresh view instance" for each test
        self.view = self.application.make("view")
        self.view.loaders = []
        self.view.composers = {}
        self.view.add_location("tests/integrations/templates")

    def test_can_pass_dict(self):
        self.assertIn("test", self.view.render("test", {"test": "test"}).get_content())

    def test_view_exists(self):
        self.assertTrue(self.view.exists("welcome"))
        self.assertFalse(self.view.exists("not_available"))

    def test_view_render_does_not_keep_previous_variables(self):
        self.view.render("test", {"var1": "var1"})
        self.view.render("test", {"var2": "var2"})

        self.assertNotIn("var1", self.view.dictionary)
        self.assertIn("var2", self.view.dictionary)

    def test_global_view_exists(self):
        self.assertTrue(self.view.exists("/tests/integrations/templates/welcome"))
        self.assertFalse(
            self.view.exists("/tests/integrations/templates/not_available")
        )

    def test_view_gets_global_template(self):
        self.assertEqual(
            self.view.render(
                "/tests/integrations/templates/test", {"test": "test"}
            ).get_content(),
            "test",
        )

    def test_view_extends_without_dictionary_parameters(self):
        self.view.share({"test": "test"})
        self.assertEqual(self.view.render("test").get_content(), "test")

    def test_composers(self):
        view = self.view.composer("test", {"test": "test"})

        self.assertEqual(view.composers, {"test": {"test": "test"}})
        self.assertEqual(view.render("test").rendered_template, "test")

    def test_composers_load_all_views_with_asterisks(self):

        self.view.composer("*", {"test": "test"})

        self.assertEqual(self.view.composers, {"*": {"test": "test"}})

        self.assertEqual(self.view.render("test").get_content(), "test")

    def test_composers_with_wildcard_base_view(self):
        self.view.composer("mail*", {"to": "test_user"})

        self.assertEqual(self.view.composers, {"mail*": {"to": "test_user"}})

        self.assertIn("test_user", self.view.render("mail/welcome").get_content())

    def test_composers_with_wildcard_base_view_route(self):
        self.view.composer("mail*", {"to": "test_user"})

        self.assertEqual(self.view.composers, {"mail*": {"to": "test_user"}})

        self.assertIn("test_user", self.view.render("mail/welcome").get_content())

    def test_composers_with_wildcard_lower_directory_view_and_incorrect_shortend_wildcard(
        self,
    ):
        self.view.composer("mail/wel*", {"to": "test_user"})

        self.assertEqual(self.view.composers, {"mail/wel*": {"to": "test_user"}})

        assert "test_user" not in self.view.render("mail/welcome").get_content()

    def test_composers_load_all_views_with_list(self):
        self.view.composer(["home", "test"], {"test": "test"})

        self.assertEqual(
            self.view.composers, {"home": {"test": "test"}, "test": {"test": "test"}}
        )

        self.assertEqual(self.view.render("test").rendered_template, "test")

    def test_view_share_updates_dictionary_not_overwrite(self):
        self.view.share({"test1": "test1"})
        self.view.share({"test2": "test2"})

        self.assertEqual(self.view._shared["test1"], "test1")
        self.assertEqual(self.view._shared["test2"], "test2")
        self.view.render("test", {"var1": "var1"})
        self.assertIn("test1", self.view.dictionary.keys())
        self.assertIn("test2", self.view.dictionary.keys())
        self.assertIn("var1", self.view.dictionary.keys())

    def test_can_use_namespaced_view(self):
        self.view.add_namespaced_location("auth", "tests/integrations/templates/auth")
        self.assertIn("Welcome", self.view.render("auth:home").get_content())

    def test_can_access_shared_helpers(self):
        content = self.view.render("test_helpers").get_content()
        self.assertIn(
            config("application.app_url"),
            content,
        )
        self.assertIn(url.asset("local", "avatar.jpg"), content)
        self.assertIn(url.url("welcome"), content)
