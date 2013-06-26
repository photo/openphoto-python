import os
import sys
import mock
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import openphoto
from openphoto.main import main

class TestException(Exception):
    pass

def raise_exception(_):
    raise TestException()

class TestCli(unittest.TestCase):
    TEST_FILE = os.path.join("tests", "unit", "data", "test_file.txt")

    @mock.patch.object(openphoto.main, "OpenPhoto")
    def test_defaults(self, MockOpenPhoto):
        get = MockOpenPhoto.return_value.get
        main([])
        MockOpenPhoto.assert_called_with(config_file=None)
        get.assert_called_with("/photos/list.json", process_response=False)

    @mock.patch.object(openphoto.main, "OpenPhoto")
    def test_config(self, MockOpenPhoto):
        main(["--config=test"])
        MockOpenPhoto.assert_called_with(config_file="test")

    @mock.patch.object(openphoto.main, "OpenPhoto")
    def test_get(self, MockOpenPhoto):
        get = MockOpenPhoto.return_value.get
        get.return_value = "Result"
        main(["-X", "GET", "-h", "test_host", "-e", "test_endpoint", "-F",
              "field1=1", "-F", "field2=2"])
        MockOpenPhoto.assert_called_with(host="test_host")
        get.assert_called_with("test_endpoint", field1="1", field2="2",
                               process_response=False)
        # TODO: self.assertEq(mock_stdout.getvalue(), "Result")

    @mock.patch.object(openphoto.main, "OpenPhoto")
    def test_post(self, MockOpenPhoto):
        post = MockOpenPhoto.return_value.post
        post.return_value = "Result"
        main(["-X", "POST", "-h", "test_host", "-e", "test_endpoint", "-F",
              "field1=1", "-F", "field2=2"])
        MockOpenPhoto.assert_called_with(host="test_host")
        post.assert_called_with("test_endpoint", field1="1", field2="2", files={},
                               process_response=False)
        # TODO: self.assertEq(mock_stdout.getvalue(), "Result")

    @mock.patch.object(openphoto.main, "OpenPhoto")
    def test_post_files(self, MockOpenPhoto):
        post = MockOpenPhoto.return_value.post
        main(["-X", "POST", "-F", "photo=@%s" % self.TEST_FILE])
        # It's not possible to directly compare the file object, so check it manually
        files = post.call_args[1]["files"]
        self.assertEqual(files.keys(), ["photo"])
        self.assertEqual(files["photo"].name, self.TEST_FILE)

    @mock.patch.object(sys, "exit", raise_exception)
    def test_unknown_arg(self):
        with self.assertRaises(TestException):
            main(["hello"])
        # TODO: self.assertIn(mock_stdout.getvalue(), "Error: Unknown argument")

    @mock.patch.object(sys, "exit", raise_exception)
    def test_unknown_option(self):
        with self.assertRaises(TestException):
            main(["--hello"])
        # TODO: self.assertIn(mock_stdout.getvalue(), "Error: no such option")

    @mock.patch.object(sys, "exit", raise_exception)
    def test_unknown_config(self):
        with self.assertRaises(TestException):
            main(["--config=this_config_doesnt_exist"])
        # TODO: self.assertIn(mock_stdout.getvalue(), "No such file or directory")
        # TODO: self.assertIn(mock_stdout.getvalue(), "You must create a configuration file")
        # TODO: self.assertIn(mock_stdout.getvalue(), "To get your credentials")

    @mock.patch.object(openphoto.main, "OpenPhoto")
    def test_verbose(self, _):
        main(["-v"])
        # TODO: self.assertIn(mock_stdout.getvalue(), "Method: GET")
        # TODO: self.assertIn(mock_stdout.getvalue(), "Endpoint: /photos/list.json")

    @mock.patch.object(openphoto.main, "OpenPhoto")
    def test_pretty_print(self, MockOpenPhoto):
        get = MockOpenPhoto.return_value.get
        get.return_value = '{"test":1}'
        main(["-p"])
        # TODO: self.assertEq(mock_stdout.getvalue(), '{\n    "test":1\n}")
