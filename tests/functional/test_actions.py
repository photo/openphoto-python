try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

from tests.functional import test_base

class TestActions(test_base.TestBase):
    testcase_name = "action API"

    # TODO: Enable this test (and write more) once the Actions API is working.
    #       Currently always returns:
    #       "Could not find route /action/create.json from /action/create.json"
    @unittest.expectedFailure
    def test_create_delete(self):
        """ Create an action on a photo, then delete it """
        action = self.client.action.create(target=self.photos[0])
