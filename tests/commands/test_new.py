import unittest
import requests
import responses
import shutil
import os
import json
from mock import patch
from cleo import Application
from cleo import CommandTester

from src.masonite.commands.NewCommand import NewCommand
from src.masonite.exceptions import ProjectLimitReached, ProjectProviderTimeout, \
    ProjectProviderHttpError
from src.masonite import __cookie_cutter_version__


class TestNewCommand(unittest.TestCase):

    test_project_dir = os.path.join(os.getcwd(), "new_project")

    def setUp(self):
        self.application = Application()
        self.application.add(NewCommand())
        self.command = self.application.find('new')
        self.command_tester = CommandTester(self.command)

        self.default_repo = "MasoniteFramework/cookie-cutter"
        self.default_branch = __cookie_cutter_version__

    def tearDown(self):
        # ensure cleaning after each test
        shutil.rmtree(self.test_project_dir, ignore_errors=True)

    @classmethod
    def tearDownClass(cls):
        # ensure cleaning even if test suite fails
        shutil.rmtree(cls.test_project_dir, ignore_errors=True)

    def test_handle_not_implemented_provider(self):
        self.command_tester.execute("new_project --provider bitbucket")
        self.assertEqual("'provider' option must be in github,gitlab\n", self.command_tester.io.fetch_error())

    @responses.activate
    def test_handle_incorrect_branch(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/branches/unknown'.format(self.default_repo),
            body='[]'
        )

        self.command_tester.execute("new_project --branch unknown")
        self.assertEqual("Branch unknown does not exist.\n", self.command_tester.io.fetch_error())

    @responses.activate
    def test_handle_incorrect_version(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases'.format(self.default_repo),
            body='{}'
        )

        self.command_tester.execute("new_project --release 0.0.0")
        self.assertEqual("Version 0.0.0 could not be found.\n", self.command_tester.io.fetch_error())

    @responses.activate
    def test_handle_incorrect_version(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases'.format(self.default_repo),
            body='{}'
        )

        self.command_tester.execute("new_project --release 0.0.0")
        self.assertEqual("Version 0.0.0 could not be found\n", self.command_tester.io.fetch_error())

    @responses.activate
    def test_correct_version_is_displayed(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases'.format(self.default_repo),
            body='[{"name": "v2.3.6", "tag_name": "v2.3.6", "zipball_url": "https://api.github.com/repos/MasoniteFramework/cookie-cutter/zipball/v2.3.6"}]'
        )
        # authorize requests not using the API
        responses.add_passthru('https://api.github.com/repos/MasoniteFramework/cookie-cutter/zipball/v2.3.6')
        responses.add_passthru('https://codeload.github.com/MasoniteFramework/cookie-cutter/legacy.zip/v2.3.6')

        self.command_tester.execute("new_project --release 2.3.6")
        self.assertTrue(self.command_tester.io.fetch_output().startswith("Installing version v2.3.6"))

    @responses.activate
    def test_warning_is_displayed_when_no_tags_in_repo_if_not_official(self):
        # there is no tags on this test repo
        # mock this one as it can be rate limited
        responses.add(responses.GET,
            'https://gitlab.com/api/v4/projects/samuelgirardin%2Fmasonite-tests/releases',
            body='[]'
        )
        # authorize requests not using the API
        responses.add_passthru('https://gitlab.com/api/v4/projects/samuelgirardin%2Fmasonite-tests/repository/archive.zip?sha=master')
        self.command_tester.execute("new_project --repo samuelgirardin/masonite-tests --provider gitlab")
        self.assertTrue("No tags has been found, using latest commit on master." in self.command_tester.io.fetch_output())

    @responses.activate
    def test_api_rate_limit_are_handled(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/branches/{1}'.format(
                self.default_repo, self.default_branch
            ),
            status=403,
        )

        # allow reproducing error raised by Github API
        with patch('six.moves.http_client.responses',
                   get=lambda status: "rate limit exceeded"):
            with self.assertRaises(ProjectLimitReached):
                self.command_tester.execute("new_project")

    @responses.activate
    def test_unknown_repos_are_handled(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/MasoniteFramework/unknown_repo/releases',
            status=404,
        )

        with self.assertRaises(ProjectProviderHttpError) as e:
            self.command_tester.execute("new_project --repo MasoniteFramework/unknown_repo")

        self.assertTrue(str(e.exception).startswith("Not Found(404)"))

    @responses.activate
    def test_private_repos_errors_are_handled(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/MasoniteFramework/secret/releases',
            status=403,
        )

        with self.assertRaises(ProjectProviderHttpError) as e:
            self.command_tester.execute("new_project --repo MasoniteFramework/secret")

        self.assertTrue(str(e.exception).startswith("Forbidden(403)"))

    @responses.activate
    def test_timeouts_are_handled(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/branches/{1}'.format(
                self.default_repo, self.default_branch
            ),
            body=requests.Timeout(),
        )

        with self.assertRaises(ProjectProviderTimeout) as e:
            self.command_tester.execute("new_project")

        self.assertTrue(str(e.exception).startswith("github provider is not reachable"))

    # Following tests are close to integration tests but still quick and without rate limiting issue so
    # they can be ran as unit tests
    # ----------------------------------------------------------------------------------------------
    @responses.activate
    def test_can_craft_default_repo_successfully(self):
        # still mocking requests to avoid failures from api rate limits
        body = {"name": self.default_branch}
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/branches/{1}'.format(
                self.default_repo, self.default_branch
            ),
            body=json.dumps(body)
        )
        # authorize requests not using the API
        responses.add_passthru(
            'https://github.com/MasoniteFramework/cookie-cutter/archive/{0}.zip'.format(self.default_branch)
        )
        responses.add_passthru(
            'https://codeload.github.com/MasoniteFramework/cookie-cutter/zip/{0}'.format(self.default_branch)
        )

        self.command_tester.execute("new_project")
        self.assertTrue(
            "Project Created Successfully" in self.command_tester.io.fetch_output()
        )
        # verify that project has really been created by checking files
        self.assertTrue("craft" in os.listdir(self.test_project_dir))
        self.assertTrue("app" in os.listdir(self.test_project_dir))

    @responses.activate
    def test_can_craft_default_repo_successfully_with_release(self):
        # still mocking requests to avoid failures from api rate limits
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases'.format(self.default_repo),
            body='[{"name": "v2.3.6", "tag_name": "v2.3.6", "zipball_url": "https://api.github.com/repos/MasoniteFramework/cookie-cutter/zipball/v2.3.6", "prerelease": false}]'
        )
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases/tags/v2.3.6'.format(self.default_repo),
            body='{"zipball_url": "https://api.github.com/repos/MasoniteFramework/cookie-cutter/zipball/v2.3.6"}'
        )
        # authorize requests not using the API
        responses.add_passthru('https://api.github.com/repos/MasoniteFramework/cookie-cutter/zipball/v2.3.6')
        responses.add_passthru('https://codeload.github.com/MasoniteFramework/cookie-cutter/legacy.zip/v2.3.6')

        self.command_tester.execute("new_project --release 2.3.6")
        self.assertTrue(
            "Project Created Successfully" in self.command_tester.io.fetch_output()
        )
        # verify that project has really been created by checking files
        self.assertTrue("craft" in os.listdir(self.test_project_dir))
        self.assertTrue("app" in os.listdir(self.test_project_dir))

    @responses.activate
    def test_can_craft_default_repo_successfully_with_branch(self):
        # still mocking requests to avoid failures from api rate limits
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/branches/2.3'.format(self.default_repo),
            body='{"name": "2.3"}'
        )
        # authorize requests not using the API
        responses.add_passthru('https://github.com/MasoniteFramework/cookie-cutter/archive/2.3.zip')
        responses.add_passthru('https://codeload.github.com/MasoniteFramework/cookie-cutter/zip/2.3')

        self.command_tester.execute("new_project --branch 2.3")
        self.assertTrue(
            "Project Created Successfully" in self.command_tester.io.fetch_output()
        )
        # verify that project has really been created by checking files
        self.assertTrue("craft" in os.listdir(self.test_project_dir))
        self.assertTrue("app" in os.listdir(self.test_project_dir))

    @responses.activate
    def test_can_craft_project_with_gitlab_provider(self):
        # mock this one as it can be rate limited
        responses.add(responses.GET,
            'https://gitlab.com/api/v4/projects/samuelgirardin%2Fmasonite-tests/releases',
            body='[]'
        )
        # authorize requests not using the API
        responses.add_passthru('https://gitlab.com/api/v4/projects/samuelgirardin%2Fmasonite-tests/repository/archive.zip?sha=master')

        repo = "samuelgirardin/masonite-tests"
        self.command_tester.execute("new_project --provider gitlab --repo {0}".format(repo))
        self.assertTrue(
            "Project Created Successfully" in self.command_tester.io.fetch_output()
        )
        # verify that project has really been created by checking files
        self.assertTrue("README.md" in os.listdir(self.test_project_dir))
