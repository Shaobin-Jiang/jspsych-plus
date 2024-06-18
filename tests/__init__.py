import unittest
from management import TestManagement

if __name__ == "__main__":
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    def add_test(case: type[unittest.TestCase]) -> None:
        suite.addTests(loader.loadTestsFromTestCase(case))

    add_test(TestManagement)

    unittest.TextTestRunner().run(suite)
