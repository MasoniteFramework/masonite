from cleo import CommandTester


class TestCommand:
    """This class allows us to test craft commands and asserts command outputs."""

    def __init__(self, application):
        self.application = application

    def run(self, command, arguments_str=""):
        command = self.application.make("commands").command_application.find(command)
        self.command_tester = CommandTester(command)
        self.command_tester.execute(arguments_str)
        return self

    def assertExactOutput(self, ref_output):
        """Assert command output to be exactly the same as the given reference output."""
        output = self._get_output()
        assert ref_output == output, f"Command output was: {output}, not {ref_output}"
        return self

    def assertOutputContains(self, ref_output):
        output = self._get_output()
        assert (
            ref_output in output
        ), f"Command output was: {output} and does not contain {ref_output}."
        return self

    def assertOutputMissing(self, ref_output):
        """Assert command output does not contain the given reference output."""
        output = self._get_output()
        assert (
            ref_output not in output
        ), f"Command output was: {output}, not {ref_output}"
        return self

    def assertHasErrors(self):
        assert self._get_errors()
        return self

    def assertExactErrors(self, ref_errors):
        errors = self._get_errors()
        assert (
            errors == ref_errors
        ), f"Command output has errors: {errors}, not {ref_errors}."
        return self

    def assertSuccess(self):
        """Assert that command returned a 0 exit code meaning that it ran successfully."""
        code = self.command_tester.status_code
        assert 0 == code, "Command exited code is not 0: {code}."
        return self

    def _get_errors(self):
        return self.command_tester.io.fetch_error()

    def _get_output(self):
        return self.command_tester.io.fetch_output()
