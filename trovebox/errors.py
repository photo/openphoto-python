"""
errors.py : Trovebox Error Classes
"""
class TroveboxError(Exception):
    """ Indicates that a Trovebox operation failed """
    pass

class TroveboxDuplicateError(TroveboxError):
    """ Indicates that an upload operation failed due to a duplicate photo """
    pass

class Trovebox404Error(Exception):
    """
    Indicates that an Http 404 error code was received
    (resource not found)
    """
    pass
