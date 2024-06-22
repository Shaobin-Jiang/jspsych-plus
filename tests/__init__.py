import unittest
from management import TestManagement
from api import TestApi

if __name__ == "__main__":
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    def add_test(case: type[unittest.TestCase]) -> None:
        suite.addTests(loader.loadTestsFromTestCase(case))

    add_test(TestManagement)
    add_test(TestApi)

    unittest.TextTestRunner().run(suite)
