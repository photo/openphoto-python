import unittest
import openphoto
import test_base

class TestTags(test_base.TestBase):
    def test_create_delete(self, tag_id="create_tag"):
        """ Create a tag then delete it """
        # Create a tag
        self.assertTrue(self.client.tag.create(tag_id))
        # Check that the tag doesn't exist (It has no photos, so it's invisible)
        self.assertNotIn(tag_id, [t.id for t in self.client.tags.list()])

        # Create a tag on one of the photos
        self.photos[0].update(tagsAdd=tag_id)
        # Check that the tag now exists
        self.assertIn(tag_id, [t.id for t in self.client.tags.list()])

        # Delete the tag
        self.client.tag.delete(tag_id)
        # Check that the tag is now gone
        self.assertNotIn(tag_id, [t.id for t in self.client.tags.list()])

        # Create then delete using the Tag object directly
        self.photos[0].update(tagsAdd=tag_id)
        tag = [t for t in self.client.tags.list() if t.id == tag_id][0]
        tag.delete()
        # Check that the tag is now gone
        self.assertNotIn(tag_id, [t.id for t in self.client.tags.list()])

    # NOTE: this test doesn't work, since it's not possible to update the tag owner
    # It's unclear what tag/update is for, since there are no fields that can be updated!
    @unittest.skip
    def test_update(self):
        """ Test that a tag can be updated """
        # Update the tag using the OpenPhoto class, passing in the tag object
        owner = "test1@openphoto.me"
        ret_val = self.client.tag.update(self.tags[0], owner=owner)

        # Check that the tag is updated
        self.tags = self.client.tags.list()
        self.assertEqual(self.tags[0].owner, owner)
        self.assertEqual(ret_val.owner, owner)

        # Update the tag using the OpenPhoto class, passing in the tag id
        owner = "test2@openphoto.me"
        ret_val = self.client.tag.update(self.TEST_TAG, owner=owner)

        # Check that the tag is updated
        self.tags = self.client.tags.list()
        self.assertEqual(self.tags[0].owner, owner)
        self.assertEqual(ret_val.owner, owner)

        # Update the tag using the Tag object directly
        owner = "test3@openphoto.me"
        ret_val = self.tags[0].update(owner=owner)

        # Check that the tag is updated
        self.tags = self.client.tags.list()
        self.assertEqual(self.tags[0].owner, owner)
        self.assertEqual(ret_val.owner, owner)

    def test_tag_with_spaces(self):
        """ Run test_create_delete using a tag containing spaces """
        self.test_create_delete("tag with spaces")

    # We mustn't run this test until Issue #919 is resolved,
    # since it creates an undeletable tag
    @unittest.skip("Tags with double-slashes cannot be deleted - Issue #919")
    def test_tag_with_double_slashes(self):
        """ Run test_create_delete using a tag containing slashes """
        self.test_create_delete("tag/with//slashes")
