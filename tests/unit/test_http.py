from __future__ import unicode_literals
import os
import json
import mock
import httpretty
from httpretty import GET, POST
from ddt import ddt, data
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import trovebox

class GetOrPost(object):
    """Helper class to call the correct (GET/POST) method"""
    def __init__(self, client, method):
        self.client = client
        self.method = method

    def call(self, *args, **kwds):
        if self.method == GET:
            return self.client.get(*args, **kwds)
        elif self.method == POST:
            return self.client.post(*args, **kwds)
        else:
            raise ValueError("unknown method: %s" % self.method)

@ddt
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
        self.client = trovebox.Trovebox(host=self.test_host,
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
        self.assertEqual(self.client.auth.host, self.test_host)

    @httpretty.activate
    @data(GET, POST)
    def test_http_scheme(self, method):
        """Check that we can access hosts starting with 'http://'"""
        self._register_uri(method,
                           uri="http://test.example.com/%s" % self.test_endpoint)

        self.client = trovebox.Trovebox(host="http://test.example.com",
                                        **self.test_oauth)
        response = GetOrPost(self.client, method).call(self.test_endpoint)
        self.assertIn("OAuth", self._last_request().headers["authorization"])
        self.assertEqual(response, self.test_data)
        self.assertEqual(self.client.last_url,
                         "http://test.example.com/%s" % self.test_endpoint)
        self.assertEqual(self.client.last_response.json(), self.test_data)

    @httpretty.activate
    @data(GET, POST)
    def test_no_scheme(self, method):
        """Check that we can access hosts without a 'http://' prefix"""
        self._register_uri(method,
                           uri="http://test.example.com/%s" % self.test_endpoint)

        self.client = trovebox.Trovebox(host="test.example.com",
                                        **self.test_oauth)
        response = GetOrPost(self.client, method).call(self.test_endpoint)
        self.assertIn("OAuth", self._last_request().headers["authorization"])
        self.assertEqual(response, self.test_data)
        self.assertEqual(self.client.last_url,
                         "http://test.example.com/%s" % self.test_endpoint)
        self.assertEqual(self.client.last_response.json(), self.test_data)

    @httpretty.activate
    @data(GET, POST)
    def test_https_scheme(self, method):
        """Check that we can access hosts starting with 'https://'"""
        self._register_uri(method,
                           uri="https://test.example.com/%s" % self.test_endpoint)

        self.client = trovebox.Trovebox(host="https://test.example.com",
                                        **self.test_oauth)
        response = GetOrPost(self.client, method).call(self.test_endpoint)
        self.assertIn("OAuth", self._last_request().headers["authorization"])
        self.assertEqual(response, self.test_data)
        self.assertEqual(self.client.last_url,
                         "https://test.example.com/%s" % self.test_endpoint)
        self.assertEqual(self.client.last_response.json(), self.test_data)

    @httpretty.activate
    @data(GET, POST)
    def test_endpoint_leading_slash(self, method):
        """Check that an endpoint with a leading slash is constructed correctly"""
        self._register_uri(method,
                           uri="http://test.example.com/%s" % self.test_endpoint)

        self.client = trovebox.Trovebox(host="http://test.example.com",
                                        **self.test_oauth)
        response = GetOrPost(self.client, method).call("/" + self.test_endpoint)
        self.assertIn("OAuth", self._last_request().headers["authorization"])
        self.assertEqual(response, self.test_data)
        self.assertEqual(self.client.last_url,
                         "http://test.example.com/%s" % self.test_endpoint)
        self.assertEqual(self.client.last_response.json(), self.test_data)

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
        self.assertEqual(self.client.last_params, {"foo": b"bar",
                                                   "spam": b"eggs"})
        self.assertEqual(self.client.last_response.json(), self.test_data)

    @httpretty.activate
    def test_post_with_parameters(self):
        """Check that the post method accepts parameters correctly"""
        self._register_uri(httpretty.POST)
        response = self.client.post(self.test_endpoint,
                                   foo="bar", spam="eggs")
        self.assertIn(b"spam=eggs", self._last_request().body)
        self.assertIn(b"foo=bar", self._last_request().body)
        self.assertEqual(response, self.test_data)
        self.assertEqual(self.client.last_url, self.test_uri)
        self.assertEqual(self.client.last_params, {"foo": b"bar",
                                                   "spam": b"eggs"})
        self.assertEqual(self.client.last_response.json(), self.test_data)

    @httpretty.activate
    def test_get_without_oauth(self):
        """Check that the get method works without OAuth parameters"""
        self.client = trovebox.Trovebox(host=self.test_host)
        self._register_uri(httpretty.GET)
        response = self.client.get(self.test_endpoint)
        self.assertNotIn("authorization", self._last_request().headers)
        self.assertEqual(response, self.test_data)

    @httpretty.activate
    def test_post_without_oauth(self):
        """Check that the post method fails without OAuth parameters"""
        self.client = trovebox.Trovebox(host=self.test_host)
        self._register_uri(httpretty.POST)
        with self.assertRaises(trovebox.TroveboxError):
            self.client.post(self.test_endpoint)

    @httpretty.activate
    @data(GET, POST)
    def test_no_response_processing(self, method):
        """Check that get/post methods work with response processing disabled"""
        self._register_uri(method)
        response = GetOrPost(self.client, method).call(self.test_endpoint,
                                                       process_response=False)
        self.assertEqual(response, json.dumps(self.test_data))

    @httpretty.activate
    def test_get_parameter_processing(self):
        """Check that the parameter processing function is working"""
        self._register_uri(httpretty.GET)
        photo = trovebox.objects.photo.Photo(None, {"id": "photo_id"})
        album = trovebox.objects.album.Album(None, {"id": "album_id"})
        tag = trovebox.objects.tag.Tag(None, {"id": "tag_id"})
        self.client.get(self.test_endpoint,
                        photo=photo, album=album, tag=tag,
                        list_=[photo, album, tag],
                        list2=["1", "2", "3"],
                        boolean=True,
                        unicode_="\xfcmlaut")
        params = self._last_request().querystring
        self.assertEqual(params["photo"], ["photo_id"])
        self.assertEqual(params["album"], ["album_id"])
        self.assertEqual(params["tag"], ["tag_id"])
        self.assertEqual(params["list_"], ["photo_id,album_id,tag_id"])
        self.assertEqual(params["list2"], ["1,2,3"])
        self.assertEqual(params["boolean"], ["1"])
        self.assertIn(params["unicode_"], [["\xc3\xbcmlaut"], ["\xfcmlaut"]])

    @httpretty.activate
    @data(GET, POST)
    def test_api_version(self, method):
        """Check that an API version can be specified"""
        self.client = trovebox.Trovebox(host=self.test_host, **self.test_oauth)
        self.client.configure(api_version=1)
        self._register_uri(method,
                           uri="http://%s/v1/%s" % (self.test_host,
                                                    self.test_endpoint))
        GetOrPost(self.client, method).call(self.test_endpoint)

    @mock.patch.object(trovebox.http.requests, 'Session')
    @data(GET, POST)
    def test_ssl_verify_disabled(self, method, mock_session):
        """Check that SSL verification can be disabled for the get method"""
        session = mock_session.return_value.__enter__.return_value
        session.get.return_value.text = "response text"
        session.get.return_value.status_code = 200
        session.get.return_value.json.return_value = self.test_data
        # Handle either post or get
        session.post = session.get

        self.client = trovebox.Trovebox(host=self.test_host, **self.test_oauth)
        self.client.configure(ssl_verify=False)
        GetOrPost(self.client, method).call(self.test_endpoint)
        self.assertEqual(session.verify, False)

    @httpretty.activate
    def test_post_file(self):
        """Check that a file can be posted"""
        self._register_uri(httpretty.POST)
        with open(self.test_file, 'rb') as in_file:
            response = self.client.post(self.test_endpoint,
                                        files={"file": in_file})
        self.assertEqual(response, self.test_data)
        body = str(self._last_request().body)
        self.assertIn("Content-Disposition: form-data; "+
                      "name=\"file\"; filename=\"test_file.txt\"", body)
        self.assertIn("Test File", str(body))


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
