from __future__ import unicode_literals
import os
import json
import httpretty
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import openphoto

class TestHttp(unittest.TestCase):
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
    test_file = os.path.join("tests", "unit", "data", "test_file.txt")


    def setUp(self):
        self.client = openphoto.OpenPhoto(host=self.test_host,
                                          **self.test_oauth)

    def _register_uri(self, method, uri=test_uri, data=None, body=None,
                      **kwds):
        """Convenience wrapper around httpretty.register_uri"""
        if data is None:
            data = self.test_data
        if body is None:
            body = json.dumps(data)
        httpretty.register_uri(method, uri=uri, body=body, **kwds)

    @staticmethod
    def _last_request():
        """This is a temporary measure until httpretty PR#59 is merged"""
        return httpretty.httpretty.last_request

    def test_attributes(self):
        """Check that the host attribute has been set correctly"""
        self.assertEqual(self.client.host, self.test_host)
        self.assertEqual(self.client.config.host, self.test_host)

    @httpretty.activate
    def test_get_with_parameters(self):
        """Check that the get method accepts parameters correctly"""
        self._register_uri(httpretty.GET)
        response = self.client.get(self.test_endpoint,
                                   foo="bar", spam="eggs")
        self.assertIn("OAuth", self._last_request().headers["authorization"])
        self.assertEqual(self._last_request().querystring["foo"], ["bar"])
        self.assertEqual(self._last_request().querystring["spam"], ["eggs"])
        self.assertEqual(response, self.test_data)
        self.assertEqual(self.client.last_url, self.test_uri)
        self.assertEqual(self.client.last_params, {"foo": "bar",
                                                   "spam": "eggs"})
        self.assertEqual(self.client.last_response.json(), self.test_data)

    @httpretty.activate
    def test_post_with_parameters(self):
        """Check that the post method accepts parameters correctly"""
        self._register_uri(httpretty.POST)
        response = self.client.post(self.test_endpoint,
                                   foo="bar", spam="eggs")
        self.assertEqual(self._last_request().body, "foo=bar&spam=eggs")
        self.assertEqual(response, self.test_data)
        self.assertEqual(self.client.last_url, self.test_uri)
        self.assertEqual(self.client.last_params, {"foo": "bar",
                                                   "spam": "eggs"})
        self.assertEqual(self.client.last_response.json(), self.test_data)

    @httpretty.activate
    def test_get_without_oauth(self):
        """Check that the get method works without OAuth parameters"""
        self.client = openphoto.OpenPhoto(host=self.test_host)
        self._register_uri(httpretty.GET)
        response = self.client.get(self.test_endpoint)
        self.assertNotIn("authorization", self._last_request().headers)
        self.assertEqual(response, self.test_data)

    @httpretty.activate
    def test_post_without_oauth(self):
        """Check that the post method fails without OAuth parameters"""
        self.client = openphoto.OpenPhoto(host=self.test_host)
        self._register_uri(httpretty.POST)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.post(self.test_endpoint)

    @httpretty.activate
    def test_get_without_response_processing(self):
        """Check that the get method works with response processing disabled"""
        self._register_uri(httpretty.GET)
        response = self.client.get(self.test_endpoint, process_response=False)
        self.assertEqual(response, json.dumps(self.test_data))

    @httpretty.activate
    def test_post_without_response_processing(self):
        """Check that the post method works with response processing disabled"""
        self._register_uri(httpretty.POST)
        response = self.client.post(self.test_endpoint, process_response=False)
        self.assertEqual(response, json.dumps(self.test_data))

    @httpretty.activate
    def test_get_parameter_processing(self):
        """Check that the parameter processing function is working"""
        self._register_uri(httpretty.GET)
        photo = openphoto.objects.Photo(None, {"id": "photo_id"})
        album = openphoto.objects.Album(None, {"id": "album_id"})
        tag = openphoto.objects.Tag(None, {"id": "tag_id"})
        self.client.get(self.test_endpoint,
                        photo=photo, album=album, tag=tag,
                        list_=[photo, album, tag],
                        boolean=True,
                        unicode_="\xfcmlaut")
        params = self._last_request().querystring
        self.assertEqual(params["photo"], ["photo_id"])
        self.assertEqual(params["album"], ["album_id"])
        self.assertEqual(params["tag"], ["tag_id"])
        self.assertEqual(params["list_"], ["photo_id,album_id,tag_id"])
        self.assertEqual(params["boolean"], ["1"])
        self.assertEqual(params["unicode_"], ["\xc3\xbcmlaut"])

    @httpretty.activate
    def test_get_with_api_version(self):
        """Check that an API version can be specified for the get method"""
        self.client = openphoto.OpenPhoto(host=self.test_host, api_version=1)
        self._register_uri(httpretty.GET,
                           uri="http://%s/v1/%s" % (self.test_host,
                                                    self.test_endpoint))
        self.client.get(self.test_endpoint)

    @httpretty.activate
    def test_post_with_api_version(self):
        """Check that an API version can be specified for the post method"""
        self.client = openphoto.OpenPhoto(host=self.test_host, api_version=1,
                                          **self.test_oauth)
        self._register_uri(httpretty.POST,
                           uri="http://%s/v1/%s" % (self.test_host,
                                                    self.test_endpoint))
        self.client.post(self.test_endpoint)

    @httpretty.activate
    def test_post_file(self):
        """Check that a file can be posted"""
        self._register_uri(httpretty.POST)
        with open(self.test_file, 'rb') as in_file:
            response = self.client.post(self.test_endpoint,
                                        files={"file": in_file})
        self.assertEqual(response, self.test_data)
        body = self._last_request().body
        self.assertIn("Content-Disposition: form-data; "+
                      "name=\"file\"; filename=\"test_file.txt\"", body)
        self.assertIn("Test File", body)


    @httpretty.activate
    def test_post_file_parameters_are_sent_as_querystring(self):
        """
        Check that parameters are send as a query string
        when a file is posted
        """
        self._register_uri(httpretty.POST)
        with open(self.test_file, 'rb') as in_file:
            response = self.client.post(self.test_endpoint, foo="bar",
                                        files={"file": in_file})
        self.assertEqual(response, self.test_data)
        self.assertEqual(self._last_request().querystring["foo"], ["bar"])
