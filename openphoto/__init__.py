from openphoto_http import OpenPhotoHttp
from errors import *
import api_photo
import api_tag
import api_album

class OpenPhoto(OpenPhotoHttp):
    """
    Client library for OpenPhoto
    If no parameters are specified, config is loaded from the default
        location (~/.config/openphoto/default).
    The config_file parameter is used to specify an alternate config file.
    If the host parameter is specified, no config file is loaded.
    """
    def __init__(self, config_file=None, host=None,
                 consumer_key='', consumer_secret='',
                 token='', token_secret=''):
        OpenPhotoHttp.__init__(self, config_file, host,
                               consumer_key, consumer_secret,
                               token, token_secret)

        self.photos = api_photo.ApiPhotos(self)
        self.photo = api_photo.ApiPhoto(self)
        self.tags = api_tag.ApiTags(self)
        self.tag = api_tag.ApiTag(self)
        self.albums = api_album.ApiAlbums(self)
        self.album = api_album.ApiAlbum(self)
