class DonutSMPError(Exception):
    """Raised when donutsmp cannot handle a query, Very likely could not find username"""
    pass

class UnauthorizedRequest(Exception):
    """Raised when donutsmp returns a 401 unauthorized"""
    pass

class UnexpectedError(Exception):
    """Raised when there is an unexpected api response status"""
    pass