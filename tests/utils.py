import os
import filecmp
import io
import sys
from typing import Callable
import unittest

class ExtendedTestCase(unittest.TestCase):
    def assertPrints(self, func: Callable, content: str, msg: str = "") -> None:
        """
        Checks if func prints content.
        """
        self.assertEqual(self.redirect_stdout(func), content, msg)

    def assertPrintBeginsWith(self, func: Callable, content: str) -> None:
        stdout: str = self.redirect_stdout(func)
        self.assertTrue(stdout.startswith(content))

    def assertHasSameStructure(self, target: str, base: str) -> None:
        """
        Checks if target directory has the same structure as base directory.
        """
        self.assertTrue(self.has_same_structure(target, base))

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

    def has_same_structure(self, target: str, base: str) -> bool:
        cmp = filecmp.dircmp(target, base)
        if cmp.left_only or cmp.right_only:
            return False

        for common_dir in cmp.common_dirs:
            child_dir_1 = os.path.join(target, common_dir)
            child_dir_2 = os.path.join(base, common_dir)
            if not self.has_same_structure(child_dir_1, child_dir_2):
                return False

        return True
