from tests import TestCase

from src.masonite.utils.str import (
    random_string,
    removeprefix,
    removesuffix,
    get_controller_name,
    add_query_params,
)

from tests.integrations.controllers.api.TestController import TestController


class TestStringsUtils(TestCase):
    def test_random_string(self):
        self.assertEqual(len(random_string()), 4)
        self.assertEqual(len(random_string(10)), 10)
        self.assertIsInstance(random_string(5), str)
        self.assertNotEqual(random_string(), random_string())

    def test_removesuffix(self):
        self.assertEqual(removesuffix("test.com", ".com"), "test")
        self.assertEqual(removesuffix("test", ".com"), "test")

    def test_removeprefix(self):
        self.assertEqual(removeprefix("AppEvent", "App"), "Event")
        self.assertEqual(removeprefix("Event", "App"), "Event")

    def test_get_controller_name(self):
        self.assertEqual(
            get_controller_name("WelcomeController@show"), "WelcomeController@show"
        )
        self.assertEqual(get_controller_name(TestController), "TestController@__call__")
        self.assertEqual(
            get_controller_name(TestController.show), "TestController@show"
        )
        controller = TestController()
        self.assertEqual(get_controller_name(controller), "TestController@__call__")

    def test_add_query_params_not_break_urls(self):
        test_urls = [
            "https://example.com/c/pay/cs_teAIXs#fid2cGd2ZndsdXFsamtQa2x0cGBrYHZ2QGtkZ2lgYSc%2FY2RpdmApJ2R1bE5gfCc%2FJ3VuWnFgdnFac2FiQF9fbWppSTxkc01tcWRTMzA9fVdgNTVHfXJWcGhUPCcpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl",
            "https://example.com?a=b",
            "https://example.com/",
        ]

        for url in test_urls:
            self.assertEqual(url, add_query_params(url, {}))

    def test_add_query_params_add_params(self):
        test_urls = [
            {
                "input": "https://example.com/c/pay/cs_teAIXs#fidx22wwe",
                "result": "https://example.com/c/pay/cs_teAIXs?test_param=1&test_param_2=2#fidx22wwe",
            },
            {
                "input": "https://example.com?a=b&",
                "result": "https://example.com?a=b&test_param=1&test_param_2=2",
            },
            {
                "input": "https://example.com",
                "result": "https://example.com?test_param=1&test_param_2=2",
            },
            {
                "input": "https://example.com/",
                "result": "https://example.com/?test_param=1&test_param_2=2",
            },
        ]

        for url in test_urls:
            self.assertEqual(
                url["result"],
                add_query_params(url["input"], {"test_param": 1, "test_param_2": 2}),
            )
