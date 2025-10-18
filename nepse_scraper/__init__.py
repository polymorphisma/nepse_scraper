from .client import NepseScraper

# Create an alias for the old class name to ensure full backward compatibility.
# Users who were using `from nepse_scraper import Nepse_scraper` will not have their code broken.
Nepse_scraper = NepseScraper

# Define what gets imported with `from nepse_scraper import *`
__all__ = ['NepseScraper', 'Nepse_scraper']