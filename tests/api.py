import asyncio
import json
import os
import unittest

from jspsych_plus.applications.jspsych import Jspsych
from utils import ExtendedTestCase
from starlette.testclient import TestClient


class TestApi(ExtendedTestCase):
    def test_channel_server_change(self):
        """
        Tests whether server side changes to the variable pool will be received
        by the clients.
        """
        jspsych = Jspsych()
        url: str = "/_channel"

        client_1 = TestClient(jspsych)
        client_2 = TestClient(jspsych)

        with client_1.websocket_connect(url) as socket_1:
            # the channel forwards the current variable pool
            socket_1.receive_json()

            asyncio.get_event_loop().run_until_complete(jspsych.var_pool.set("v1", 123))
            self.assertDictEqual(socket_1.receive_json(), {"v1": 123})

            with client_2.websocket_connect(url) as socket_2:
                self.assertEqual(socket_2.receive_json()["v1"], 123)

                asyncio.get_event_loop().run_until_complete(
                    jspsych.var_pool.set("v2", "aaa")
                )
                self.assertDictEqual(socket_1.receive_json(), {"v2": "aaa"})
                self.assertDictEqual(socket_2.receive_json(), {"v2": "aaa"})

            # tests whether using a callable to modify a variable works
            asyncio.get_event_loop().run_until_complete(jspsych.var_pool.set("v3", [1]))
            socket_1.receive_json()

            asyncio.get_event_loop().run_until_complete(
                jspsych.var_pool.set("v3", func=lambda x: x.append(2))
            )
            self.assertDictEqual(socket_1.receive_json(), {"v3": [1, 2]})

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

    def test_fs(self):
        """
        Tests various features of the "file system" works properly.
        """
        jspsych = Jspsych()
        client = TestClient(jspsych)

        jspsych.data_dir = jspsych.static_dir

        # The query param is actually ?path=1/2 here, but in a normal url, the
        # slash should be converted to %2F
        response_1 = client.get("/fs/tree?path=1%2F2")
        self.assertEqual(response_1.status_code, 403)
        self.assertEqual(response_1.content.decode(), "Non existent path")

        response_2 = client.get("/fs/tree?path=%2F")
        self.assertEqual(response_2.status_code, 200)

        correct_result = []
        for root, dirs, files in os.walk(jspsych.data_dir):
            correct_result.append([root, dirs, files])

        self.assertEqual(
            response_2.content.decode().replace('\\"', '"'),
            f'"{json.dumps(correct_result)}"',
        )

        response_3 = client.get("/fs/tree?path=..")
        self.assertEqual(response_3.status_code, 403)
        self.assertEqual(response_3.content.decode(), "Permission denied")

        with open(os.path.join(jspsych.data_dir, "index.html"), mode="r") as fid:
            content = fid.read()
            response_4 = client.get("/fs/read?path=%2Findex.html")
            self.assertEqual(response_4.content.decode(), content)

        written_content: str = "Hello world"
        client.post(
            "/fs/write",
            content=json.dumps({"path": "temp", "content": written_content}),
        )
        written_file: str = os.path.join(jspsych.data_dir, "temp")
        try:
            self.assertTrue(os.path.exists(written_file))
            self.assertTrue(os.path.isfile(written_file))
            with open(written_file, mode="r") as fid:
                self.assertEqual(fid.read(), written_content)
        finally:
            os.remove(written_file)


if __name__ == "__main__":
    unittest.main()
