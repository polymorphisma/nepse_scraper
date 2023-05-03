# _NEPSE_SCRAPER_

Welcome to **nepse_scraper**, the Python module that provides easy access to the Nepal Stock Exchange (NEPSE) API. With just a few lines of code, you can retrieve today's stock prices, market summary, head indices and etc to help you make better investment decisions. The code is well-documented and organized, making it easy to understand and modify for your specific use case.

But that's not all! With the power of Python libraries such as **pandas**, you can quickly process the retrieved data and convert it into your desired format.

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
### Cloning 

```
git clone git@github.com:polymorphisma/nepse_scraper.git
```
#### Downloading Dependencies
```
pip install -r requirements.txt
```

_or_ 

```
pip install requests urllib3 wasmtime retrying
```

### Usage
```py
from nepse_scraper import Request_module

# create object from Request_module class
request_obj = Request_module()

# getting today's price from nepse
today_price = request_obj.get_today_price()
print(today_price)
```


### All Methods
- get_news()
- get_head_indices() 
- get_market_summary()
- get_sectorwise_summary()
- get_today_price() 
- is_trading_day()
- get_top_gainer() 
- get_top_loser() 
- get_top_trade() 
- get_top_transaction()
- get_top_turnover() 
- get_today_market_summary()
- get_security_detail()
- get_marketcap()
- get_trading_average()
- get_sector_detail()


## License

MIT

**Free Software, Hell Yeah!**
