try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import trovebox
from tests.functional import test_base

class TestActions(test_base.TestBase):
    testcase_name = "action API"

    def test_create_view_delete(self):
        """ Create an action on a photo, view it, then delete it """
        # Create and check that the action exists
        action = self.client.action.create(target=self.photos[0], type="comment", name="test")
        action_id = action.id
        self.assertEqual(self.client.action.view(action_id).name, "test")

        # Delete and check that the action is gone
        action.delete()
        with self.assertRaises(trovebox.TroveboxError):
            self.client.action.view(action_id)

