from __future__ import print_function
import sys
import os
import logging
try:
    import unittest2 as unittest # Python2.6
except ImportError:
    import unittest

import openphoto

def get_test_server_api():
    return int(os.getenv("OPENPHOTO_TEST_SERVER_API", openphoto.LATEST_API_VERSION))

class TestBase(unittest.TestCase):
    TEST_TITLE = "Test Image - delete me!"
    TEST_TAG = "test_tag"
    TEST_ALBUM = "test_album"
    MAXIMUM_TEST_PHOTOS = 4 # Never have more the 4 photos on the test server
    testcase_name = "(unknown testcase)"
    api_version = None

    config_file = os.getenv("OPENPHOTO_TEST_CONFIG", "test")
    debug = (os.getenv("OPENPHOTO_TEST_DEBUG", "0") == "1")

    def __init__(self, *args, **kwds):
        unittest.TestCase.__init__(self, *args, **kwds)
        self.photos = []

        logging.basicConfig(filename="tests.log",
                            filemode="w",
                            format="%(message)s",
                            level=logging.INFO)

    @classmethod
    def setUpClass(cls):
        """ Ensure there is nothing on the server before running any tests """
        if cls.debug:
            if cls.api_version is None:
                print("\nTesting Latest %s" % cls.testcase_name)
            else:
                print("\nTesting %s v%d" % (cls.testcase_name, cls.api_version))

        cls.client = openphoto.OpenPhoto(config_file=cls.config_file,
                                         api_version=cls.api_version)

        if cls.client.photos.list() != []:
            raise ValueError("The test server (%s) contains photos. "
                             "Please delete them before running the tests"
                             % cls.client._host)

        if cls.client.tags.list() != []:
            raise ValueError("The test server (%s) contains tags. "
                             "Please delete them before running the tests"
                             % cls.client._host)

        if cls.client.albums.list() != []:
            raise ValueError("The test server (%s) contains albums. "
                             "Please delete them before running the tests"
                             % cls.client._host)

    @classmethod
    def tearDownClass(cls):
        """ Once all tests have finished, delete all photos, tags and albums"""
        cls._delete_all()

    def setUp(self):
        """
        Ensure the three test photos are present before each test.
        Give them each a tag.
        Put them into an album.
        """
        self.photos = self.client.photos.list()
        if len(self.photos) != 3:
            if self.debug:
                print("[Regenerating Photos]")
            else:
                print(" ", end='')
                sys.stdout.flush()
            if len(self.photos) > 0:
                self._delete_all()
            self._create_test_photos()
            self.photos = self.client.photos.list()

        self.tags = self.client.tags.list()
        if (len(self.tags) != 1 or
                self.tags[0].id != self.TEST_TAG or
                str(self.tags[0].count) != "3"):
            if self.debug:
                print("[Regenerating Tags]")
            else:
                print(" ", end='')
                sys.stdout.flush()
            self._delete_all()
            self._create_test_photos()
            self.photos = self.client.photos.list()
            self.tags = self.client.tags.list()
        if len(self.tags) != 1:
            print("Tags: %s" % self.tags)
            raise Exception("Tag creation failed")

        self.albums = self.client.albums.list()
        if (len(self.albums) != 1 or
                self.albums[0].name != self.TEST_ALBUM or
                self.albums[0].count != "3"):
            if self.debug:
                print("[Regenerating Albums]")
            else:
                print(" ", end='')
                sys.stdout.flush()
            self._delete_all()
            self._create_test_photos()
            self.photos = self.client.photos.list()
            self.tags = self.client.tags.list()
            self.albums = self.client.albums.list()
        if len(self.albums) != 1:
            print("Albums: %s" % self.albums)
            raise Exception("Album creation failed")

        logging.info("\nRunning %s..." % self.id())

    def tearDown(self):
        logging.info("Finished %s\n" % self.id())

    @classmethod
    def _create_test_photos(cls):
        """ Upload three test photos """
        album = cls.client.album.create(cls.TEST_ALBUM)
        photos = [
            cls.client.photo.upload("tests/test_photo1.jpg",
                                    title=cls.TEST_TITLE,
                                    albums=album.id),
            cls.client.photo.upload("tests/test_photo2.jpg",
                                    title=cls.TEST_TITLE,
                                    albums=album.id),
            cls.client.photo.upload("tests/test_photo3.jpg",
                                    title=cls.TEST_TITLE,
                                    albums=album.id),
            ]
        # Add the test tag, removing any autogenerated tags
        for photo in photos:
            photo.update(tags=cls.TEST_TAG)

    @classmethod
    def _delete_all(cls):
        photos = cls.client.photos.list()
        if len(photos) > cls.MAXIMUM_TEST_PHOTOS:
            raise ValueError("There too many photos on the test server - must always be less than %d."
                             % cls.MAXIMUM_TEST_PHOTOS)
        for photo in photos:
            photo.delete()
        for tag in cls.client.tags.list():
            tag.delete()
        for album in cls.client.albums.list():
            album.delete()
