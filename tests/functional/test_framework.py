import logging

import trovebox
from tests.functional import test_base

class TestFramework(test_base.TestBase):
    testcase_name = "framework"

    def setUp(self):
        """
        Override the default setUp, since we don't need a populated database
        """
        logging.info("\nRunning %s...", self.id())

    def test_api_version_zero(self):
        """
        API v0 has a special hello world message
        """
        client = trovebox.Trovebox(config_file=self.config_file)
        client.configure(api_version=0)
        result = client.get("hello.json")
        self.assertEqual(result['message'],
                         "Hello, world! This is version zero of the API!")
        self.assertEqual(result['result']['__route__'], "/v0/hello.json")

    def test_specified_api_version(self):
        """
        For all API versions >0, we get a generic hello world message
        """
        for api_version in range(1, test_base.get_test_server_api() + 1):
            client = trovebox.Trovebox(config_file=self.config_file)
            client.configure(api_version=api_version)
            result = client.get("hello.json")
            self.assertEqual(result['message'], "Hello, world!")
            self.assertEqual(result['result']['__route__'],
                             "/v%d/hello.json" % api_version)

    def test_unspecified_api_version(self):
        """
        If the API version is unspecified,
        we get a generic hello world message.
        """
        client = trovebox.Trovebox(config_file=self.config_file)
        result = client.get("hello.json")
        self.assertEqual(result['message'], "Hello, world!")
        self.assertEqual(result['result']['__route__'], "/hello.json")

    def test_future_api_version(self):
        """
        If the API version is unsupported, we should get an error
        (ValueError, since the returned 404 HTML page is not valid JSON)
        """
        version = trovebox.LATEST_API_VERSION + 1
        client = trovebox.Trovebox(config_file=self.config_file)
        client.configure(api_version=version)
        with self.assertRaises(trovebox.Trovebox404Error):
            client.get("hello.json")
