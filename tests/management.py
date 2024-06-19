import os
import shutil
import sys
import tempfile

from typing import Callable

import unittest
from unittest.mock import patch

from jspsych_plus.management import management
from utils import ExtendedTestCase


class TestManagement(ExtendedTestCase):
    def test_help(self):
        """
        Tests whether these commands correctly prints the help info:
        - jspsych help
        - jspsych -h
        - jspsych
        - jspsych invalid-command
        """
        help_msg: str = self.redirect_stdout(management.print_help)

        self.assertPrints(self.mock_cmd_call(["help"]), help_msg)
        self.assertPrints(self.mock_cmd_call(["-h"]), help_msg)
        self.assertPrints(self.mock_cmd_call([]), help_msg)
        self.assertPrints(self.mock_cmd_call(["invalid-command"]), help_msg)

    def test_new_project(self):
        """
        Tests whether these commands would create projects properly:
        - jspsych new: creates a project named "jspsych-project"
        - jspsych new test1: creates a project named "test1"
        - jspsych new test2 [relative-path]: creates project in the right spot
        - jspsych new test3 [absolute-path]: creates project in the right spot
        - jspsych new test4 [nonempty-path]: does not create a project
        """
        test_dir: str = tempfile.mkdtemp(
            dir=os.path.dirname(__file__),
            prefix="new-project-test",
        )

        template_dir: str = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "jspsych_plus",
                "template",
            )
        )

        cwd: str = os.getcwd()
        os.chdir(test_dir)

        try:
            self.mock_cmd_call(["new"])()
            self.assertHasSameStructure(
                os.path.join(test_dir, "jspsych-project"),
                template_dir,
            )

            self.mock_cmd_call(["new", "test1"])()
            self.assertHasSameStructure(
                os.path.join(test_dir, "test1"),
                template_dir,
            )

            self.mock_cmd_call(["new", "test2", "./proj/target"])()
            self.assertHasSameStructure(
                os.path.join(test_dir, "proj/target", "test2"),
                template_dir,
            )

            abs_path = os.path.join(test_dir, "abs_path")
            self.mock_cmd_call(["new", "test3", abs_path])()
            self.assertHasSameStructure(
                os.path.join(abs_path, "test3"),
                template_dir,
            )

            # No project should be created as <test_dir>/abs_path is not empty
            self.assertPrintBeginsWith(
                self.mock_cmd_call(["new", "abs_path", test_dir]),
                "Cannot create project",
            )
        finally:
            os.chdir(cwd)
            shutil.rmtree(test_dir)

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
