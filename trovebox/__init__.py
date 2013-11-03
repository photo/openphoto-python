"""
__init__.py : Trovebox package top level
"""
from .http import Http
from .errors import TroveboxError, TroveboxDuplicateError, Trovebox404Error
from ._version import __version__
from trovebox.api import api_photo
from trovebox.api import api_tag
from trovebox.api import api_album
from trovebox.api import api_action
from trovebox.api import api_activity
from trovebox.api import api_system

LATEST_API_VERSION = 2

class Trovebox(Http):
    """
    Client library for Trovebox
    If no parameters are specified, config is loaded from the default
        location (~/.config/trovebox/default).
    The config_file parameter is used to specify an alternate config file.
    If the host parameter is specified, no config file is loaded and
        OAuth tokens (consumer*, token*) can optionally be specified.
    All requests will include the api_version path, if specified.
    This should be used to ensure that your application will continue to work
        even if the Trovebox API is updated to a new revision.
    """
    def __init__(self, config_file=None, host=None,
                 consumer_key='', consumer_secret='',
                 token='', token_secret='',
                 api_version=None):
        Http.__init__(self, config_file, host,
                      consumer_key, consumer_secret,
                      token, token_secret, api_version)

        self.photos = api_photo.ApiPhotos(self)
        self.photo = api_photo.ApiPhoto(self)
        self.tags = api_tag.ApiTags(self)
        self.tag = api_tag.ApiTag(self)
        self.albums = api_album.ApiAlbums(self)
        self.album = api_album.ApiAlbum(self)
        self.action = api_action.ApiAction(self)
        self.activities = api_activity.ApiActivities(self)
        self.activity = api_activity.ApiActivity(self)
        self.system = api_system.ApiSystem(self)
