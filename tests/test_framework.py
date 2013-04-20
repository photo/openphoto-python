import unittest
import logging
import openphoto
import test_base

class TestFramework(test_base.TestBase):
    testcase_name = "framework"

    def setUp(self):
        """Override the default setUp, since we don't need a populated database"""
        logging.info("\nRunning %s..." % self.id())

    def create_client_from_base(self, api_version):
        return openphoto.OpenPhoto(self.client._host,
                                   self.client._consumer_key,
                                   self.client._consumer_secret,
                                   self.client._token,
                                   self.client._token_secret,
                                   api_version=api_version)

    def test_api_version_zero(self):
        # API v0 has a special hello world message
        client = self.create_client_from_base(api_version=0)
        result = client.get("hello.json")
        self.assertEqual(result['message'], "Hello, world! This is version zero of the API!")
        self.assertEqual(result['result']['__route__'], "/v0/hello.json")

    def test_specified_api_version(self):
        # For all API versions >0, we get a generic hello world message
        for api_version in range(1, openphoto.LATEST_API_VERSION + 1):
            client = self.create_client_from_base(api_version=api_version)
            result = client.get("hello.json")
            self.assertEqual(result['message'], "Hello, world!")
            self.assertEqual(result['result']['__route__'], "/v%d/hello.json" % api_version)

    def test_unspecified_api_version(self):
        # If the API version is unspecified, we get a generic hello world message
        client = self.create_client_from_base(api_version=None)
        result = client.get("hello.json")
        self.assertEqual(result['message'], "Hello, world!")
        self.assertEqual(result['result']['__route__'], "/hello.json")

    def test_future_api_version(self):
        # If the API version is unsupported, we should get an error
        # (it's a ValueError, since the returned 404 HTML page is not valid JSON)
        client = self.create_client_from_base(api_version=openphoto.LATEST_API_VERSION + 1)
        with self.assertRaises(ValueError):
            client.get("hello.json")
