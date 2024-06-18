import io
import sys

from typing import Callable

import unittest
from unittest.mock import patch

from jspsych_plus.management import management


class TestManagement(unittest.TestCase):
    def test_help(self):
        """
        Tests whether these commands:
        - jspsych help
        - jspsych -h
        - jspsych
        - jspsych invalid-command
        corrects print the help info
        """
        help_msg: str = self.redirect_stdout(management.print_help)

        self.assertPrints(self.mock_cmd_call(["help"]), help_msg)
        self.assertPrints(self.mock_cmd_call(["-h"]), help_msg)
        self.assertPrints(self.mock_cmd_call([]), help_msg)
        self.assertPrints(self.mock_cmd_call(["invalid-command"]), help_msg)

    def assertPrints(self, func: Callable, content: str, msg: str = "") -> None:
        """
        Checks if func prints content.
        """
        self.assertEqual(self.redirect_stdout(func), content, msg)

    def redirect_stdout(self, func: Callable) -> str:
        """
        Redirect stdout of func to str.
        """
        buffer = io.StringIO()

        sys.stdout = buffer

        func()
        print_output: str = buffer.getvalue()

        sys.stdout = sys.__stdout__

        return print_output

    def mock_cmd_call(self, argv: list[str]) -> Callable:
        """
        Mocks a command line call to the jspsych command.
        """

        def func() -> None:
            argv.insert(0, "jspsych")
            with patch.object(sys, "argv", argv):
                management.exec_from_cmd()

        return func


if __name__ == "__main__":
    unittest.main()
