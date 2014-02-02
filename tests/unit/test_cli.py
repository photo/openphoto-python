from __future__ import unicode_literals
import os
import sys
import shutil
import mock
try:
    import StringIO as io # Python2
except ImportError:
    import io # Python3
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import trovebox
from trovebox.main import main

class TestException(Exception):
    pass

def raise_exception(_):
    raise TestException()

class TestCli(unittest.TestCase):
    test_file = os.path.join("tests", "unit", "data", "test_file.txt")
    test_unicode_file = os.path.join("tests", "unit", "data",
                                     "\xfcnicode_test_file.txt")

    @mock.patch.object(trovebox.main.trovebox, "Trovebox")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_defaults(self, _, mock_trovebox):
        """Check that the default behaviour is correct"""
        get = mock_trovebox.return_value.get
        main([])
        mock_trovebox.assert_called_with(config_file=None)
        get.assert_called_with("/photos/list.json", process_response=False)

    @mock.patch.object(trovebox.main.trovebox, "Trovebox")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_config(self, _, mock_trovebox):
        """Check that a config file can be specified"""
        main(["--config=test"])
        mock_trovebox.assert_called_with(config_file="test")

    @mock.patch.object(trovebox.main.trovebox, "Trovebox")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_get(self, mock_stdout, mock_trovebox):
        """Check that the get operation is working"""
        get = mock_trovebox.return_value.get
        get.return_value = "Result"
        main(["-X", "GET", "-h", "test_host", "-e", "test_endpoint", "-F",
              "field1=1", "-F", "field2=2"])
        mock_trovebox.assert_called_with(host="test_host")
        get.assert_called_with("test_endpoint", field1="1", field2="2",
                               process_response=False)
        self.assertEqual(mock_stdout.getvalue(), "Result\n")

    @mock.patch.object(trovebox.main.trovebox, "Trovebox")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_post(self, mock_stdout, mock_trovebox):
        """Check that the post operation is working"""
        post = mock_trovebox.return_value.post
        post.return_value = "Result"
        main(["-X", "POST", "-h", "test_host", "-e", "test_endpoint", "-F",
              "field1=1", "-F", "field2=2"])
        mock_trovebox.assert_called_with(host="test_host")
        post.assert_called_with("test_endpoint", field1="1", field2="2",
                                files={}, process_response=False)
        self.assertEqual(mock_stdout.getvalue(), "Result\n")

    @mock.patch.object(trovebox.main.trovebox, "Trovebox")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_post_files(self, _, mock_trovebox):
        """Check that files are posted correctly"""
        post = mock_trovebox.return_value.post
        main(["-X", "POST", "-F", "photo=@%s" % self.test_file])
        # It's not possible to directly compare the file object,
        # so check it manually
        files = post.call_args[1]["files"]
        self.assertEqual(list(files.keys()), ["photo"])
        self.assertEqual(files["photo"].name, self.test_file)

    @mock.patch.object(trovebox.main.trovebox, "Trovebox")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_post_files_with_user_expansion(self, _, mock_trovebox):
        """
        Check that files are posted correctly when specified relative
        to the '~' user directory
        """
        post = mock_trovebox.return_value.post
        user_file = "~/.trovebox_temporary_file"
        expanded_file = os.path.expanduser(user_file)
        shutil.copy(self.test_file, expanded_file)
        try:
            main(["-X", "POST", "-F", "photo=@%s" % user_file])
            # It's not possible to directly compare the file object,
            # so check it manually
            files = post.call_args[1]["files"]
            self.assertEqual(list(files.keys()), ["photo"])
            self.assertEqual(files["photo"].name, expanded_file)
        finally:
            os.remove(expanded_file)

    @mock.patch.object(trovebox.main.trovebox, "Trovebox")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_post_missing_files(self, _, mock_trovebox):
        """Check that missing files cause an exception"""
        post = mock_trovebox.return_value.post
        with self.assertRaises(IOError):
            main(["-X", "POST", "-F", "photo=@%s.missing" % self.test_file])

    @mock.patch.object(trovebox.main.trovebox, "Trovebox")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_post_unicode_files(self, _, mock_trovebox):
        """Check that unicode filenames are posted correctly"""
        post = mock_trovebox.return_value.post

        # Python 2.x provides encoded commandline arguments
        file_param = "photo=@%s" % self.test_unicode_file
        if sys.version < '3':
            file_param = file_param.encode(sys.getfilesystemencoding())

        main(["-X", "POST", "-F", "photo=@%s" % self.test_unicode_file])
        # It's not possible to directly compare the file object,
        # so check it manually
        files = post.call_args[1]["files"]
        self.assertEqual(list(files.keys()), ["photo"])
        self.assertEqual(files["photo"].name, self.test_unicode_file)

    @unittest.skipIf(sys.version >= '3',
                     "Python3 only uses unicode commandline arguments")
    @mock.patch('trovebox.main.sys.getfilesystemencoding')
    @mock.patch.object(trovebox.main.trovebox, "Trovebox")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_post_utf8_files(self, _, mock_trovebox, mock_getfilesystemencoding):
        """Check that utf-8 encoded filenames are posted correctly"""
        post = mock_trovebox.return_value.post
        # Make the system think its filesystemencoding is utf-8
        mock_getfilesystemencoding.return_value = "utf-8"

        file_param = "photo=@%s" % self.test_unicode_file
        file_param = file_param.encode("utf-8")

        main(["-X", "POST", "-F", file_param])
        # It's not possible to directly compare the file object,
        # so check it manually
        files = post.call_args[1]["files"]
        self.assertEqual(list(files.keys()), ["photo"])
        self.assertEqual(files["photo"].name, self.test_unicode_file)

    @mock.patch.object(sys, "exit", raise_exception)
    @mock.patch('sys.stderr', new_callable=io.StringIO)
    def test_unknown_arg(self, mock_stderr):
        """Check that an unknown argument produces an error"""
        with self.assertRaises(TestException):
            main(["hello"])
        self.assertIn("error: Unknown argument", mock_stderr.getvalue())

    @mock.patch.object(sys, "exit", raise_exception)
    @mock.patch('sys.stderr', new_callable=io.StringIO)
    def test_unknown_option(self, mock_stderr):
        """Check that an unknown option produces an error"""
        with self.assertRaises(TestException):
            main(["--hello"])
        self.assertIn("error: no such option", mock_stderr.getvalue())

    @mock.patch.object(sys, "exit", raise_exception)
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_unknown_config(self, mock_stdout):
        """Check that an unknown config file produces an error"""
        with self.assertRaises(TestException):
            main(["--config=this_config_doesnt_exist"])
        self.assertIn("No such file or directory", mock_stdout.getvalue())
        self.assertIn("You must create a configuration file",
                      mock_stdout.getvalue())
        self.assertIn("To get your credentials", mock_stdout.getvalue())

    @mock.patch.object(trovebox.main.trovebox, "Trovebox")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_verbose_without_params(self, mock_stdout, _):
        """Check that the verbose option works with no parameters"""
        main(["-v"])
        self.assertIn("Method: GET", mock_stdout.getvalue())
        self.assertIn("Endpoint: /photos/list.json", mock_stdout.getvalue())
        self.assertNotIn("Fields:", mock_stdout.getvalue())

    @mock.patch.object(trovebox.main.trovebox, "Trovebox")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_verbose_with_params(self, mock_stdout, _):
        """Check that the verbose option works with parameters"""
        main(["-v", "-F foo=bar"])
        self.assertIn("Method: GET", mock_stdout.getvalue())
        self.assertIn("Endpoint: /photos/list.json", mock_stdout.getvalue())
        self.assertIn("Fields:\n   foo=bar", mock_stdout.getvalue())

    @mock.patch.object(trovebox.main.trovebox, "Trovebox")
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_pretty_print(self, mock_stdout, mock_trovebox):
        """Check that the pretty-print option is working"""
        get = mock_trovebox.return_value.get
        get.return_value = '{"test":1}'
        main(["-p"])
        self.assertEqual(mock_stdout.getvalue(), '{\n    "test":1\n}\n')

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_version(self, mock_stdout):
        """Check that the version string is correctly printed"""
        main(["--version"])
        self.assertEqual(mock_stdout.getvalue(), trovebox.__version__ + "\n")

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_help(self, mock_stdout):
        """Check that the help string is correctly printed"""
        main(["--help"])
        self.assertIn("show this help message", mock_stdout.getvalue())
