import unittest

import requests
import responses
import shutil
import os
from mock import patch
from cleo import Application
from cleo import CommandTester

from src.masonite.commands.NewCommand import NewCommand
from src.masonite.exceptions import ProjectLimitReached, ProjectProviderTimeout, \
    ProjectProviderHttpError, ProjectTargetNotEmpty


class TestNewCommand(unittest.TestCase):

    test_project_dir = os.path.join(os.getcwd(), "new_project")

    def setUp(self):
        self.application = Application()
        self.application.add(NewCommand())
        self.command = self.application.find('new')
        self.command_tester = CommandTester(self.command)

        self.default_repo = "MasoniteFramework/cookie-cutter"
        # ensure cleaning after each test

    def tearDown(self):
        # ensure cleaning after each
        shutil.rmtree(self.test_project_dir, ignore_errors=True)

    @classmethod
    def tearDownClass(cls):
        # ensure cleaning event if test suite fails
        shutil.rmtree(cls.test_project_dir, ignore_errors=True)

    def test_cannot_craft_to_not_empty_directory(self):
        # run command without arguments, target is the current directory which is not empty
        with self.assertRaises(ProjectTargetNotEmpty):
            self.command_tester.execute([])

        with self.assertRaises(ProjectTargetNotEmpty):
            self.command_tester.execute([('target', '../../tests')])

    def test_handle_not_implemented_provider(self):
        self.command_tester.execute([('target', 'new_project'), ('--provider', 'bitbucket')])
        self.assertEqual("'provider' option must be in github,gitlab\n", self.command_tester.get_display())

    @responses.activate
    def test_handle_incorrect_branch(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/branches/unknown'.format(self.default_repo),
            body='[]'
        )

        self.command_tester.execute([('target', 'new_project'), ('--branch', 'unknown')])
        self.assertEqual("Branch unknown does not exist.\n", self.command_tester.get_display())

    @responses.activate
    def test_handle_incorrect_version(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases'.format(self.default_repo),
            body='{}'
        )

        self.command_tester.execute([('target', 'new_project'), ('--release', '0.0.0')])
        self.assertEqual("Version 0.0.0 could not be found.\n", self.command_tester.get_display())

    @responses.activate
    def test_handle_incorrect_version(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases'.format(self.default_repo),
            body='{}'
        )

        self.command_tester.execute([('target', 'new_project'), ('--release', '0.0.0')])
        self.assertEqual("Version 0.0.0 could not be found\n", self.command_tester.get_display())

    @responses.activate
    def test_correct_version_is_displayed(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases'.format(self.default_repo),
            body='[{"name": "v2.3.6", "tag_name": "v2.3.6", "zipball_url": "https://api.github.com/repos/MasoniteFramework/cookie-cutter/zipball/v2.3.6"}]'
        )

        self.command_tester.execute([('target', 'new_project'), ('--release', '2.3.6')])
        self.assertTrue(self.command_tester.get_display().startswith("Installing version v2.3.6"))

    @responses.activate
    def test_warning_is_displayed_when_no_tags_in_repo(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases'.format(self.default_repo),
            body='{}'
        )

        self.command_tester.execute([('target', 'new_project')])
        self.assertTrue("[WARNING] No tags has been found, using latest commit on master." in self.command_tester.get_display())

    @responses.activate
    def test_api_rate_limit_are_handled(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases'.format(self.default_repo),
            status=403,
        )
        # allow reproducing error raised by Github API
        with patch('six.moves.http_client.responses',
                   get=lambda status: "rate limit exceeded"):
            with self.assertRaises(ProjectLimitReached):
                self.command_tester.execute([('target', 'new_project')])

    @responses.activate
    def test_unknown_repos_are_handled(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/MasoniteFramework/unknown_repo/releases',
            status=404,
        )

        with self.assertRaises(ProjectProviderHttpError) as e:
            self.command_tester.execute([('target', 'new_project'), ('--repo', 'MasoniteFramework/unknown_repo')])

        self.assertTrue(str(e.exception).startswith("Not Found(404)"))

    @responses.activate
    def test_private_repos_errors_are_handled(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/MasoniteFramework/secret/releases',
            status=403,
        )

        with self.assertRaises(ProjectProviderHttpError) as e:
            self.command_tester.execute([('target', 'new_project'), ('--repo', 'MasoniteFramework/secret')])

        self.assertTrue(str(e.exception).startswith("Forbidden(403)"))

    @responses.activate
    def test_timeouts_are_handled(self):
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases'.format(self.default_repo),
            body=requests.Timeout(),
        )

        with self.assertRaises(ProjectProviderTimeout) as e:
            self.command_tester.execute([('target', 'new_project')])

        self.assertTrue(str(e.exception).startswith("github provider is not reachable"))

    def test_download_errors_are_displayed(self):
        pass

    @responses.activate
    def test_can_craft_default_repo_successfully(self):
        # still mocking requests to avoid failures from api rate limits
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases'.format(self.default_repo),
            body='[{"name": "v2.3.6", "tag_name": "v2.3.6", "zipball_url": "https://api.github.com/repos/MasoniteFramework/cookie-cutter/zipball/v2.3.6", "prerelease": false}]'
        )
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases/tags/v2.3.6'.format(self.default_repo),
            body='{"zipball_url": "https://api.github.com/repos/MasoniteFramework/cookie-cutter/zipball/v2.3.6"}'
        )

        self.command_tester.execute([('target', 'new_project')])
        self.assertTrue(
            "Project Created Successfully" in self.command_tester.get_display()
        )
        # verify that project has really been created by checking files
        self.assertTrue("craft" in os.listdir(self.test_project_dir))
        self.assertTrue("app" in os.listdir(self.test_project_dir))

    @responses.activate
    def test_can_craft_other_repo_successfully(self):
        # using a real repo but not a masonite project template, just for testing
        other_repo = "MasoniteFramework/docs"
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases'.format(other_repo),
            body='[{"name": "v2.3.6", "tag_name": "v2.3.6", "zipball_url": "https://api.github.com/repos/MasoniteFramework/cookie-cutter/zipball/v2.3.6", "prerelease": false}]'
        )
        responses.add(responses.GET,
            'https://api.github.com/repos/{0}/releases/tags/v2.3.6'.format(other_repo),
            body='{"zipball_url": "https://api.github.com/repos/MasoniteFramework/cookie-cutter/zipball/v2.3.6"}'
        )

        self.command_tester.execute([('target', 'new_project'), ("--repo", other_repo)])
        self.assertTrue(
            "Project Created Successfully" in self.command_tester.get_display()
        )
        # verify that project has really been created by checking files
        self.assertTrue("craft" in os.listdir(self.test_project_dir))
        self.assertTrue("app" in os.listdir(self.test_project_dir))
