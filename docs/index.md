# Documentation
## API References
- [Nepse scraper](#nepse-scraper)
  - [get_today_price()](#get-today-price)
  - [get_head_indices()](#get-head-indices)
  - [get_sectorwise_summary()](#get-sectorwise-summary)
  - [get_market_summary()](#get-market-summary)
  - [get_news()](#get-news)
  - [get_top_gainer()](#get-top-gainer)
  - [get_top_loser()](#get-top-loser)
  - [get_top_turnover()](#get-top-turnover)
  - [get_top_trade()](#get-top-trade)
  - [get_top_transaction()](#get-top-transaction)



### NEPSE SCRAPER
#### Get today price
    Get today's trading data for from Nepal Stock Exchange (NEPSE).

    This method queries the NEPSE API to retrieve the trading data for the current date or a specified date.
    The data is returned as a json response.

    Args:
        date_ (str, optional): The date for which trading data should be retrieved in "YYYY-MM-DD" format. Defaults to None,
            which retrieves data for the current date.(Date should be from today to one year prior)

    Returns:
        json: A json response returned by NEPSE API.

    Raises:
        ValueError: If the date string is not in the "YYYY-MM-DD" format.
```py
from nepse_scraper import Nepse_scraper

request_obj = Nepse_scraper()
# get last trading date's price
value = request_obj.get_today_price()

## or
# get's price of provided date
# Note: nepse only gives access data from today date and one year prior
## example: if today date is '2023-05-07' you can scrape data from '2022-05-07 to '2023-05-07'
value = request_obj.get_today_price('2023-05-07')
```

#### Get head indices
    Retrieve the head indices data from the Nepal Stock Exchange (NEPSE).

    This method reads the head indices file located at paths.headindices_path and queries the NEPSE API to retrieve
    data. The data is returned as a dictionary containing index as keys and the corresponding index data as values.

    Returns:
        dict: A dictionary containing the latest data for each head index, with index as keys and response as a value.
        
        Example:
        58:{data from one year prior from today date} # 58 -> this is nepse code in nepalstock.com.np

```py
from nepse_scraper import Nepse_scraper

request_obj = Nepse_scraper()
value = request_obj.get_head_indices()
```


#### Get sectorwise summary
    Retrieve the sector-wise summary from a given business date from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the sector-wise summary for a given business date.
        If no date is specified, the default behavior is to retrieve the sector-wise summary for the current business date.
        The sector-wise summary is returned as a json response from NEPSE API.

        Args:
            date_ (str, optional): The business date for which to retrieve the sector-wise summary, in YYYY-MM-DD format.
                Defaults to None, in which case the sector-wise summary for all the data avialable on {nepalstock.com.np}.

        Returns:
            json: A json response returned by NEPSE API.

```py
from nepse_scraper import Nepse_scraper

request_obj = Nepse_scraper()
value = request_obj.get_sectorwise_summary()

## or
# get sectorwise summary data from provided date
# Note: nepse only gives access data from today date and one year prior
## example: if today date is '2023-05-07' you can get data from '2022-05-07 to '2023-05-07'
value = request_obj.get_sectorwise_summary('2023-05-07')
```


#### Get Market summary
    Retrieve the market summary from a given business date from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the market summary for a given business date.
        If no date is specified, the default behavior is to retrieve the market summary for the current business date.
        The market summary is returned as a dictionary with various statistics as keys and corresponding values.

        Args:
            date_ (str, optional): The business date for which to retrieve the market summary, in YYYY-MM-DD format.
            Defaults to None, in which case the market summary for the current business date is retrieved.

        Returns:
            json: A json response returned by NEPSE API.

```py
from nepse_scraper import Nepse_scraper

request_obj = Nepse_scraper()
value = request_obj.get_market_summary()

## or
# get sectorwise summary data from provided date
# Note: nepse only gives access data from today date and one year prior
## example: if today date is '2023-05-07' you can get data from '2022-05-07 to '2023-05-07'
value = request_obj.get_market_summary('2023-05-07')
```


#### Get news
    Retrieve the latest news and announcements from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the latest news and announcements regarding listed companies.
        The news and announcements are returned as a json.

        Returns:
            json: A json response returned by NEPSE API.


```py
from nepse_scraper import Nepse_scraper

request_obj = Nepse_scraper()
value = request_obj.get_news()
```

#### Get top gainer
    Retrieve the all the gains of ticker in terms of share price from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the all the gains of ticker in terms of share price.
        The all the gains of ticker are returned as a json.

        Returns:
            json: A json response returned by NEPSE API.



```py
from nepse_scraper import Nepse_scraper

request_obj = Nepse_scraper()
value = request_obj.get_top_gainer()
```

#### Get top loser
    Retrieve the all the loser of ticker in terms of share price from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the all the loser of ticker in terms of share price.
        The all the loser of ticker are returned as a json.

        Returns:
            json: A json response returned by NEPSE API.


```py
from nepse_scraper import Nepse_scraper

request_obj = Nepse_scraper()
value = request_obj.get_top_loser()
```


#### Get top turnover
    Retrieve the all the turnover of ticker in terms of share price from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the all the turnover of ticker in terms of share price.
        The all the turnover of ticker are returned as a json.

        Returns:
            json: A json response returned by NEPSE API.


```py
from nepse_scraper import Nepse_scraper

request_obj = Nepse_scraper()
value = request_obj.get_top_turnover()
```



#### Get top trade
    Retrieve the all the trade of ticker in terms of share price from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the all the trade of ticker in terms of share price.
        The all the trade of ticker are returned as a json.

        Returns:
            json: A json response returned by NEPSE API.


```py
from nepse_scraper import Nepse_scraper

request_obj = Nepse_scraper()
value = request_obj.get_top_trade()
```



#### Get top transaction
    Retrieve the all the transaction of ticker in terms of share price from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the all the transaction of ticker in terms of share price.
        The all the transaction of ticker are returned as a json.

        Returns:
            json: A json response returned by NEPSE API.


```py
from nepse_scraper import Nepse_scraper

request_obj = Nepse_scraper()
value = request_obj.get_top_transaction()
```


