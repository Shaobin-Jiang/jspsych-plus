import asyncio
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

            asyncio.get_event_loop().run_until_complete(
                jspsych.var_pool.set("v1", 123)
            )
            self.assertDictEqual(socket_1.receive_json(), {"v1": 123})

            with client_2.websocket_connect(url) as socket_2:
                self.assertEqual(socket_2.receive_json()["v1"], 123)

                asyncio.get_event_loop().run_until_complete(
                    jspsych.var_pool.set("v2", "aaa")
                )
                self.assertDictEqual(socket_1.receive_json(), {"v2": "aaa"})
                self.assertDictEqual(socket_2.receive_json(), {"v2": "aaa"})

            # tests whether using a callable to modify a variable works
            asyncio.get_event_loop().run_until_complete(
                jspsych.var_pool.set("v3", [1])
            )
            socket_1.receive_json()

            asyncio.get_event_loop().run_until_complete(
                jspsych.var_pool.set("v3", func=lambda x: x.append(2))
            )
            self.assertDictEqual(socket_1.receive_json(), {"v3": [1, 2]})


if __name__ == "__main__":
    unittest.main()
