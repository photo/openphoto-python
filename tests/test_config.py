import unittest
import os
import shutil
import openphoto

CONFIG_HOME_PATH = os.path.join("test", "config")
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
        f = open(os.path.join(CONFIG_PATH, config_file), "w")
        f.write("host = %s\n" % host)
        f.write("# Comment\n\n")
        f.write("consumerKey = \"%s_consumer_key\"\n" % config_file)
        f.write("\"consumerSecret\" = %s_consumer_secret\n" % config_file)
        f.write("'token'=%s_token\n" % config_file)
        f.write("tokenSecret = '%s_token_secret'\n" % config_file)

    def test_default_config(self):
        self.create_config("default", "Test Default Host")
        client = openphoto.OpenPhoto()
        self.assertEqual(client._host, "Test Default Host")
        self.assertEqual(client._consumer_key, "default_consumer_key")
        self.assertEqual(client._consumer_secret, "default_consumer_secret")
        self.assertEqual(client._token, "default_token")
        self.assertEqual(client._token_secret, "default_token_secret")

    def test_custom_config(self):
        self.create_config("default", "Test Default Host")
        self.create_config("custom", "Test Custom Host")
        client = openphoto.OpenPhoto(config_file="custom")
        self.assertEqual(client._host, "Test Custom Host")
        self.assertEqual(client._consumer_key, "custom_consumer_key")
        self.assertEqual(client._consumer_secret, "custom_consumer_secret")
        self.assertEqual(client._token, "custom_token")
        self.assertEqual(client._token_secret, "custom_token_secret")

    def test_host_override(self):
        self.create_config("default", "Test Default Host")
        client = openphoto.OpenPhoto(host="host_override")
        self.assertEqual(client._host, "host_override")
        self.assertEqual(client._consumer_key, "")
        self.assertEqual(client._consumer_secret, "")
        self.assertEqual(client._token, "")
        self.assertEqual(client._token_secret, "")

    def test_missing_config_files(self):
        with self.assertRaises(IOError):
            openphoto.OpenPhoto()
        with self.assertRaises(IOError):
            openphoto.OpenPhoto(config_file="custom")

    def test_host_and_config_file_raises_exception(self):
        self.create_config("custom", "Test Custon Host")
        with self.assertRaises(ValueError):
            openphoto.OpenPhoto(config_file="custom", host="host_override")


