import os
import shutil
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

from trovebox import Trovebox

CONFIG_HOME_PATH = os.path.join("tests", "config")
CONFIG_PATH = os.path.join(CONFIG_HOME_PATH, "trovebox")

class TestAuth(unittest.TestCase):
    def setUp(self):
        """ Override XDG_CONFIG_HOME env var, to use test configs """
        try:
            self.original_xdg_config_home = os.environ["XDG_CONFIG_HOME"]
        except KeyError:
            self.original_xdg_config_home = None
        os.environ["XDG_CONFIG_HOME"] = CONFIG_HOME_PATH
        os.makedirs(CONFIG_PATH)

    def tearDown(self):
        if self.original_xdg_config_home is None:
            del os.environ["XDG_CONFIG_HOME"]
        else:
            os.environ["XDG_CONFIG_HOME"] = self.original_xdg_config_home
        shutil.rmtree(CONFIG_HOME_PATH, ignore_errors=True)

    @staticmethod
    def create_config(config_file, host):
        """Create a dummy config file"""
        with open(os.path.join(CONFIG_PATH, config_file), "w") as conf:
            conf.write("host = %s\n" % host)
            conf.write("# Comment\n\n")
            conf.write("consumerKey = \"%s_consumer_key\"\n" % config_file)
            conf.write("\"consumerSecret\"= %s_consumer_secret\n" % config_file)
            conf.write("'token'=%s_token\n" % config_file)
            conf.write("tokenSecret = '%s_token_secret'\n" % config_file)

    def test_default_config(self):
        """ Ensure the default config is loaded """
        self.create_config("default", "Test Default Host")
        client = Trovebox()
        auth = client.auth
        self.assertEqual(client.host, "Test Default Host")
        self.assertEqual(auth.consumer_key, "default_consumer_key")
        self.assertEqual(auth.consumer_secret, "default_consumer_secret")
        self.assertEqual(auth.token, "default_token")
        self.assertEqual(auth.token_secret, "default_token_secret")

    def test_custom_config(self):
        """ Ensure a custom config can be loaded """
        self.create_config("default", "Test Default Host")
        self.create_config("custom", "Test Custom Host")
        client = Trovebox(config_file="custom")
        auth = client.auth
        self.assertEqual(client.host, "Test Custom Host")
        self.assertEqual(auth.consumer_key, "custom_consumer_key")
        self.assertEqual(auth.consumer_secret, "custom_consumer_secret")
        self.assertEqual(auth.token, "custom_token")
        self.assertEqual(auth.token_secret, "custom_token_secret")

    def test_full_config_path(self):
        """ Ensure a full custom config path can be loaded """
        self.create_config("path", "Test Path Host")
        full_path = os.path.abspath(CONFIG_PATH)
        client = Trovebox(config_file=os.path.join(full_path, "path"))
        auth = client.auth
        self.assertEqual(client.host, "Test Path Host")
        self.assertEqual(auth.consumer_key, "path_consumer_key")
        self.assertEqual(auth.consumer_secret, "path_consumer_secret")
        self.assertEqual(auth.token, "path_token")
        self.assertEqual(auth.token_secret, "path_token_secret")

    def test_host_override(self):
        """ Ensure that specifying a host overrides the default config """
        self.create_config("default", "Test Default Host")
        client = Trovebox(host="host_override")
        auth = client.auth
        self.assertEqual(auth.host, "host_override")
        self.assertEqual(auth.consumer_key, "")
        self.assertEqual(auth.consumer_secret, "")
        self.assertEqual(auth.token, "")
        self.assertEqual(auth.token_secret, "")

    def test_missing_config_files(self):
        """ Ensure that missing config files raise exceptions """
        with self.assertRaises(IOError):
            Trovebox()
        with self.assertRaises(IOError):
            Trovebox(config_file="custom")

    def test_host_and_config_file(self):
        """ It's not valid to specify both a host and a config_file """
        self.create_config("custom", "Test Custom Host")
        with self.assertRaises(ValueError):
            Trovebox(config_file="custom", host="host_override")


