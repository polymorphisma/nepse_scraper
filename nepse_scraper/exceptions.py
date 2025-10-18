
class NepseScraperException(Exception):
    """Base exception for all nepse-scraper specific errors."""
    pass

class SSLCertVerificationError(NepseScraperException):
    """
    Raised when SSL certificate verification fails.
    
    This is often due to an incomplete certificate chain on the server or
    a corporate proxy. The recommended solution is to initialize the client
    with `verify_ssl=False`.
    """
    pass