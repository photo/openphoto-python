import unittest
import openphoto
import test_base

class TestTags(test_base.TestBase):
    testcase_name = "tag API"

    @unittest.expectedFailure # Tag create fails - Issue #927
    # NOTE: the below has not been tested/debugged, since it fails at the first step
    def test_create_delete(self, tag_name="create_tag"):
        """ Create a tag then delete it """
        # Create a tag
        tag = self.client.tag.create(tag_name)

        # Check the return value
        self.assertEqual(tag.id, tag_name)
        # Check that the tag now exists
        self.assertIn(tag_name, self.client.tags.list())

        # Delete the tag
        self.assertTrue(self.client.tag.delete(tag_name))
        # Check that the tag is now gone
        self.assertNotIn(tag_name, self.client.tags.list())

        # Create and delete using the Tag object directly
        tag = self.client.tag.create(tag_name)
        self.assertTrue(tag.delete())
        # Check that the tag is now gone
        self.assertNotIn(tag_name, self.client.tags.list())

    @unittest.expectedFailure # Tag update fails - Issue #927
    # NOTE: the below has not been tested/debugged, since it fails at the first step
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

    @unittest.expectedFailure # Tag create fails - Issue #927
    # NOTE: the below has not been tested/debugged, since it fails at the first step
    def test_tag_with_spaces(self):
        """ Run test_create_delete using a tag containing spaces """
        self.test_create_delete("tag with spaces")

    # We mustn't run this test until Issue #919 is resolved,
    # since it creates an undeletable tag
    @unittest.skip("Tags with double-slashes cannot be deleted - Issue #919")
    def test_tag_with_double_slashes(self):
        """ Run test_create_delete using a tag containing slashes """
        self.test_create_delete("tag/with//slashes")
