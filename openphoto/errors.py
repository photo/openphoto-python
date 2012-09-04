class OpenPhotoError(Exception):
    """ Indicates that an OpenPhoto operation failed """
    pass

class OpenPhotoDuplicateError(OpenPhotoError):
    """ Indicates that an upload operation failed due to a duplicate photo """
    pass

class NotImplementedError(OpenPhotoError):
    """ Indicates that the API function has not yet been coded - please help! """
    pass

