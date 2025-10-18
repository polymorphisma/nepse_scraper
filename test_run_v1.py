# run_tests.py

import datetime
from nepse_scraper.client import NepseScraper

# --- Test Configuration ---
VALID_TICKER = 'NABIL'
VALID_INDEX_ID = 58
END_DATE = datetime.date.today()
START_DATE = END_DATE - datetime.timedelta(days=7)

# --- Test Plan ---
TEST_CASES = [
    # General Status and Data
    {
        "name": "Check if Market is Open",
        "method": "is_market_open",
        "kwargs": {},
        "validator": lambda r: isinstance(r, bool)
    },
    {
        "name": "Get Today's Prices",
        "method": "get_today_price",
        "kwargs": {},
        "validator": lambda r: isinstance(r, list)
    },
    # Top Stocks
    {
        "name": "Get Top Gainers",
        "method": "get_top_stocks",
        "kwargs": {"category": "top_gainer"},
        "validator": lambda r: isinstance(r, list)
    },
    {
        "name": "Get All Losers (show_all=True)",
        "method": "get_top_stocks",
        "kwargs": {"category": "top_loser", "show_all": True},
        "validator": lambda r: isinstance(r, list)
    },
    # Ticker-Specific Information
    {
        "name": "Get Ticker Info",
        "method": "get_ticker_info",
        "kwargs": {"ticker": VALID_TICKER},
        "validator": lambda r: isinstance(r, dict) and 'securityDailyTradeDto' in r
    },
    {
        "name": "Get Ticker Price History",
        "method": "get_ticker_price_history",
        "kwargs": {"ticker": VALID_TICKER, "start_date": START_DATE.strftime("%Y-%m-%d"), "end_date": END_DATE.strftime("%Y-%m-%d")},
        "validator": lambda r: isinstance(r, dict) and 'content' in r and isinstance(r['content'], list)
    },
    {
        "name": "Get Ticker Contact Info",
        "method": "get_ticker_contact",
        "kwargs": {"ticker": VALID_TICKER},
        "validator": lambda r: isinstance(r, dict) and 'companyName' in r
    },
    # Market and Sector Data
    {
        "name": "Get Sector-wise Summary",
        "method": "get_sectorwise_summary",
        "kwargs": {},
        "validator": lambda r: isinstance(r, list) and len(r) > 0
    },
    {
        "name": "Get Company Disclosures",
        "method": "get_company_disclosures",
        "kwargs": {},
        "validator": lambda r: isinstance(r, list)
    },
    {
        "name": "Get Market Summary",
        "method": "get_market_summary",
        "kwargs": {},
        "validator": lambda r: isinstance(r, list) and len(r) > 0
    },
    {
        "name": "Get All Detailed Securities",
        "method": "get_all_securities",
        "kwargs": {},
        "validator": lambda r: isinstance(r, list) and len(r) > 200
    },
    {
        "name": "Get Broker List",
        "method": "get_brokers",
        "kwargs": {},
        "validator": lambda r: isinstance(r, list)
    },
    # Index Data
    {
        "name": "Get Live Index Data",
        "method": "get_live_indices",
        "kwargs": {"index_id": VALID_INDEX_ID},
        "validator": lambda r: isinstance(r, list)
    },
    {
        "name": "Get NEPSE Index Overview",
        "method": "get_nepse_index",
        "kwargs": {},
        "validator": lambda r: isinstance(r, list) and len(r) > 0
    },
    # Newly Added Endpoints from JS Analysis
    {
        "name": "Get Security Daily Trade Stat",
        "method": "get_security_daily_trade_stat",
        "kwargs": {"ticker": VALID_TICKER},
        "validator": lambda r: isinstance(r, dict) or (isinstance(r, list) and len(r) == 0)
    },
    {
        "name": "Get Supply and Demand",
        "method": "get_supply_demand",
        "kwargs": {"show_all": True},
        "validator": lambda r: isinstance(r, dict) and 'supplyList' in r
    },
    {
        "name": "Get Top by Trade Quantity",
        "method": "get_top_by_trade_quantity",
        "kwargs": {},
        "validator": lambda r: isinstance(r, list)
    },
    # --- Final Sweep of Untested Functions ---
    {
        "name": "Get Indices History",
        "method": "get_indices_history",
        "kwargs": {"index_id": VALID_INDEX_ID, "start_date": START_DATE.strftime("%Y-%m-%d"), "end_date": END_DATE.strftime("%Y-%m-%d")},
        # FIX: Check for the 'content' key.
        "validator": lambda r: isinstance(r, dict) and 'content' in r and isinstance(r['content'], list)
    },
    {
        "name": "Get Market Summary History",
        "method": "get_market_summary_history",
        "kwargs": {},
        "validator": lambda r: isinstance(r, list)
    },
    {
        "name": "Get Market Cap",
        "method": "get_market_cap",
        "kwargs": {},
        "validator": lambda r: isinstance(r, list)
    },
    {
        "name": "Get Sectors",
        "method": "get_sectors",
        "kwargs": {},
        # FIX: Check for the 'sectors' key.
        "validator": lambda r: isinstance(r, dict) and 'sectors' in r and isinstance(r['sectors'], list)
    },
    {
        "name": "Get Sector Indices",
        "method": "get_sector_indices",
        "kwargs": {},
        "validator": lambda r: isinstance(r, list)
    },
    {
        "name": "Get Simplified Securities List",
        "method": "get_securities_list",
        "kwargs": {},
        "validator": lambda r: isinstance(r, list)
    },
    {
        "name": "Get Trading Average",
        "method": "get_trading_average",
        "kwargs": {}, # Use default values (120 days)
        "validator": lambda r: isinstance(r, list)
    },

    {
        "name": "Get General Notices",
        "method": "get_notices",
        "kwargs": {},
        "validator": lambda r: isinstance(r, list)
    },
    {
        "name": "Get Information Officers",
        "method": "get_info_officers",
        "kwargs": {},
        "validator": lambda r: isinstance(r, dict)
    },
    # Test case for the resgister endpoint

    {
        "name": "Register and Call a Custom Endpoint",
        "method": "call_endpoint",
        # The 'setup' key is a special instruction for our test runner.
        # It will execute this lambda function before calling the main method.
        "setup": lambda scraper: scraper.register_endpoint(
            name='is_open_test', 
            path='/api/nots/nepse-data/market-open', 
            method='GET'
        ),
        "kwargs": {"name": "is_open_test"},
        "validator": lambda r: isinstance(r, dict) and 'isOpen' in r
    },
]


def run_tests():
    print("Initializing NepseScraper client for integration tests...")
    scraper = NepseScraper(verify_ssl=False) # Setting verify_ssl=False to hide warnings for now
    passed_count = 0
    failed_count = 0

    print(f"\nRunning {len(TEST_CASES)} tests...\n" + "="*40)

    for test in TEST_CASES:
        name = test["name"]
        method_name = test["method"]
        kwargs = test["kwargs"]
        validator = test["validator"]
        
        print(f"[*] Testing: {name} (Method: {method_name})")

        try:
            # Handling the option setup
            if "setup" in test:
                test["setup"](scraper)

            method_to_call = getattr(scraper, method_name)
            response = method_to_call(**kwargs)
            
            if validator(response):
                print(f"    [PASSED]\n")
                passed_count += 1
            else:
                print(f"    [FAILED] - Validation failed. Response was: {str(response)[:100]}...\n")
                failed_count += 1

        except Exception as e:
            print(f"    [FAILED] - An exception occurred: {e}\n")
            failed_count += 1
        finally: 
            print("="*40 + f"\nTest Summary: {passed_count} PASSED, {failed_count} FAILED\n")


if __name__ == "__main__":
    run_tests()