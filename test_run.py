# test_run.py
import json
import logging

# Configure basic logging to see output from our library
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# --- 1. Test Backward Compatibility ---
# We import both names to ensure our alias in __init__.py works.
from nepse_scraper import NepseScraper, Nepse_scraper

def run_tests():
    """Runs a series of tests against the refactored scraper client."""

    print("--- Starting Nepse Scraper v1.0 Refactor Test ---")

    # --- 2. Test Initialization ---
    try:
        # We use the new name, but could also use Nepse_scraper
        print("\nInitializing client with SSL verification DISABLED due to server's incomplete chain.")
        scraper = NepseScraper(verify_ssl=False)
        print("\n[SUCCESS] Client initialized successfully.")
    except Exception as e:
        print(f"\n[FAILURE] Client failed to initialize: {e}")
        return # Stop if we can't even create the client

    # --- 3. Test a simple GET endpoint ---
    try:
        print("\nTesting: is_market_open()")
        is_open = scraper.is_market_open()
        print(f"[SUCCESS] Market is currently {'OPEN' if is_open else 'CLOSED'}.")
    except Exception as e:
        print(f"[FAILURE] is_market_open() failed: {e}")

    # --- 4. Test a simple POST endpoint ---
    try:
        print("\nTesting: get_today_price()")
        prices = scraper.get_today_price()
        # We check if we got a list and it's not empty (assuming it's a trading day)
        if isinstance(prices, list) and len(prices) > 0:
            print(f"[SUCCESS] get_today_price() returned {len(prices)} records.")
            print(f"   Example record: {json.dumps(prices[0], indent=2)}")
        elif isinstance(prices, list) and len(prices) == 0:
             print(f"[SUCCESS] get_today_price() returned 0 records (likely a holiday or off-hours).")
        else:
            print(f"[WARNING] get_today_price() returned an unexpected type: {type(prices)}")
    except Exception as e:
        print(f"[FAILURE] get_today_price() failed: {e}")

    # --- 5. Test a more complex POST endpoint ---
    try:
        print("\nTesting: get_ticker_info('NABIL')")
        ticker_info = scraper.get_ticker_info('NABIL')
        # Check for the nested symbol and name
        if isinstance(ticker_info, dict) and ticker_info.get('security', {}).get('symbol') == 'NABIL':
            print(f"[SUCCESS] get_ticker_info('NABIL') returned valid data.")
            print(f"   Security Name: {ticker_info.get('security', {}).get('securityName')}")
        else:
            print(f"[FAILURE] get_ticker_info('NABIL') returned unexpected data or structure.")
            print(json.dumps(ticker_info, indent=2))
    except Exception as e:
        print(f"[FAILURE] get_ticker_info('NABIL') failed: {e}")
        
    # --- 6. Test a helper-dependent endpoint ---
    try:
        print("\nTesting: get_top_ten_stocks('top-gainer')")
        top_gainers = scraper.get_top_stocks('top_gainer')
        if isinstance(top_gainers, list) and len(top_gainers) > 0:
            print(f"[SUCCESS] get_top_ten_stocks('top-gainer') returned {len(top_gainers)} records.")
            print(f"   Top Gainer: {json.dumps(top_gainers[0], indent=2)}")
        elif isinstance(top_gainers, list) and len(top_gainers) == 0:
            print(f"[SUCCESS] get_top_ten_stocks('top-gainer') returned 0 records.")
        else:
             print(f"[WARNING] get_top_ten_stocks('top-gainer') returned an unexpected type: {type(top_gainers)}")
    except Exception as e:
        print(f"[FAILURE] get_top_ten_stocks('top-gainer') failed: {e}")


if __name__ == "__main__":
    run_tests()
