import unittest
from core import logic


class CoreTest(unittest.TestCase):
    default_test_command = {
        "doge_command": {
            "commands": [
                "doge"
            ]
        }
    }

    def test_parse_command_and_params(self):
        test_message = "doge param"
        test_commands = self.default_test_command
        command, params = logic.parse_message(test_commands, test_message)
        self.assertEqual("doge_command", command)
        self.assertEqual("param", params)

    def test_parse_command_and_uppercase_params(self):
        test_message = "doge Param"
        test_commands = self.default_test_command
        command, params = logic.parse_message(test_commands, test_message)
        self.assertEqual("doge_command", command)
        self.assertEqual("Param", params)

    def test_parse_uppercase_command_and_params(self):
        test_message = "DoGe param"
        test_commands = self.default_test_command
        command, params = logic.parse_message(test_commands, test_message)
        self.assertEqual("doge_command", command)
        self.assertEqual("param", params)

    def test_parse_command_without_params(self):
        test_message = "doge"
        test_commands = self.default_test_command
        command, params = logic.parse_message(test_commands, test_message)
        self.assertEqual("doge_command", command)
        self.assertEqual("", params)

    def test_parse_nonexistent_command(self):
        test_message = "noone"
        test_commands = self.default_test_command
        command, params = logic.parse_message(test_commands, test_message)
        self.assertEqual(None, command)
        self.assertEqual(None, params)
