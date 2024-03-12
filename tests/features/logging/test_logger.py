import pendulum
import tempfile

from tests import TestCase
from src.masonite.facades import Log, Config


class TestLogger(TestCase):
    def setUp(self):
        super().setUp()
        self.timestamp = pendulum.datetime(2022, 10, 10, 9, 0, 0)
        self.fakeTime(self.timestamp)

        self.log_file_path = Config.get("logging.channels.single.path")
        self.log_file = tempfile.NamedTemporaryFile(mode="w+")
        Config.set("logging.channels.single.path", self.log_file.name)

    def tearDown(self):
        super().tearDown()
        self.restoreTime()
        Config.set("logging.channels.single.path", self.log_file)

    def test_terminal_logging(self):
        Log.error("message")
        self.assertConsoleOutputContains("2022-10-10 09:00:00 - ERROR: message")

    def test_terminal_logging_with_other_level(self):
        Log.info("other message")
        self.assertConsoleOutputContains("2022-10-10 09:00:00 - INFO: other message")

    def test_that_messages_under_min_level_are_not_logged(self):
        Log.debug("other message")
        self.assertConsoleEmpty()

    def test_timezone_can_be_changed(self):
        old_timezone = Config.get("logging.channels.default.timezone")
        Config.set("logging.channels.default.timezone", "Europe/Paris")

        Log.info("other message")
        timestamp_in_tz = self.timestamp.in_tz("Europe/Paris").format(
            "YYYY-MM-DD HH:mm:ss"
        )
        self.assertConsoleOutputContains(f"{timestamp_in_tz} - INFO: other message")

        Config.set("logging.channels.default.timezone", old_timezone)

    def test_stack_channels(self):
        Log.stack("single", "console").warning("message")
        # check logged in file
        self.assertEqual(
            str(self.log_file.readline()),
            "2022-10-10 09:00:00 - WARNING: message\n",
        )
        # check logged in console
        self.assertConsoleOutputContains("2022-10-10 09:00:00 - WARNING: message")

    def test_file_logging(self):
        Log.channel("single").warning("Some warning")
        self.assertEqual(
            str(self.log_file.readline()),
            "2022-10-10 09:00:00 - WARNING: Some warning\n",
        )

    def test_on_demand_channel(self):
        Log.build(
            "daily", {"path": self.log_file.name, "format": "{message}"}
        ).critical("Some message")
        self.assertEqual(
            self.log_file.readline(),
            "Some message\n",
        )
