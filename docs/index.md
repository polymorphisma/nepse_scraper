# Documentation
## API References
- [Nepse scraper](#nepse-scraper)
  - [get_today_price()](#get-today-price)

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

