import os
import sys
from StringIO import StringIO
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
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_defaults(self, _, MockOpenPhoto):
        get = MockOpenPhoto.return_value.get
        main([])
        MockOpenPhoto.assert_called_with(config_file=None)
        get.assert_called_with("/photos/list.json", process_response=False)

    @mock.patch.object(openphoto.main, "OpenPhoto")
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_config(self, _, MockOpenPhoto):
        main(["--config=test"])
        MockOpenPhoto.assert_called_with(config_file="test")

    @mock.patch.object(openphoto.main, "OpenPhoto")
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_get(self, mock_stdout, MockOpenPhoto):
        get = MockOpenPhoto.return_value.get
        get.return_value = "Result"
        main(["-X", "GET", "-h", "test_host", "-e", "test_endpoint", "-F",
              "field1=1", "-F", "field2=2"])
        MockOpenPhoto.assert_called_with(host="test_host")
        get.assert_called_with("test_endpoint", field1="1", field2="2",
                               process_response=False)
        self.assertEqual(mock_stdout.getvalue(), "Result\n")

    @mock.patch.object(openphoto.main, "OpenPhoto")
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_post(self, mock_stdout, MockOpenPhoto):
        post = MockOpenPhoto.return_value.post
        post.return_value = "Result"
        main(["-X", "POST", "-h", "test_host", "-e", "test_endpoint", "-F",
              "field1=1", "-F", "field2=2"])
        MockOpenPhoto.assert_called_with(host="test_host")
        post.assert_called_with("test_endpoint", field1="1", field2="2", files={},
                               process_response=False)
        self.assertEqual(mock_stdout.getvalue(), "Result\n")

    @mock.patch.object(openphoto.main, "OpenPhoto")
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_post_files(self, _, MockOpenPhoto):
        post = MockOpenPhoto.return_value.post
        main(["-X", "POST", "-F", "photo=@%s" % self.TEST_FILE])
        # It's not possible to directly compare the file object, so check it manually
        files = post.call_args[1]["files"]
        self.assertEqual(files.keys(), ["photo"])
        self.assertEqual(files["photo"].name, self.TEST_FILE)

    @mock.patch.object(sys, "exit", raise_exception)
    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_unknown_arg(self, mock_stderr):
        with self.assertRaises(TestException):
            main(["hello"])
        self.assertIn("error: Unknown argument", mock_stderr.getvalue())

    @mock.patch.object(sys, "exit", raise_exception)
    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_unknown_option(self, mock_stderr):
        with self.assertRaises(TestException):
            main(["--hello"])
        self.assertIn("error: no such option", mock_stderr.getvalue())

    @mock.patch.object(sys, "exit", raise_exception)
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_unknown_config(self, mock_stdout):
        with self.assertRaises(TestException):
            main(["--config=this_config_doesnt_exist"])
        self.assertIn("No such file or directory", mock_stdout.getvalue())
        self.assertIn("You must create a configuration file", mock_stdout.getvalue())
        self.assertIn("To get your credentials", mock_stdout.getvalue())

    @mock.patch.object(openphoto.main, "OpenPhoto")
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_verbose(self, mock_stdout, _):
        main(["-v"])
        self.assertIn("Method: GET", mock_stdout.getvalue())
        self.assertIn("Endpoint: /photos/list.json", mock_stdout.getvalue())

    @mock.patch.object(openphoto.main, "OpenPhoto")
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_pretty_print(self, mock_stdout, MockOpenPhoto):
        get = MockOpenPhoto.return_value.get
        get.return_value = '{"test":1}'
        main(["-p"])
        self.assertEqual(mock_stdout.getvalue(), '{\n    "test":1\n}\n')
