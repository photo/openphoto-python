from __future__ import unicode_literals
import json
import httpretty
from httpretty import GET

try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import trovebox

class TestSystem(unittest.TestCase):
    test_host = "test.example.com"

    def setUp(self):
        self.client = trovebox.Trovebox(host=self.test_host)

    @staticmethod
    def _return_value(result, message="", code=200):
        return json.dumps({"message": message, "code": code, "result": result})

class TestSystemVersion(TestSystem):
    test_result = {"api": "v2",
                   "database": "2.0.0"}

    @httpretty.activate
    def test_version(self):
        """Check that the version dictionary is returned correctly"""
        httpretty.register_uri(GET, uri="http://test.example.com/system/version.json",
                               body=self._return_value(self.test_result),
                               status=200)
        response = self.client.system.version()

        self.assertEqual(response, self.test_result)

class TestSystemDiagnostics(TestSystem):
    test_result = {'database': [{'label': 'failure',
                                 'message': 'Could not properly connect to the database.',
                                 'status': False}],
                   }

    @httpretty.activate
    def test_diagnostics_pass(self):
        """Check that the diagnostics dictionary is returned correctly on success"""
        httpretty.register_uri(GET, uri="http://test.example.com/system/diagnostics.json",
                               body=self._return_value(self.test_result),
                               status=200)
        response = self.client.system.diagnostics()

        self.assertEqual(response, self.test_result)

    @httpretty.activate
    def test_diagnostics_fail(self):
        """
        Check that the diagnostics dictionary is returned correctly on failure.
        Although the JSON code is 500, no exception should be raised.
        """
        # On failure, the diagnostics endpoint returns a JSON code of 500
        # and a response status code of 200.
        httpretty.register_uri(GET, uri="http://test.example.com/system/diagnostics.json",
                               body=self._return_value(self.test_result, code=500),
                               status=200)
        response = self.client.system.diagnostics()

        self.assertEqual(response, self.test_result)
