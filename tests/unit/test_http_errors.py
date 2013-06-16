from __future__ import unicode_literals
import json
import httpretty
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import openphoto
from tests.unit.test_http import TestHttp

class TestHttpErrors(TestHttp):
    def _register_uri(self, method, uri=TestHttp.TEST_URI,
                      data=None, body=None, status=200, **kwds):
        """Convenience wrapper around httpretty.register_uri"""
        if data is None:
            data = self.TEST_DATA
            # Set the JSON return code to match the HTTP status
            data["code"] = status
        if body is None:
            body = json.dumps(data)
        httpretty.register_uri(method, uri=uri, body=body, status=status,
                               **kwds)

    @httpretty.activate
    def test_get_with_error_status_raises_openphoto_exception(self):
        self._register_uri(httpretty.GET, status=500)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.get(self.TEST_ENDPOINT)

    @httpretty.activate
    def test_post_with_error_status_raises_openphoto_exception(self):
        self._register_uri(httpretty.POST, status=500)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.post(self.TEST_ENDPOINT)

    # TODO: 404 status should raise 404 error, even if JSON is valid
    @unittest.expectedFailure
    @httpretty.activate
    def test_get_with_404_status_raises_404_exception(self):
        self._register_uri(httpretty.GET, status=404)
        with self.assertRaises(openphoto.OpenPhoto404Error):
            response = self.client.get(self.TEST_ENDPOINT)

    # TODO: 404 status should raise 404 error, even if JSON is valid
    @unittest.expectedFailure
    @httpretty.activate
    def test_post_with_404_status_raises_404_exception(self):
        self._register_uri(httpretty.POST, status=404)
        with self.assertRaises(openphoto.OpenPhoto404Error):
            response = self.client.post(self.TEST_ENDPOINT)

    @httpretty.activate
    def test_get_with_invalid_json_raises_exception(self):
        self._register_uri(httpretty.GET, body="Invalid JSON")
        with self.assertRaises(ValueError):
            self.client.get(self.TEST_ENDPOINT)

    @httpretty.activate
    def test_post_with_invalid_json_raises_exception(self):
        self._register_uri(httpretty.POST, body="Invalid JSON")
        with self.assertRaises(ValueError):
            self.client.post(self.TEST_ENDPOINT)

    @httpretty.activate
    def test_get_with_error_status_and_invalid_json_raises_openphoto_exception(self):
        self._register_uri(httpretty.GET, body="Invalid JSON", status=500)
        with self.assertRaises(openphoto.OpenPhotoError):
            response = self.client.get(self.TEST_ENDPOINT)

    @httpretty.activate
    def test_post_with_error_status_and_invalid_json_raises_openphoto_exception(self):
        self._register_uri(httpretty.POST, body="Invalid JSON", status=500)
        with self.assertRaises(openphoto.OpenPhotoError):
            response = self.client.post(self.TEST_ENDPOINT)

    @httpretty.activate
    def test_get_with_404_status_and_invalid_json_raises_404_exception(self):
        self._register_uri(httpretty.GET, body="Invalid JSON", status=404)
        with self.assertRaises(openphoto.OpenPhoto404Error):
            response = self.client.get(self.TEST_ENDPOINT)

    @httpretty.activate
    def test_post_with_404_status_and_invalid_json_raises_404_exception(self):
        self._register_uri(httpretty.POST, body="Invalid JSON", status=404)
        with self.assertRaises(openphoto.OpenPhoto404Error):
            response = self.client.post(self.TEST_ENDPOINT)

    @httpretty.activate
    def test_get_with_duplicate_status_raises_duplicate_exception(self):
        data = {"message": "This photo already exists", "code": 409}
        self._register_uri(httpretty.GET, data=data, status=409)
        with self.assertRaises(openphoto.OpenPhotoDuplicateError):
            response = self.client.get(self.TEST_ENDPOINT)

    @httpretty.activate
    def test_post_with_duplicate_status_raises_duplicate_exception(self):
        data = {"message": "This photo already exists", "code": 409}
        self._register_uri(httpretty.POST, data=data, status=409)
        with self.assertRaises(openphoto.OpenPhotoDuplicateError):
            response = self.client.post(self.TEST_ENDPOINT)

    # TODO: Status code mismatch should raise an exception
    @unittest.expectedFailure
    @httpretty.activate
    def test_get_with_status_code_mismatch_raises_openphoto_exception(self):
        data = {"message": "Test Message", "code": 200}
        self._register_uri(httpretty.GET, data=data, status=202)
        with self.assertRaises(openphoto.OpenPhotoError):
            response = self.client.get(self.TEST_ENDPOINT)

    # TODO: Status code mismatch should raise an exception
    @unittest.expectedFailure
    @httpretty.activate
    def test_post_with_status_code_mismatch_raises_openphoto_exception(self):
        data = {"message": "Test Message", "code": 200}
        self._register_uri(httpretty.POST, data=data, status=202)
        with self.assertRaises(openphoto.OpenPhotoError):
            response = self.client.post(self.TEST_ENDPOINT)

