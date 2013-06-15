from __future__ import unicode_literals
import json
import httpretty
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import openphoto

class TestHttp(unittest.TestCase):
    TEST_HOST = "test.example.com"
    TEST_ENDPOINT = "test.json"
    TEST_URI = "http://%s/%s" % (TEST_HOST, TEST_ENDPOINT)
    TEST_DATA = {"message": "Test Message",
                 "code": 200,
                 "result": "Test Result"}

    def setUp(self):
        self.client = openphoto.OpenPhoto(host=self.TEST_HOST,
                                          consumer_key="dummy",
                                          consumer_secret="dummy",
                                          token="dummy",
                                          token_secret="dummy")

    def _register_uri(self, method, uri=TEST_URI, data=TEST_DATA, **kwds):
        """Convenience wrapper around httpretty.register_uri"""
        body = json.dumps(data)
        httpretty.register_uri(method, uri=uri, body=body, **kwds)

    @staticmethod
    def _last_request():
        """This is a temporary measure until httpretty PR#59 is merged"""
        return httpretty.httpretty.last_request

    def test_attributes(self):
        self.assertEqual(self.client.host, self.TEST_HOST)
        self.assertEqual(self.client.config.host, self.TEST_HOST)

    @httpretty.activate
    def test_get_with_parameters(self):
        self._register_uri(httpretty.GET)
        response = self.client.get(self.TEST_ENDPOINT,
                                   foo="bar", spam="eggs")
        self.assertIn("OAuth", self._last_request().headers["authorization"])
        self.assertEqual(self._last_request().querystring["foo"], ["bar"])
        self.assertEqual(self._last_request().querystring["spam"], ["eggs"])
        self.assertEqual(response, self.TEST_DATA)
        self.assertEqual(self.client.last_url, self.TEST_URI)
        self.assertEqual(self.client.last_params, {"foo": "bar", "spam": "eggs"})
        self.assertEqual(self.client.last_response.json(), self.TEST_DATA)

    @httpretty.activate
    def test_post_with_parameters(self):
        self._register_uri(httpretty.POST)
        response = self.client.post(self.TEST_ENDPOINT,
                                   foo="bar", spam="eggs")
        self.assertEqual(self._last_request().body, "foo=bar&spam=eggs")
        self.assertEqual(response, self.TEST_DATA)
        self.assertEqual(self.client.last_url, self.TEST_URI)
        self.assertEqual(self.client.last_params, {"foo": "bar", "spam": "eggs"})
        self.assertEqual(self.client.last_response.json(), self.TEST_DATA)

    @httpretty.activate
    def test_get_without_oauth(self):
        self.client = openphoto.OpenPhoto(host=self.TEST_HOST)
        self._register_uri(httpretty.GET)
        response = self.client.get(self.TEST_ENDPOINT)
        self.assertNotIn("authorization", self._last_request().headers)
        self.assertEqual(response, self.TEST_DATA)

    @httpretty.activate
    def test_post_without_oauth_raises_exception(self):
        self.client = openphoto.OpenPhoto(host=self.TEST_HOST)
        self._register_uri(httpretty.POST)
        with self.assertRaises(openphoto.OpenPhotoError):
            self.client.post(self.TEST_ENDPOINT)

    @httpretty.activate
    def test_get_without_response_processing(self):
        self._register_uri(httpretty.GET)
        response = self.client.get(self.TEST_ENDPOINT, process_response=False)
        self.assertEqual(response, json.dumps(self.TEST_DATA))

    @httpretty.activate
    def test_post_without_response_processing(self):
        self._register_uri(httpretty.POST)
        response = self.client.post(self.TEST_ENDPOINT, process_response=False)
        self.assertEqual(response, json.dumps(self.TEST_DATA))

    @httpretty.activate
    def test_get_parameter_processing(self):
        self._register_uri(httpretty.GET)
        photo = openphoto.objects.Photo(None, {"id": "photo_id"})
        album = openphoto.objects.Album(None, {"id": "album_id"})
        tag = openphoto.objects.Tag(None, {"id": "tag_id"})
        response = self.client.get(self.TEST_ENDPOINT,
                                   photo=photo, album=album, tag=tag,
                                   list_=[photo, album, tag],
                                   boolean=True,
                                   unicode_="\xfcmlaut")
        params=self._last_request().querystring
        self.assertEqual(params["photo"], ["photo_id"])
        self.assertEqual(params["album"], ["album_id"])
        self.assertEqual(params["tag"], ["tag_id"])
        self.assertEqual(params["list_"], ["photo_id,album_id,tag_id"])
        self.assertEqual(params["boolean"], ["1"])
        self.assertEqual(params["unicode_"], ["\xc3\xbcmlaut"])
