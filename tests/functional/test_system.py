import logging
import unittest

import trovebox
from tests.functional import test_base

class TestSystem(test_base.TestBase):
    testcase_name = "system"

    def setUp(self):
        """
        Override the default setUp, since we don't need a populated database
        """
        logging.info("\nRunning %s...", self.id())

    def test_system_version(self):
        """
        Check that the API version string is returned correctly
        """
        client = trovebox.Trovebox(config_file=self.config_file)
        version = client.system.version()
        self.assertEqual(version["api"], "v%s" % trovebox.LATEST_API_VERSION)

    @unittest.skip("Diagnostics don't work with the hosted site")
    def test_system_diagnostics(self):
        """
        Check that the system diagnostics can be performed
        """
        client = trovebox.Trovebox(config_file=self.config_file)
        diagnostics = client.system.diagnostics()
        self.assertIn(diagnostics, "database")
