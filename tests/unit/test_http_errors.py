from __future__ import unicode_literals
import json
import httpretty
from httpretty import GET, POST
from ddt import ddt, data

try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

from test_http import GetOrPost
import trovebox

@ddt
class TestHttpErrors(unittest.TestCase):
    test_host = "test.example.com"
    test_endpoint = "test.json"
    test_uri = "http://%s/%s" % (test_host, test_endpoint)
    test_data = {"message": "Test Message",
                 "code": 200,
                 "result": "Test Result"}
    test_oauth = {"consumer_key": "dummy",
                  "consumer_secret": "dummy",
                  "token": "dummy",
                  "token_secret": "dummy"}

    def setUp(self):
        self.client = trovebox.Trovebox(host=self.test_host,
                                        **self.test_oauth)

    def _register_uri(self, method, uri=test_uri,
                      data=None, body=None, status=200, **kwds):
        """Convenience wrapper around httpretty.register_uri"""
        if data is None:
            data = self.test_data
            # Set the JSON return code to match the HTTP status
            data["code"] = status
        if body is None:
            body = json.dumps(data)
        httpretty.register_uri(method, uri=uri, body=body, status=status,
                               **kwds)

    @httpretty.activate
    @data(GET, POST)
    def test_error_status(self, method):
        """
        Check that an error status causes the get/post methods
        to raise an exception
        """
        self._register_uri(method, status=500)
        with self.assertRaises(trovebox.TroveboxError):
            GetOrPost(self.client, method).call(self.test_endpoint)

    @httpretty.activate
    @data(GET, POST)
    def test_404_status(self, method):
        """
        Check that a 404 status causes the get/post methods
        to raise a 404 exception
        """
        self._register_uri(method, status=404)
        with self.assertRaises(trovebox.Trovebox404Error):
            GetOrPost(self.client, method).call(self.test_endpoint)

    @httpretty.activate
    @data(GET, POST)
    def test_with_invalid_json(self, method):
        """
        Check that invalid JSON causes the get/post methods to
        raise an exception
        """
        self._register_uri(method, body="Invalid JSON")
        with self.assertRaises(ValueError):
            GetOrPost(self.client, method).call(self.test_endpoint)

    @httpretty.activate
    @data(GET, POST)
    def test_with_error_status_and_invalid_json(self, method):
        """
        Check that invalid JSON causes the get/post methods to raise
        an exception, even with an error status is returned
        """
        self._register_uri(method, body="Invalid JSON", status=500)
        with self.assertRaises(trovebox.TroveboxError):
            GetOrPost(self.client, method).call(self.test_endpoint)

    @httpretty.activate
    @data(GET, POST)
    def test_with_404_status_and_invalid_json(self, method):
        """
        Check that invalid JSON causes the get/post methods to raise
        an exception, even with a 404 status is returned
        """
        self._register_uri(method, body="Invalid JSON", status=404)
        with self.assertRaises(trovebox.Trovebox404Error):
            GetOrPost(self.client, method).call(self.test_endpoint)

    @httpretty.activate
    @data(GET, POST)
    def test_with_duplicate_status(self, method):
        """
        Check that a get/post with a duplicate status
        raises a duplicate exception
        """
        data = {"message": "This photo already exists", "code": 409}
        self._register_uri(method, data=data, status=409)
        with self.assertRaises(trovebox.TroveboxDuplicateError):
            GetOrPost(self.client, method).call(self.test_endpoint)

    @httpretty.activate
    @data(GET, POST)
    def test_with_status_code_mismatch(self, method):
        """
        Check that a mismatched HTTP status code still returns the
        JSON status code.
        """
        data = {"message": "Test Message", "code": 202}
        self._register_uri(method, data=data, status=200)
        response = GetOrPost(self.client, method).call(self.test_endpoint)
        self.assertEqual(response["code"], 202)

    @httpretty.activate
    @data(GET, POST)
    def test_http_error_with_no_response_processing(self, method):
        """
        Check that get/post methods work with response processing disabled
        when an HTTP error code is returned.
        """
        httpretty.register_uri(method, self.test_uri, status=500)
        with self.assertRaises(trovebox.TroveboxError):
            response = GetOrPost(self.client, method).call(self.test_endpoint,
                                                           process_response=False)

