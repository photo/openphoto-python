from openphoto_http import OpenPhotoHttp, OpenPhotoError, OpenPhotoDuplicateError
from api_photo import ApiPhoto
from api_tag import ApiTag
from api_album import ApiAlbum

class OpenPhoto(OpenPhotoHttp, ApiPhoto, ApiTag, ApiAlbum):
    """ Client library for OpenPhoto """
    pass
