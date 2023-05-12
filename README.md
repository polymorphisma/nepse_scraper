# Nepse scraper
> Python module that provides convenient access to the Nepal Stock Exchange (NEPSE) API, enabling developers and analysts to retrieve stock market data and improve investment decisions.

> If you're looking for more detailed documentation on how to use my project called "nepse_scraper," I would recommend checking out the project's GitHub page at [https://github.com/polymorphisma/nepse_scraper/].

# Table of content
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
  - [Using Pip](#using-pip)
- [Usage](#usage)
- [Documentation](/docs/index.md)
- [License](#license)

## Introduction
Welcome to **nepse_scraper**, the Python module that provides easy access to the Nepal Stock Exchange (NEPSE) API. With just a few lines of code, you can retrieve today's stock prices, market summary, head indices and etc to help you make better investment decisions. The code is well-documented and organized, making it easy to understand and modify for your specific use case.

**nepse_scraper** is open-source, which means you can contribute and improve the code by adding new functions to retrieve additional data, enhancing existing functions with more options, or improving the error handling and exception handling to make it more robust. Your contributions can help make **nepse_scraper** even more useful for developers and analysts who work with data from the Nepal Stock Exchange.

So what are you waiting for? Try out **nepse_scraper** and see how it can simplify your stock market analysis and investment strategies.


## Features
- Get Today Price
- Get Head Indices
- Get Market Summary
- Get Sector Summary
- Get Sector Detail
- Get Broker Details
- Get News
- Many More ....
<!-- - Get Top Gainer
- Get Top Loser
- Get Top Trade
- Get Top Transaction
- Get Top Turnover
- Get Today Market Summary
- Get Security Detail
- Get Marketcap
- Get Trading Average -->


## Installation

### Using Pip
```
pip install nepse-scraper
```


## Usage
```py
from nepse_scraper import Nepse_scraper

# create object from Nepse_scraper class
request_obj = Nepse_scraper()

# getting today's price from nepse
today_price = request_obj.get_today_price()
print(today_price)

# "Please refer to the documentation for more detailed usage instructions."
```


## License

MIT

**Free Software, Hell Yeah!**
