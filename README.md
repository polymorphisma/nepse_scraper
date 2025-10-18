
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/nepse-scraper?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/nepse-scraper)
[![PyPI version](https://badge.fury.io/py/nepse-scraper.svg)](https://badge.fury.io/py/nepse-scraper)

# Nepse Scraper

A robust and feature-complete Python client for the Nepal Stock Exchange (NEPSE) API.

`nepse-scraper` provides a clean, high-level interface to access real-time and historical stock market data, enabling developers, analysts, and investors to build powerful financial applications and analysis tools.

## Table of Contents
- [Installation](#installation)
- [Quick Start & Important SSL/TLS Note](#quick-start--important-ssltls-note)
- [Advanced Usage](#advanced-usage)
  - [Extensibility: Using Custom Endpoints](#extensibility-using-custom-endpoints)
- [Key Features](#key-features)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Installation

Install the package directly from PyPI:
```bash
pip install nepse-scraper
```

## Quick Start & Important SSL/TLS Note

Here's how to get started with just a few lines of code.

> ### **:warning: Important Note on SSL/TLS Verification**
> 
> The official NEPSE server has a known issue where it does not provide a complete SSL/TLS certificate chain. This will cause `SSLCertVerificationError` connection errors in most standard Python environments.
> 
> <span style="color:red">**It is highly recommended to initialize the client with `verify_ssl=False` to ensure a successful connection.**</span>
> 
> ```python
> from nepse_scraper import NepseScraper
> 
> # Recommended initialization:
> scraper = NepseScraper(verify_ssl=False)
> ```

### Basic Usage

```python
from nepse_scraper import NepseScraper

# 1. Initialize the client (with SSL verification disabled as recommended)
scraper = NepseScraper(verify_ssl=False)

# 2. Check if the market is open
is_open = scraper.is_market_open()
print(f"Is the NEPSE market open? {'Yes' if is_open else 'No'}")

# 3. Fetch today's price data for all companies
try:
    today_prices = scraper.get_today_price()
    if today_prices:
        print(f"\nFetched {len(today_prices)} records for today's price.")
        # Find and print the record for a specific symbol
        aclbsl_data = next((item for item in today_prices if item['symbol'] == 'ACLBSL'), None)
        if aclbsl_data:
            print("Example record for ACLBSL:")
            print(aclbsl_data)

except Exception as e:
    print(f"An error occurred: {e}")

# 4. Get detailed information for a specific ticker
nabil_info = scraper.get_ticker_info('NABIL')
print("\nFetched Ticker Info for NABIL:")
print(nabil_info.get('security', {}).get('securityName'))
```

## Advanced Usage

### Extensibility: Using Custom Endpoints

The NEPSE API may change or have undocumented endpoints. `nepse-scraper` allows you to dynamically register and call any endpoint at runtime.

```python
# 1. Initialize the client
scraper = NepseScraper(verify_ssl=False)

# 2. Register a new or custom endpoint
#    (Using an existing endpoint as an example with a new name)
scraper.register_endpoint(
    name='custom_market_status', 
    path='/api/nots/nepse-data/market-open', 
    method='GET'
)

# 3. Call your custom endpoint using the generic `call_endpoint` method
custom_response = scraper.call_endpoint(name='custom_market_status')
print("\nResponse from custom endpoint 'custom_market_status':")
print(custom_response)
```

## Key Features

- **Complete API Coverage**: Access to all major NEPSE endpoints.
- **Robust & Resilient**: Built-in smart retries for handling transient network and server errors.
- **Secure by Default**: Enforces secure SSL connections, with a clear, configurable option for known server/network issues.
- **Extensible**: Dynamically add and call new or undocumented API endpoints at runtime.
- **Modern Architecture**: Fully typed, decoupled, and built on a high-performance session-based core.
- **User-Friendly Errors**: Catches common connection problems and provides clear, actionable error messages.

### Available Data
- **Market Status**: Check if the market is open.
- **Live Data**: Get live trades and real-time index graphs.
- **Daily Data**: Fetch today's prices and market summaries.
- **Historical Data**: Access historical prices for tickers and indices.
- **Company Info**: Retrieve security details, contact information, and corporate disclosures/notices.
- **Top Stocks**: Get lists of top gainers, losers, turnover, trade volume, transactions, and more.
- **And much more...**

## Documentation


For a more detailed API reference and examples, please see the [**Documentation (`docs/index.md`)**](./docs/index.md).

The source code in `nepse_scraper/client.py` is also extensively documented with docstrings and type hints.

## Contributing

Contributions are welcome! Whether it's adding new features, improving documentation, or reporting bugs, please feel free to open an issue or submit a pull request on our [GitHub repository](https://github.com/polymorphisma/nepse_scraper/).

## License

This project is licensed under the MIT License. See the [LICENSE.txt](LICENSE.txt) file for details.

**Happy Cod1ng!**