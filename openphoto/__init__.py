from openphoto_http import OpenPhotoHttp
from errors import *
import api_photo
import api_tag
import api_album

LATEST_API_VERSION = 2

class OpenPhoto(OpenPhotoHttp):
    """
    Python client library for the specified OpenPhoto host.
    OAuth tokens (consumer*, token*) can optionally be specified.

    All requests will include the api_version path, if specified.
    This should be used to ensure that your application will continue to work
    even if the OpenPhoto API is updated to a new revision.
    """
    def __init__(self, host,
                 consumer_key='', consumer_secret='',
                 token='', token_secret='',
                 api_version=None):
        OpenPhotoHttp.__init__(self, host,
                               consumer_key, consumer_secret,
                               token, token_secret, api_version)

        self.photos = api_photo.ApiPhotos(self)
        self.photo = api_photo.ApiPhoto(self)
        self.tags = api_tag.ApiTags(self)
        self.tag = api_tag.ApiTag(self)
        self.albums = api_album.ApiAlbums(self)
        self.album = api_album.ApiAlbum(self)
