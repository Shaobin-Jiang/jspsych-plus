import unittest

from jspsych_plus.jspsych import Jspsych
from starlette.testclient import TestClient

from utils import ExtendedTestCase


class TestEndpoint(ExtendedTestCase):
    def test_static(self):
        """
        Tests whether static files are fetched properly.
        """
        jspsych = Jspsych()
        client = TestClient(jspsych)

        self.assertEqual(client.get("/").status_code, 200)
        self.assertEqual(client.get("/index").status_code, 200)
        self.assertEqual(client.get("/index.html").status_code, 200)

        self.assertEqual(client.get("/scripts/main.js").status_code, 200)
        self.assertEqual(client.get("/123").status_code, 404)


if __name__ == "__main__":
    unittest.main()
