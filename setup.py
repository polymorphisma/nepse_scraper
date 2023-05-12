from setuptools import setup, find_packages
from os import path

current_dir = path.abspath(path.dirname(__file__))

VERSION = '0.1.7'
DESCRIPTION = 'Python Scraper for Nepse'

with open(path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
    name="nepse_scraper",
    version=VERSION,
    author="Shrawan Sunar",
    author_email="shrawansunar.6@gmail.com",
    package_data={'nepse_scraper': ['*.wasm']},
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    url='https://github.com/polymorphisma/nepse_scraper/',  
    install_requires=['requests','urllib3','wasmtime', 'retrying'],
    keywords=['python', 'nepse data', 'nepse scraper','nepse', 'scraping'],
    download_url="https://github.com/polymorphisma/nepse_scraper/archive/refs/tags/v_01.7.tar.gz",
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
