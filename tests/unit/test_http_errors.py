from __future__ import unicode_literals
import json
import httpretty
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import openphoto

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
        self.client = openphoto.OpenPhoto(host=self.test_host,
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
    def test_get_with_error_status(self):
        """
        Check that an error status causes the get method
        to raise an exception
        """
        self._register_uri(httpretty.GET, status=500)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.get(self.test_endpoint)

    @httpretty.activate
    def test_post_with_error_status(self):
        """
        Check that an error status causes the post method
        to raise an exception
        """
        self._register_uri(httpretty.POST, status=500)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.post(self.test_endpoint)

    # TODO: 404 status should raise 404 error, even if JSON is valid
    @unittest.expectedFailure
    @httpretty.activate
    def test_get_with_404_status(self):
        """
        Check that a 404 status causes the get method
        to raise a 404 exception
        """
        self._register_uri(httpretty.GET, status=404)
        with self.assertRaises(openphoto.OpenPhoto404Error):
            self.client.get(self.test_endpoint)

    # TODO: 404 status should raise 404 error, even if JSON is valid
    @unittest.expectedFailure
    @httpretty.activate
    def test_post_with_404_status(self):
        """
        Check that a 404 status causes the post method
        to raise a 404 exception
        """
        self._register_uri(httpretty.POST, status=404)
        with self.assertRaises(openphoto.OpenPhoto404Error):
            self.client.post(self.test_endpoint)

    @httpretty.activate
    def test_get_with_invalid_json(self):
        """
        Check that invalid JSON causes the get method to
        raise an exception
        """
        self._register_uri(httpretty.GET, body="Invalid JSON")
        with self.assertRaises(ValueError):
            self.client.get(self.test_endpoint)

    @httpretty.activate
    def test_post_with_invalid_json(self):
        """
        Check that invalid JSON causes the post method to
        raise an exception
        """
        self._register_uri(httpretty.POST, body="Invalid JSON")
        with self.assertRaises(ValueError):
            self.client.post(self.test_endpoint)

    @httpretty.activate
    def test_get_with_error_status_and_invalid_json(self):
        """
        Check that invalid JSON causes the get method to raise an exception,
        even with an error status is returned
        """
        self._register_uri(httpretty.GET, body="Invalid JSON", status=500)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.get(self.test_endpoint)

    @httpretty.activate
    def test_post_with_error_status_and_invalid_json(self):
        """
        Check that invalid JSON causes the post method to raise an exception,
        even with an error status is returned
        """
        self._register_uri(httpretty.POST, body="Invalid JSON", status=500)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.post(self.test_endpoint)

    @httpretty.activate
    def test_get_with_404_status_and_invalid_json(self):
        """
        Check that invalid JSON causes the get method to raise an exception,
        even with a 404 status is returned
        """
        self._register_uri(httpretty.GET, body="Invalid JSON", status=404)
        with self.assertRaises(openphoto.OpenPhoto404Error):
            self.client.get(self.test_endpoint)

    @httpretty.activate
    def test_post_with_404_status_and_invalid_json(self):
        """
        Check that invalid JSON causes the post method to raise an exception,
        even with a 404 status is returned
        """
        self._register_uri(httpretty.POST, body="Invalid JSON", status=404)
        with self.assertRaises(openphoto.OpenPhoto404Error):
            self.client.post(self.test_endpoint)

    @httpretty.activate
    def test_get_with_duplicate_status(self):
        """
        Check that a get with a duplicate status
        raises a duplicate exception
        """
        data = {"message": "This photo already exists", "code": 409}
        self._register_uri(httpretty.GET, data=data, status=409)
        with self.assertRaises(openphoto.OpenPhotoDuplicateError):
            self.client.get(self.test_endpoint)

    @httpretty.activate
    def test_post_with_duplicate_status(self):
        """
        Check that a post with a duplicate status
        raises a duplicate exception
        """
        data = {"message": "This photo already exists", "code": 409}
        self._register_uri(httpretty.POST, data=data, status=409)
        with self.assertRaises(openphoto.OpenPhotoDuplicateError):
            self.client.post(self.test_endpoint)

    # TODO: Status code mismatch should raise an exception
    @unittest.expectedFailure
    @httpretty.activate
    def test_get_with_status_code_mismatch(self):
        """
        Check that an exception is raised if a get returns a
        status code that doesn't match the JSON code
        """
        data = {"message": "Test Message", "code": 200}
        self._register_uri(httpretty.GET, data=data, status=202)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.get(self.test_endpoint)

    # TODO: Status code mismatch should raise an exception
    @unittest.expectedFailure
    @httpretty.activate
    def test_post_with_status_code_mismatch(self):
        """
        Check that an exception is raised if a post returns a
        status code that doesn't match the JSON code
        """
        data = {"message": "Test Message", "code": 200}
        self._register_uri(httpretty.POST, data=data, status=202)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.post(self.test_endpoint)

