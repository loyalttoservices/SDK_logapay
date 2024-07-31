
class LogApayException(Exception):
    """Base exception class"""
    pass


class APINotAuthenticated(LogApayException):
    """Raise when not authenticated"""
    pass
        
        
class APINotAuthorized(LogApayException):
    """Raise when not authorized to do request on"""
    pass