# Documentation

This document provides a detailed API reference for the most common methods available in `nepse-scraper`. For a complete and up-to-the-minute reference, please consult the docstrings within the source code.

## API Reference

### `NepseScraper`

This is the main client class used to interact with the NEPSE API.

**Initialization:**

```python
from nepse_scraper import NepseScraper

# It is highly recommended to initialize with SSL verification disabled
# due to a known issue with the NEPSE server's certificate chain.
scraper = NepseScraper(verify_ssl=False)
```

---

### Key Methods

#### `is_market_open()`

Checks if the NEPSE market is currently open.

- **Returns:** `bool` - `True` if the market is open, `False` otherwise.

```python
is_open = scraper.is_market_open()
print(f"Market is open: {is_open}")
```

---

#### `get_today_price()`

Get today's trading data for all securities from the Nepal Stock Exchange (NEPSE).

- **Args:**
    - `business_date (str, optional)`: The date in "YYYY-MM-DD" format. Defaults to the latest trading day.
- **Returns:** `List[Dict]` - A list of dictionaries, each representing a security's price data.

```python
# Get the latest trading day's prices
latest_prices = scraper.get_today_price()

# Get prices for a specific date
prices_for_date = scraper.get_today_price(business_date='2025-10-10')
```

---

#### `get_top_stocks()`

Fetches top stocks based on a category (e.g., gainers, losers, turnover).

- **Args:**
    - `category (str)`: Valid options are: `'top_gainer'`, `'top_loser'`, `'top_turnover'`, `'top_trade'`, `'top_transaction'`.
    - `show_all (bool)`: If `True`, fetches all stocks in the category, not just the top ten. Defaults to `False`.
- **Returns:** `List[Dict]` - A list of dictionaries representing the top stocks.

```python
# Get the top 10 gainers
top_gainers = scraper.get_top_stocks(category='top_gainer')

# Get all losers, not just the top 10
all_losers = scraper.get_top_stocks(category='top_loser', show_all=True)
```

---

#### `get_ticker_info()`

Retrieve all available information for one or more tickers.

- **Args:**
    - `ticker (Union[str, List[str]])`: A single ticker symbol as a string or a list of ticker symbols.
- **Returns:** `Dict` or `Dict[str, Dict]` - An information dictionary for a single ticker, or a dictionary of dictionaries keyed by ticker symbol for multiple tickers.

```python
# Get info for a single ticker
nabil_info = scraper.get_ticker_info('NABIL')

# Get info for multiple tickers at once
multi_info = scraper.get_ticker_info(['NABIL', 'NICA'])
```

---

#### `get_ticker_price_history()`

Fetches the price history for a given ticker within a date range.

- **Args:**
    - `ticker (str)`: The ticker symbol for the security.
    - `start_date (str)`: The start date in "YYYY-MM-DD" format.
    - `end_date (str)`: The end date in "YYYY-MM-DD" format.
- **Returns:** `Dict` - A dictionary containing the price history content.

```python
history = scraper.get_ticker_price_history(
    ticker='NABIL',
    start_date='2025-10-01',
    end_date='2025-10-14'
)
print(history.get('content'))
```

---

#### `get_company_disclosures()`

Retrieve the latest news and announcements (disclosures) from NEPSE.

- **Returns:** `List[Dict]` - A list of news and announcement items.

```python
news = scraper.get_company_disclosures()
```

---

#### `get_brokers()`

Fetches a list of all registered brokers from NEPSE, with optional filters.

- **Args:**
    - `**kwargs`: Optional filters like `member_name`, `member_code`, etc.
- **Returns:** `List[Dict]` - A list of dictionaries containing broker information.

```python
# Get all brokers
all_brokers = scraper.get_brokers()

# Find a specific broker by name
specific_broker = scraper.get_brokers(member_name='Agrawal Securities')
```