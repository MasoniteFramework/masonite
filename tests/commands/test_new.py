import unittest
import responses
from cleo import Application
from cleo import CommandTester

from src.masonite.commands.NewCommand import NewCommand
from src.masonite.exceptions import ProjectLimitReached, ProjectProviderTimeout, \
    ProjectProviderHttpError, ProjectTargetNotEmpty


class TestNewCommand(unittest.TestCase):

    def setUp(self):
        self.application = Application()
        self.application.add(NewCommand())
        self.command = self.application.find('new')
        self.command_tester = CommandTester(self.command)

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
    def test_handle_provider_(self):
        responses.add(responses.GET, 'https://api.github.com/repos/test_user/test_repo',
                  body=Exception('test'))
        responses.add(responses.GET, 'https://api.github.com/repos/test_user/test_repo/releases',
                  body=Exception('test'))

        self.command_tester.execute([('target', 'new_project'), ('--repo', 'test_user/test_repo')])