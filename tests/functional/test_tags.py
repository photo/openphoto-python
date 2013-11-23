try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

from tests.functional import test_base

@unittest.skipIf(test_base.get_test_server_api() == 1,
                 "The tag API didn't work at v1 - see frontend issue #927")
class TestTags(test_base.TestBase):
    testcase_name = "tag API"

    def test_create_delete(self, tag_id="create_tag"):
        """
        Create a tag then delete it.
        This test is a little contrived, since the tag create/delete
        endpoints are only intended for internal use.
        """
        # Create a tag
        self.assertTrue(self.client.tag.create(tag_id))
        # Check that the tag doesn't exist (It has no photos, so it's invisible)
        self.assertNotIn(tag_id, [t.id for t in self.client.tags.list()])

        # Create a tag on one of the photos
        self.photos[0].update(tagsAdd=tag_id)
        # Check that the tag now exists
        self.assertIn(tag_id, [t.id for t in self.client.tags.list()])

        # Delete the tag
        self.assertTrue(self.client.tag.delete(tag_id))
        # Check that the tag is now gone
        self.assertNotIn(tag_id, [t.id for t in self.client.tags.list()])
        # Also remove the tag from the photo
        self.photos[0].update(tagsRemove=tag_id)

        # Create the tag again
        self.photos[0].update(tagsAdd=tag_id)
        self.assertIn(tag_id, [t.id for t in self.client.tags.list()])

        # Delete using the tag object directly
        tag = [t for t in self.client.tags.list() if t.id == tag_id][0]
        self.assertTrue(tag.delete())

        # Check that the tag is now gone
        self.assertNotIn(tag_id, [t.id for t in self.client.tags.list()])
        # Also remove the tag from the photo
        self.photos[0].update(tagsRemove=tag_id)

    # TODO: Un-skip and update this tests once there are tag fields
    #       that can be updated (the owner field cannot be updated).
    @unittest.skip("Can't test the tag.update endpoint, "
                   "since there are no fields that can be updated")
    def test_update(self):
        """ Test that a tag can be updated """
        # Update the tag using the Trovebox class, passing in the tag object
        owner = "test1@trovebox.com"
        ret_val = self.client.tag.update(self.tags[0], owner=owner)

        # Check that the tag is updated
        self.tags = self.client.tags.list()
        self.assertEqual(self.tags[0].owner, owner)
        self.assertEqual(ret_val.owner, owner)

        # Update the tag using the Trovebox class, passing in the tag id
        owner = "test2@trovebox.com"
        ret_val = self.client.tag.update(self.TEST_TAG, owner=owner)

        # Check that the tag is updated
        self.tags = self.client.tags.list()
        self.assertEqual(self.tags[0].owner, owner)
        self.assertEqual(ret_val.owner, owner)

        # Update the tag using the Tag object directly
        owner = "test3@trovebox.com"
        ret_val = self.tags[0].update(owner=owner)

        # Check that the tag is updated
        self.tags = self.client.tags.list()
        self.assertEqual(self.tags[0].owner, owner)
        self.assertEqual(ret_val.owner, owner)

    def test_tag_with_spaces(self):
        """ Run test_create_delete using a tag containing spaces """
        self.test_create_delete("tag with spaces")

    def test_tag_with_slashes(self):
        """ Run test_create_delete using a tag containing slashes """
        self.test_create_delete("tag/with/slashes")

    # TODO: Un-skip this test once issue #919 is resolved -
    #       tags with double-slashes cannot be deleted
    @unittest.skip("Tags with double-slashed cannot be deleted")
    def test_tag_with_double_slashes(self):
        """ Run test_create_delete using a tag containing double-slashes """
        self.test_create_delete("tag//with//double//slashes")
