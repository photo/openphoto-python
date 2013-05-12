try:
    import unittest2 as unittest
except ImportError:
    import unittest
import os
import shutil
import openphoto

CONFIG_HOME_PATH = os.path.join("tests", "config")
CONFIG_PATH = os.path.join(CONFIG_HOME_PATH, "openphoto")

class TestConfig(unittest.TestCase):
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

    def create_config(self, config_file, host):
        with open(os.path.join(CONFIG_PATH, config_file), "w") as f:
            f.write("host = %s\n" % host)
            f.write("# Comment\n\n")
            f.write("consumerKey = \"%s_consumer_key\"\n" % config_file)
            f.write("\"consumerSecret\" = %s_consumer_secret\n" % config_file)
            f.write("'token'=%s_token\n" % config_file)
            f.write("tokenSecret = '%s_token_secret'\n" % config_file)

    def test_default_config(self):
        """ Ensure the default config is loaded """
        self.create_config("default", "Test Default Host")
        client = openphoto.OpenPhoto()
        self.assertEqual(client._host, "Test Default Host")
        self.assertEqual(client._consumer_key, "default_consumer_key")
        self.assertEqual(client._consumer_secret, "default_consumer_secret")
        self.assertEqual(client._token, "default_token")
        self.assertEqual(client._token_secret, "default_token_secret")

    def test_custom_config(self):
        """ Ensure a custom config can be loaded """
        self.create_config("default", "Test Default Host")
        self.create_config("custom", "Test Custom Host")
        client = openphoto.OpenPhoto(config_file="custom")
        self.assertEqual(client._host, "Test Custom Host")
        self.assertEqual(client._consumer_key, "custom_consumer_key")
        self.assertEqual(client._consumer_secret, "custom_consumer_secret")
        self.assertEqual(client._token, "custom_token")
        self.assertEqual(client._token_secret, "custom_token_secret")

    def test_full_config_path(self):
        """ Ensure a full custom config path can be loaded """
        self.create_config("path", "Test Path Host")
        full_path = os.path.abspath(CONFIG_PATH)
        client = openphoto.OpenPhoto(config_file=os.path.join(full_path, "path"))
        self.assertEqual(client._host, "Test Path Host")
        self.assertEqual(client._consumer_key, "path_consumer_key")
        self.assertEqual(client._consumer_secret, "path_consumer_secret")
        self.assertEqual(client._token, "path_token")
        self.assertEqual(client._token_secret, "path_token_secret")

    def test_host_override(self):
        """ Ensure that specifying a host overrides the default config """
        self.create_config("default", "Test Default Host")
        client = openphoto.OpenPhoto(host="host_override")
        self.assertEqual(client._host, "host_override")
        self.assertEqual(client._consumer_key, "")
        self.assertEqual(client._consumer_secret, "")
        self.assertEqual(client._token, "")
        self.assertEqual(client._token_secret, "")

    def test_missing_config_files_raise_exceptions(self):
        """ Ensure that missing config files raise exceptions """
        with self.assertRaises(IOError):
            openphoto.OpenPhoto()
        with self.assertRaises(IOError):
            openphoto.OpenPhoto(config_file="custom")

    def test_host_and_config_file_raises_exception(self):
        """ It's not valid to specify both a host and a config_file """
        self.create_config("custom", "Test Custom Host")
        with self.assertRaises(ValueError):
            openphoto.OpenPhoto(config_file="custom", host="host_override")


