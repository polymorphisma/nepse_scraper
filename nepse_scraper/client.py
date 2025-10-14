# nepse_scraper/client.py

import logging
from typing import Any, Dict, List, Optional, Union

from .core import NepseAPISession
from .endpoints import api_dict

logger = logging.getLogger(__name__)


class NepseScraper:
    """
    The main client for interacting with the Nepal Stock Exchange (NEPSE) API.
    """
    def __init__(self, verify_ssl: bool = True) -> None:
        """Initializes the client and the underlying API session."""
        self.session = NepseAPISession(verify_ssl=verify_ssl)
        self._security_map: Optional[Dict[str, int]] = None
        self._sector_map: Optional[Dict[str, int]] = None
        logger.info("NepseScraper client initialized.")

    # =========================================================================
    # Private Helper Methods
    # =========================================================================

    def _get_security_map(self) -> Dict[str, int]:
        """Internal helper to fetch all securities and return a symbol-to-id map."""
        if self._security_map is not None:
            logger.debug("Using cached security map.")
            return self._security_map

        logger.info("Fetching all security listings to build symbol-to-id map.")
        endpoint = api_dict['security_api']
        response = self.session.get(endpoint['api'])
        securities = response.json()
        self._security_map = {item.get('symbol'): item.get('id') for item in securities}
        return self._security_map

    def _resolve_ticker_ids(self, tickers: List[str]) -> Dict[str, int]:
        """Resolves a list of ticker symbols to their security IDs."""
        security_map = self._get_security_map()
        resolved_tickers = {s: security_map.get(s) for s in tickers if security_map.get(s)}
        if len(resolved_tickers) != len(tickers):
            missing = sorted(list(set(tickers).difference(resolved_tickers.keys())))
            logger.error(f"Could not find security IDs for the following tickers: {missing}")
            raise ValueError(f"Ticker(s) not found: {missing}")
        return resolved_tickers

    # =========================================================================
    # Public API Methods
    # =========================================================================

    def is_market_open(self) -> bool:
        """
        Checks if the NEPSE market is currently open.

        Returns:
            bool: True if the market is open, False otherwise.
        """
        logger.info("Checking market status.")
        endpoint = api_dict['marketopen_api']
        response = self.session.get(endpoint['api'])
        return response.json().get('isOpen', 'CLOSE') == 'OPEN'

    def get_today_price(self, business_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get today's trading data from the Nepal Stock Exchange (NEPSE).

        Args:
            business_date (str, optional): The date for which trading data should be retrieved in "YYYY-MM-DD" format. 
                                           Defaults to None, which retrieves data for the latest trading day.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a security's price data for the day.
        """
        logger.info(f"Fetching today's price for date: {business_date or 'latest'}")
        endpoint = api_dict['today_price_api']
        params = {"page": "0", "size": "500", "businessDate": business_date}
        response = self.session.post(endpoint['api'], params=params)
        return response.json().get('content', [])

    def get_top_stocks(self, category: str, show_all: bool = False) -> List[Dict[str, Any]]:
        """
        Fetches top stocks based on a category (e.g., gainers, losers, turnover).

        Args:
            category (str): The category of top stocks to fetch. Valid options are:
                            'top_gainer', 'top_loser', 'top_turnover', 'top_trade', 'top_transaction'.
            show_all (bool): If True, fetches all stocks in the category, not just the top ten. Defaults to False.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the top stocks.

        Raises:
            ValueError: If an invalid category is provided.
        """
        logger.info(f"Fetching top stocks for category: {category}, show_all: {show_all}")
        valid_categories = ('top_gainer', 'top_loser', 'top_turnover', 'top_trade', 'top_transaction')
        if category not in valid_categories:
            raise ValueError(f"Invalid category: {category}. Must be one of {valid_categories}")
        
        endpoint = api_dict[category]
        params = {'all': str(show_all).lower()}
        response = self.session.get(endpoint['api'], params=params)
        return response.json()

    def get_ticker_info(self, ticker: Union[str, List[str]]) -> Union[Dict[str, Any], Dict[str, Dict[str, Any]]]:
        """
        Retrieve all the information for one or more tickers from Nepse.

        Args:
            ticker (Union[str, List[str]]): A single ticker symbol as a string or a list of ticker symbols.

        Returns:
            Union[Dict[str, Any], Dict[str, Dict[str, Any]]]: 
                If a single ticker is provided, returns a dictionary with its information.
                If a list of tickers is provided, returns a dictionary with tickers as keys and their info as values.

        Raises:
            ValueError: If the provided ticker is not found in NEPSE or if no ticker is provided.
        """
        if not ticker:
            raise ValueError('Ticker is required.')
            
        ticker_list = [ticker.upper()] if isinstance(ticker, str) else [t.upper() for t in ticker]
        logger.info(f"Fetching ticker info for: {ticker_list}")
        
        ticker_ids = self._resolve_ticker_ids(ticker_list)
        endpoint_info = api_dict['ticker_info_api']
        base_path = endpoint_info['api']
        results = {}

        for symbol, security_id in ticker_ids.items():
            path = f"{base_path}/{security_id}"
            response = self.session.post(path, which_payload='stock-live')
            results[symbol] = response.json()
            
        return results[ticker_list[0]] if len(ticker_list) == 1 else results

    def get_live_trades(self) -> List[Dict[str, Any]]:
        """
        Fetches the live market trades if the market is open.

        Returns:
            List[Dict[str, Any]]: A list of live trade data, or an empty list if the market is closed.
        """
        if not self.is_market_open():
            logger.warning("Attempted to get live trades while market is closed.")
            return []
            
        logger.info("Fetching live trades.")
        endpoint = api_dict['stock_live_api']
        response = self.session.post(endpoint['api'], which_payload='stock-live')
        return response.json()

    def get_indices_history(self, index_id: int, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Fetches the historical data for a given index ID within a date range.

        Args:
            index_id (int): The ID of the index to fetch (e.g., 58 for NEPSE Index).
            start_date (str): The start date in "YYYY-MM-DD" format.
            end_date (str): The end date in "YYYY-MM-DD" format.

        Returns:
            List[Dict[str, Any]]: A list of historical data points for the index.
        """
        logger.info(f"Fetching historical data for index ID: {index_id}")
        endpoint = api_dict['head_indices_api']
        path = f"{endpoint['api']}/{index_id}"
        params = {'startDate': start_date, 'endDate': end_date}
        response = self.session.get(path, params=params)
        return response.json()

    def get_sectorwise_summary(self) -> List[Dict[str, Any]]:
        """
        Retrieve the sector-wise summary from the Nepal Stock Exchange (NEPSE).

        Returns:
            List[Dict[str, Any]]: A JSON response from the NEPSE API containing the sector-wise summary.
        """
        logger.info("Fetching sector-wise summary.")
        endpoint = api_dict['sectorwise_summary_api']
        response = self.session.get(endpoint['api'])
        return response.json()

    def get_market_summary_history(self) -> List[Dict[str, Any]]:
        """
        Retrieve the market summary history from the Nepal Stock Exchange (NEPSE).

        Returns:
            List[Dict[str, Any]]: A JSON response containing the historical market summary.
        """
        logger.info("Fetching historical market summary.")
        endpoint = api_dict['market_summary_history_api']
        response = self.session.get(endpoint['api'])
        return response.json()

    def get_company_disclosures(self) -> List[Dict[str, Any]]:
        """
        Retrieve the latest news and announcements (disclosures) from NEPSE.

        Returns:
            List[Dict[str, Any]]: A list of news and announcements.
        """
        logger.info("Fetching company disclosures.")
        endpoint = api_dict['disclosure']
        response = self.session.get(endpoint['api'])
        return response.json().get('news', [])

    def get_market_summary(self) -> Dict[str, Any]:
        """
        Retrieve today's market summary from the Nepal Stock Exchange (NEPSE).

        Returns:
            Dict[str, Any]: A dictionary containing the current market summary.
        """
        logger.info("Fetching current market summary.")
        endpoint = api_dict['market_summary_api']
        response = self.session.get(endpoint['api'])
        return response.json()

    def get_all_securities(self) -> List[Dict[str, Any]]:
        """
        Retrieve a list of all listed securities on the NEPSE.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each with details of a security.
        """
        logger.info("Fetching all securities.")
        endpoint = api_dict['security_api']
        response = self.session.get(endpoint['api'])
        return response.json()

    def get_market_cap(self) -> List[Dict[str, Any]]:
        """
        Retrieve market capitalization data from the Nepal Stock Exchange (NEPSE).

        Returns:
            List[Dict[str, Any]]: A list containing market capitalization data.
        """
        logger.info("Fetching market capitalization data.")
        endpoint = api_dict['marketcap_api']
        response = self.session.get(endpoint['api'])
        return response.json()

    def get_brokers(self, member_name: str = "", contact_person: str = "", contact_number: str = "", member_code: str = "", province_id: int = 0, district_id: int = 0, municipality_id: int = 0) -> List[Dict[str, Any]]:
        """
        Fetches a list of all registered brokers from NEPSE with optional filters.

        Args:
            member_name (str, optional): The name of the broker member. Defaults to "".
            contact_person (str, optional): The contact person name of the broker. Defaults to "".
            contact_number (str, optional): The contact number of the broker. Defaults to "".
            member_code (str, optional): The code of the broker member. Defaults to "".
            province_id (int, optional): The ID of the province where the broker is located. Defaults to 0.
            district_id (int, optional): The ID of the district where the broker is located. Defaults to 0.
            municipality_id (int, optional): The ID of the municipality where the broker is located. Defaults to 0.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing broker information.
        """
        logger.info(f"Fetching list of brokers with filters: member_name={member_name}, contact_person={contact_person}, contact_number={contact_number}, member_code={member_code}, province_id={province_id}, district_id={district_id}, municipality_id={municipality_id}")
        
        endpoint = api_dict['broker_api']
        
        # Construct parameters with the filters
        params = {
            "memberName": member_name,
            "contactPerson": contact_person,
            "contactNumber": contact_number,
            "memberCode": member_code,
            "provinceId": province_id,
            "districtId": district_id,
            "municipalityId": municipality_id,
            "page": "0",  # Default pagination
            "size": "500"  # Default pagination
        }
        
        # Send a GET request to the API endpoint with the parameters
        response = self.session.get(endpoint['api'], params=params)
        
        # Return the JSON response
        return response.json()

    def get_sectors(self) -> List[Dict[str, Any]]:
        """
        Retrieve details of all sectors listed in the NEPSE.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing sector details.
        """
        logger.info("Fetching list of all sectors.")
        endpoint = api_dict['sector_api']
        response = self.session.get(endpoint['api'])
        return response.json()

    def get_sector_indices(self) -> List[Dict[str, Any]]:
        """
        Retrieve index information for all sectors listed in the NEPSE.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing sector index data.
        """
        logger.info("Fetching list of all sector indices.")
        endpoint = api_dict['sector_index_api']
        response = self.session.get(endpoint['api'])
        return response.json()
        
    def get_live_indices(self, index_id: int = 58) -> List[Dict[str, Any]]:
        """
        Retrieve live indices data. If the market is closed, it retrieves the last trading day's index data.

        Args:
            index_id (int): The ID for the index. Defaults to 58 (NEPSE Index).
                            Refer to NEPSE documentation for a full list of valid index IDs.

        Returns:
            List[Dict[str, Any]]: A list containing time-series data for the index.
            
        Raises:
            ValueError: If the provided index ID is not within a valid range.
        """
        if not (51 <= index_id <= 67):
             raise ValueError(f"'{index_id}' is not a valid index ID. Must be between 51 and 67.")

        logger.info(f"Fetching live data for index ID: {index_id}")
        endpoint = api_dict['indices_live_api']
        path = f"{endpoint['api']}/{index_id}"
        response = self.session.post(path, which_payload='sector-live')
        return response.json()

    def get_ticker_contact(self, ticker: Union[str, List[str]]) -> Union[Dict[str, Any], Dict[str, Dict[str, Any]]]:
        """
        Retrieve contact information for one or more tickers from Nepse.

        Args:
            ticker (Union[str, List[str]]): A single ticker symbol or a list of ticker symbols.

        Returns:
            Union[Dict[str, Any], Dict[str, Dict[str, Any]]]: 
                Contact information for a single ticker, or a dictionary of contact information keyed by ticker symbol.

        Raises:
            ValueError: If the ticker is not found or no ticker is provided.
        """
        if not ticker:
            raise ValueError('Ticker is required.')

        ticker_list = [ticker.upper()] if isinstance(ticker, str) else [t.upper() for t in ticker]
        logger.info(f"Fetching contact info for: {ticker_list}")

        ticker_ids = self._resolve_ticker_ids(ticker_list)
        endpoint = api_dict['ticker_contact_api']
        base_path = endpoint['api']
        results = {}

        for symbol, security_id in ticker_ids.items():
            path = f"{base_path}/{security_id}"
            response = self.session.get(path)
            results[symbol] = response.json()

        return results[ticker_list[0]] if len(ticker_list) == 1 else results

    def get_ticker_price_history(self, ticker: str, start_date: str, end_date: str, page: int = 0, size: int = 500) -> List[Dict[str, Any]]:
        """
        Fetches the price history for a given ticker within a date range.

        Args:
            ticker (str): The ticker symbol for the security.
            start_date (str): The start date in "YYYY-MM-DD" format.
            end_date (str): The end date in "YYYY-MM-DD" format.
            page (int): The page number for pagination.
            size (int): The number of records per page.

        Returns:
            List[Dict[str, Any]]: A list of price history data for the ticker.
        """
        ticker_upper = ticker.upper()
        logger.info(f"Fetching price history for ticker: {ticker_upper}")
        
        ticker_id = self._resolve_ticker_ids([ticker_upper])[ticker_upper]
        endpoint = api_dict['ticker_price_api']
        
        path = f"{endpoint['api']}/{ticker_id}"
        
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'page': page,
            'size': size
        }
        response = self.session.get(path, params=params)
        return response.json()

    # =========================================================================
    # NEW METHODS ADDED
    # =========================================================================

    def get_nepse_index(self) -> List[Dict[str, Any]]:
        """
        Retrieves the NEPSE index and sub-indices data.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing an index.
        """
        logger.info("Fetching NEPSE index data.")
        endpoint = api_dict['nepse_index_api']
        response = self.session.get(endpoint['api'])
        return response.json()

    def get_security_daily_trade_stat(self, ticker: str) -> Dict[str, Any]:
        """
        Retrieves daily trade statistics for a specific security.

        Args:
            ticker (str): The ticker symbol of the security.

        Returns:
            Dict[str, Any]: A dictionary containing the daily trade statistics.
        """
        ticker_upper = ticker.upper()
        logger.info(f"Fetching daily trade statistics for ticker: {ticker_upper}")
        ticker_id = self._resolve_ticker_ids([ticker_upper])[ticker_upper]
        endpoint = api_dict['security_daily_trade_stat_api']
        path = f"{endpoint['api']}/{ticker_id}"
        response = self.session.get(path)
        return response.json()

    def get_securities_list(self) -> List[Dict[str, Any]]:
        """
        Retrieves a simplified list of all securities.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a security.
        """
        logger.info("Fetching the simplified list of securities.")
        endpoint = api_dict['securities_list_api']
        response = self.session.get(endpoint['api'])
        return response.json()

    def get_supply_demand(self, show_all: bool = False) -> List[Dict[str, Any]]:
        """
        Retrieves the top supply and demand data.

        Args:
            show_all (bool): If True, fetches all supply/demand data, not just the top. Defaults to False.

        Returns:
            List[Dict[str, Any]]: A list of supply and demand data.
        """
        logger.info(f"Fetching supply and demand data, show_all: {show_all}")
        endpoint = api_dict['supply_demand_api']
        params = {'all': str(show_all).lower()}
        response = self.session.get(endpoint['api'], params=params)
        return response.json()


    def get_top_by_trade_quantity(self, show_all: bool = False) -> List[Dict[str, Any]]:
        """
        Retrieves the top securities ranked by trade quantity.

        Args:
            show_all (bool): If True, fetches all data, not just the top ten. Defaults to False.

        Returns:
            List[Dict[str, Any]]: A list of securities ranked by trade quantity.
        """
        logger.info(f"Fetching top stocks by trade quantity, show_all: {show_all}")
        endpoint = api_dict['top_trade_qty_api']
        params = {'all': str(show_all).lower()}
        response = self.session.get(endpoint['api'], params=params)
        return response.json()

    def get_trading_average(self, n_days: int = 120, business_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve the trading average for a specified number of days.

        Args:
            n_days (int): The number of days to include in the trading average calculation (must be between 1 and 180). 
                          Defaults to 120.
            business_date (str, optional): The end date for the calculation in "YYYY-MM-DD" format. 
                                           Defaults to the latest date.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the trading average data.
            
        Raises:
            ValueError: If n_days is not between 1 and 180.
        """
        if not (1 <= n_days <= 180):
            raise ValueError("n_days must be between 1 and 180.")

        logger.info(f"Fetching trading average for {n_days} days, ending on {business_date or 'latest'}")
        endpoint = api_dict['trading_average_api']
        
        params = {
            "nDays": n_days,
            "businessDate": business_date,
            "page": "0", 
            "size": "500" # Use a large size to get all data
        }
        
        response = self.session.get(endpoint['api'], params=params)
        return response.json()


    def get_notices(self) -> List[Dict[str, Any]]:
        """
        Retrieves general notices from NEPSE.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a notice.
        """
        logger.info("Fetching general notices.")
        endpoint = api_dict['notice_api']
        response = self.session.get(endpoint['api'])
        return response.json()

    def get_info_officers(self) -> List[Dict[str, Any]]:
        """
        Retrieves a list of information officers from NEPSE.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing an information officer.
        """
        logger.info("Fetching list of information officers.")
        endpoint = api_dict['info_officer_api']
        response = self.session.get(endpoint['api'])
        return response.json()