class OpenPhotoError(Exception):
    """ Indicates that an OpenPhoto operation failed """
    pass

class OpenPhotoDuplicateError(OpenPhotoError):
    """ Indicates that an upload operation failed due to a duplicate photo """
    pass

class OpenPhoto404Error(Exception):
    """
    Indicates that an Http 404 error code was received
    (resource not found)
    """
    pass
