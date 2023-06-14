from retrying import retry
from .apis import api_dict
import requests
from datetime import datetime, date
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import time
from wasmtime import Store, Module, Instance
import json
import os

import pkg_resources
WASM_FILE = pkg_resources.resource_filename(__name__, 'nepse.wasm')


# WASM_FILE = r'nepse.wasm'

ROOT_URL = 'https://www.nepalstock.com.np'


class TokenParser():
    def __init__(self):
        self.store = Store()
        module = Module.from_file(self.store.engine, WASM_FILE)
        instance = Instance(self.store, module, [])

        self.cdx = instance.exports(self.store)["cdx"]
        self.rdx = instance.exports(self.store)["rdx"]
        self.bdx = instance.exports(self.store)["bdx"]
        self.ndx = instance.exports(self.store)["ndx"]
        self.mdx = instance.exports(self.store)["mdx"]

    def parse_token_response(self, token_response):
        n = self.cdx(self.store, token_response['salt1'], token_response['salt2'],
                     token_response['salt3'], token_response['salt4'], token_response['salt5'])
        l = self.rdx(self.store, token_response['salt1'], token_response['salt2'],
                     token_response['salt4'], token_response['salt3'], token_response['salt5'])
        o = self.bdx(self.store, token_response['salt1'], token_response['salt2'],
                     token_response['salt4'], token_response['salt3'], token_response['salt5'])
        p = self.ndx(self.store, token_response['salt1'], token_response['salt2'],
                     token_response['salt4'], token_response['salt3'], token_response['salt5'])
        q = self.mdx(self.store, token_response['salt1'], token_response['salt2'],
                     token_response['salt4'], token_response['salt3'], token_response['salt5'])
        i = self.cdx(self.store, token_response['salt2'], token_response['salt1'],
                     token_response['salt3'], token_response['salt5'], token_response['salt4'])
        r = self.rdx(self.store, token_response['salt2'], token_response['salt1'],
                     token_response['salt3'], token_response['salt4'], token_response['salt5'])
        s = self.bdx(self.store, token_response['salt2'], token_response['salt1'],
                     token_response['salt4'], token_response['salt3'], token_response['salt5'])
        t = self.ndx(self.store, token_response['salt2'], token_response['salt1'],
                     token_response['salt4'], token_response['salt3'], token_response['salt5'])
        u = self.mdx(self.store, token_response['salt2'], token_response['salt1'],
                     token_response['salt4'], token_response['salt3'], token_response['salt5'])

        access_token = token_response['accessToken']
        refresh_token = token_response['refreshToken']

        parsed_access_token = access_token[0:n] + access_token[n+1:l] + access_token[l +
                                                                                     1:o] + access_token[o+1:p] + access_token[p+1:q] + access_token[q+1:]
        parsed_refresh_token = refresh_token[0:i] + refresh_token[i+1:r] + refresh_token[r +
                                                                                         1:s] + refresh_token[s+1:t] + refresh_token[t+1:u] + refresh_token[u+1:]

        return (parsed_access_token, parsed_refresh_token)


class PayloadParser():
    def __init__(self):
        self.dummyData = [147, 117, 239, 143, 157, 312, 161, 612, 512, 804, 411, 527, 170, 511, 421, 667, 764, 621, 301, 106, 133, 793, 411, 511, 312, 423, 344, 346, 653, 758, 342, 222, 236, 811, 711, 611, 122, 447, 128, 199, 183, 135, 489, 703, 800, 745, 152, 863,
                          134, 211, 142, 564, 375, 793, 212, 153, 138, 153, 648, 611, 151, 649, 318, 143, 117, 756, 119, 141, 717, 113, 112, 146, 162, 660, 693, 261, 362, 354, 251, 641, 157, 178, 631, 192, 734, 445, 192, 883, 187, 122, 591, 731, 852, 384, 565, 596, 451, 772, 624, 691]
        self.url = ROOT_URL + api_dict["marketopen_api"]["api"]
        self.method = api_dict["marketopen_api"]['method']
        self.payload = {}
        self.headers = {
            "authority": "www.nepalstock.com.np",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.5",
            "referer": "https://www.nepalstock.com.np",
            "sec-ch-ua": '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        }

    def return_payload(self, access_token_value, which=None):
        headers = {
            'Authorization': f'Salter {access_token_value[0]}', **self.headers}

        response = requests.request(
            self.method, self.url, headers=headers, data=self.payload, verify=False)
        given_id = json.loads(response.content)["id"]

        today = datetime.now().day

        payload_id = self.dummyData[given_id] + given_id + 2 * today

        if which == 'stock-live':
            return payload_id

        if which == 'sector-live':
            if payload_id % 10 < 5:
                index_value = 3
            else:
                index_value = 1
        else:
            if payload_id % 10 < 5:
                index_value = 1
            else:
                index_value = 3

        payload_id = payload_id + access_token_value[1].get(
            f"salt{index_value+1}") * today - access_token_value[1].get(f"salt{index_value}")

        return payload_id


class Nepse:
    """
    this is the main class which gets the data from nepse

    Paramaters:
        optional str: date_value
            which date data you want(only works for todays date to exact one year before time period)

    """

    def __init__(self):
        self.parser_obj = PayloadParser()
        self.token_parser = TokenParser()

        self.token_url = ROOT_URL + api_dict['authenticate_api']['api']
        self.token_method = api_dict['authenticate_api']['method']

        self.headers = {
            'Host': 'www.nepalstock.com.np',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.nepalstock.com.np/',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'Trailers',
        }

    def request_api(self, url, access_token, method='GET', which_payload=None, querystring=None, payload=None):
        """
        this method/fucnion returns the data form requested url in json format

        Parameters
            str: url
                url of the api you want to get data from

            str: access_token
                this can be generated from get_valid_token() function(only works if given get_valid_token() generated token)

            str: Method
                this is optional can pass 'POST', 'GET'
        Returns
            json: what
                returns the json file accured after requsting to the api
        """
        headers = {
            'Authorization': f'Salter {access_token[0]}', **self.headers}

        if payload == None:
            payload = {'id': self.parser_obj.return_payload(
                access_token, which=which_payload)}

        # Send the request with the given parameters
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=payload,
                params=querystring,
                verify=False
            )
            # shranavyawan
            # Raise an exception if the response status code is not successful
            response.raise_for_status()
            return response

        except Exception as exp:
            raise ValueError(f"Error sending request: {exp}")

    def get_valid_token(self):
        """
        IMP

        this function is used to generate the access token to by pass authantication of the nepalstock.com.np

        Parameters
            None
        Returns
            str: acess_token
        """
        header = self.headers
        disable_warnings(InsecureRequestWarning)

        token_response = requests.request(
            self.token_method, self.token_url, headers=header, verify=False).json()
        for salt_index in range(1, 6):
            token_response[f'salt{salt_index}'] = int(
                token_response[f'salt{salt_index}'])

        return [self.token_parser.parse_token_response(token_response)[0], token_response]

    def return_data(self, url, access_token, method='GET', which_payload=None,  querystring=None, payload=None):
        return self.request_api(method=method, url=url, access_token=access_token, which_payload=which_payload, querystring=querystring, payload=payload)


class Nepse_scraper:

    SLEEP_TIME = 3000  # -> wait time for every failed request(in milisecond)

    def __init__(self) -> None:
        self.nepse_obj = Nepse()
        self.desired_status = 200

    @retry(wait_fixed=SLEEP_TIME)
    def call_nepse_function(self, url, method,  querystring=None, payload=None, which_payload=None):
        try:
            access_token = self.nepse_obj.get_valid_token()
            response = self.nepse_obj.return_data(
                url, access_token=access_token, method=method, querystring=querystring, payload=payload, which_payload=which_payload)

            if response.status_code != self.desired_status:
                raise ValueError(
                    'Unexpected status code: {}'.format(response.status_code))
            return response.json()

        except Exception as exp:
            raise ValueError('Unexpected Error: {}'.format(exp))

    def _get_security(self):
        api = ROOT_URL + api_dict['security']['api']
        method = api_dict['security']['method']

        return self.call_nepse_function(url=api, method=method)

    def is_trading_day(self) -> bool:
        """
        Check if today is a trading day on the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to determine if today is a trading day or not.
        If today is a trading day, it returns True, otherwise it returns False.

        Returns:
            bool: True if today is a trading day, False otherwise.
        """
        api = ROOT_URL + api_dict['marketopen_api']['api']
        method = api_dict['marketopen_api']['method']

        response = self.call_nepse_function(url=api, method=method)

        date_ = response['asOf'].split('T')[0]

        if date_ != str(date.today()):
            return False

        return True

    def is_market_open(self) -> bool:
        """
        Check if today is a trading day on the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to determine if today is a trading day or not.
        If today is a trading day, it returns True, otherwise it returns False.

        Returns:
            bool: True if today is a trading day, False otherwise.
        """

        api = ROOT_URL + api_dict['marketopen_api']['api']
        method = api_dict['marketopen_api']['method']

        response = self.call_nepse_function(url=api, method=method)

        isOpen = response['isOpen']

        if isOpen != 'OPEN':
            return False

        return True

    def get_today_price(self, date_: str = None) -> json:
        """
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
        """
        api = ROOT_URL + api_dict['today_price_api']['api']
        method = api_dict['today_price_api']['method']

        querystring = {"page": "0", "size": "500", "businessDate": date_}

        return self.call_nepse_function(url=api, method=method, querystring=querystring)

    def get_head_indices(self) -> dict:
        """
        Retrieve the head indices data from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve data. The data is returned as a dictionary containing index as keys and the corresponding index data as values.

        Returns:
            dict: A dictionary containing the latest data for each head index, with index as keys and response as a value.
        """
        api = ROOT_URL + api_dict['head_indices_api']['api']
        method = api_dict['head_indices_api']['method']

        querystring = {"page": "0", "size": "500"}

        dicts = {}

        sector_index = self._get_sector_index()

        for val in sector_index:
            dicts[val['id']] = self.call_nepse_function(
                url=api + '/' + str(val['id']), method=method, querystring=querystring)

        return dicts

    def get_sectorwise_summary(self, date_: str = None) -> json:
        """
        Retrieve the sector-wise summary from a given business date from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the sector-wise summary for a given business date.
        If no date is specified, the default behavior is to retrieve the sector-wise summary for the current business date.
        The sector-wise summary is returned as a json response from NEPSE API.

        Args:
            date_ (str, optional): The business date for which to retrieve the sector-wise summary, in YYYY-MM-DD format.
                Defaults to None, in which case the sector-wise summary for all the data avialable on {nepalstock.com.np}.

        Returns:
            json: A json response returned by NEPSE API.
        """

        api = ROOT_URL + api_dict['sectorwise_summary_api']['api']
        method = api_dict['sectorwise_summary_api']['method']

        querystring = {"page": "0", "size": "500", "businessDate": date_}

        return self.call_nepse_function(url=api, method=method, querystring=querystring)

    def get_market_summary(self, date_: str = None) -> json:
        """
        Retrieve the market summary from a given business date from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the market summary for a given business date.
        If no date is specified, the default behavior is to retrieve the market summary for the current business date.
        The market summary is returned as a dictionary with various statistics as keys and corresponding values.

        Args:
            date_ (str, optional): The business date for which to retrieve the market summary, in YYYY-MM-DD format.
            Defaults to None, in which case the market summary for the current business date is retrieved.

        Returns:
            json: A json response returned by NEPSE API.
        """
        api = ROOT_URL + api_dict['market_summary_history_api']['api']
        method = api_dict['market_summary_history_api']['method']

        querystring = {"page": "0", "size": "500", "businessDate": date_}

        return self.call_nepse_function(url=api, method=method, querystring=querystring)

    def get_news(self) -> json:
        """
        Retrieve the latest news and announcements from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the latest news and announcements regarding listed companies.
        The news and announcements are returned as a json.

        Returns:
            json: A json response returned by NEPSE API.
        """
        api = ROOT_URL + api_dict['disclosure']['api']
        method = api_dict['disclosure']['method']

        return self.call_nepse_function(url=api, method=method)

    def get_top_gainer(self) -> json:
        """
        Retrieve the all the gains of ticker in terms of share price from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the all the gains of ticker in terms of share price.
        The all the gains of ticker are returned as a json.

        Returns:
            json: A json response returned by NEPSE API.
        """
        api = ROOT_URL + api_dict['top_gainer']['api']
        method = api_dict['top_gainer']['method']

        return self.call_nepse_function(url=api, method=method)

    def get_top_loser(self) -> json:
        """
        Retrieve the all the loser of ticker in terms of share price from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the all the loser of ticker in terms of share price.
        The all the loser of ticker are returned as a json.

        Returns:
            json: A json response returned by NEPSE API.
        """
        api = ROOT_URL + api_dict['top_loser']['api']
        method = api_dict['top_loser']['method']

        return self.call_nepse_function(url=api, method=method)

    def get_top_turnover(self) -> json:
        """
        Retrieve the all the turnover of ticker in terms of share price from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the all the turnover of ticker in terms of share price.
        The all the turnover of ticker are returned as a json.

        Returns:
            json: A json response returned by NEPSE API.
        """
        api = ROOT_URL + api_dict['top_turnover']['api']
        method = api_dict['top_turnover']['method']

        return self.call_nepse_function(url=api, method=method)

    def get_top_trade(self) -> json:
        """
        Retrieve the all the trade of ticker in terms of share price from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the all the trade of ticker in terms of share price.
        The all the trade of ticker are returned as a json.

        Returns:
            json: A json response returned by NEPSE API.
        """
        api = ROOT_URL + api_dict['top_trade']['api']
        method = api_dict['top_trade']['method']

        return self.call_nepse_function(url=api, method=method)

    def get_top_transaction(self) -> json:
        """
        Retrieve the all the transaction of ticker in terms of share price from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve the all the transaction of ticker in terms of share price.
        The all the transaction of ticker are returned as a json.

        Returns:
            json: A json response returned by NEPSE API.
        """
        api = ROOT_URL + api_dict['top_transaction']['api']
        method = api_dict['top_transaction']['method']

        return self.call_nepse_function(url=api, method=method)

    def get_today_market_summary(self) -> json:
        """
        Retrieve today's market summary from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve today's market summary, which includes information
        such as the current NEPSE index value, trading volume, and the number of transactions.

        Returns:
            json: A json response returned by NEPSE API.
        """
        api = ROOT_URL + api_dict['market_summary_api']['api']
        method = api_dict['market_summary_api']['method']

        return self.call_nepse_function(url=api, method=method)

    def get_all_security(self) -> json:
        """
        Retrieve security detail information from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve security detail information, which includes the
        names and codes of all listed securities on the NEPSE, along with their market prices and other
        relevant data.

        Returns:
            json: A json response returned by NEPSE API.
        """
        api = ROOT_URL + api_dict['security_api']['api']
        method = api_dict['security_api']['method']

        return self.call_nepse_function(url=api, method=method)

    def get_marketcap(self) -> json:
        """
        Retrieve market capitalization data from the Nepal Stock Exchange (NEPSE).

        This method queries the NEPSE API to retrieve market capitalization data for all listed securities
        on the NEPSE.

        Returns:
            json: A json response returned by NEPSE API.
        """
        api = ROOT_URL + api_dict['marketcap_api']['api']
        method = api_dict['marketcap_api']['method']

        return self.call_nepse_function(url=api, method=method)

    def get_trading_average(self, date_: str = None, n_days: int = 120) -> json:
        """
        Retrieve the trading average for the specified number of days ending on the given date (or today if date is not
        specified).

        Args:
            date_: A string representing the date (in YYYY-MM-DD format) for which to retrieve the trading average. If
                not specified, the method will retrieve the trading average for today.
            n_days: An integer representing the number of days to include in the trading average calculation. The default
                value is 120.
        Returns:
            json: A json response returned by NEPSE API.
        Raises:
            ValueError: If n_days is less than or equal to zero.
        """
        if n_days < 1 or n_days > 180:
            raise ValueError(r"n_days must be between 1 and 180")

        api = ROOT_URL + api_dict['trading_average_api']['api']
        method = api_dict['trading_average_api']['method']

        querystring = {"page": "0", "size": "500",
                       "businessDate": date_, "nDays": n_days}

        return self.call_nepse_function(url=api, method=method, querystring=querystring)

    def get_broker(self, member_name: str = "", contact_person: str = "", contact_number: str = "", member_code: str = "", province_id: int = 0, district_id: int = 0, municipality_id: int = 0):
        """
        Get broker information from NEPSE.

        Args:
            member_name (str, optional): The name of the broker member. Defaults to "".
            contact_person (str, optional): The contact person name of the broker. Defaults to "".
            contact_number (str, optional): The contact number of the broker. Defaults to "".
            member_code (str, optional): The code of the broker member. Defaults to "".
            province_id (int, optional): The ID of the province where the broker is located. Defaults to 0.
            district_id (int, optional): The ID of the district where the broker is located. Defaults to 0.
            municipality_id (int, optional): The ID of the municipality where the broker is located. Defaults to 0.

        Returns:
            json: A json response returned by NEPSE API.
        """
        api = ROOT_URL + api_dict['broker_api']['api']
        method = api_dict['broker_api']['method']
        querystring = {"page": "0", "size": "500"}

        payload = {
            "memberName": member_name,
            "contactPerson": contact_person,
            "contactNumber": contact_number,
            "memberCode": member_code,
            "provinceId": province_id,
            "districtId": district_id,
            "municipalityId": municipality_id
        }

        return self.call_nepse_function(url=api, method=method, querystring=querystring, payload=payload)

    def get_sector_detail(self):
        """
        Retrieve details of all sectors listed in the NEPSE.
        Returns:
            json: A json response returned by NEPSE API.
        """
        api = ROOT_URL + api_dict['sector_api']['api']
        method = api_dict['sector_api']['method']
        querystring = {"page": "0", "size": "500"}

        return self.call_nepse_function(url=api, method=method, querystring=querystring)

    def _get_sector_index(self) -> json:
        """
        Retrieve index of all sectors listed in the NEPSE.

        Returns:
            json: A json response returned by NEPSE API.
        """
        api = ROOT_URL + api_dict['sector_index_api']['api']
        method = api_dict['sector_index_api']['method']
        querystring = {"page": "0", "size": "500"}

        return self.call_nepse_function(url=api, method=method, querystring=querystring)

    def _return_ticker_id(self, ticker_list: list) -> dict:

        all_security = self._get_security()
        values = {d.get('symbol'): d.get('id')
                  for d in all_security if d.get('symbol') in ticker_list}

        if len(ticker_list) != len(values.keys()):
            raise ValueError(
                f"{set(ticker_list).difference(values.keys())}: Not Found")

        return values

    def get_ticker_info(self, ticker=None) -> dict:
        """
        Retrieve all the information of ticker from Nepse

        Args:
            ticker (str or list): if list provided returns information of all the provided ticker or list
                                  if str provided then returns provided tickers information

        Returns:
            dict: dictionary contiang provided ticker as key and values as retrived value form nepse

        Raise:
            ValueError: If provided ticker is not found in nepse

        """

        if not (ticker):
            raise ValueError('Ticker is required')

        if isinstance(ticker, str):
            ticker = [ticker]

        ticker = [x.upper() for x in ticker]

        values = self._return_ticker_id(ticker)

        return_value = dict()

        for key, value in values.items():

            api = ROOT_URL + \
                api_dict['ticker_info_api']['api'] + '/' + str(value)
            method = api_dict['ticker_info_api']['method']

            return_value[key] = self.call_nepse_function(
                url=api, method=method, which_payload='stock-live')

        if len(ticker) == 1:
            return return_value[ticker[0]]

        return return_value

    def get_ticker_contact_info(self, ticker=None) -> dict:
        """
        Retrieve all the contact information of ticker from Nepse. 
        i.e:
            Phone Number
            Email
            Contact Person
            Location etc

        args:
            ticker (str or list): if list provided returns information of all the provided ticker or list
                                  if str provided then returns provided tickers information

        Returns:
            dict: dictionary contiang provided ticker as key and values as retrived value form nepse

        Raise:
            ValueError: If provided ticker is not found in nepse

        """

        if not (ticker):
            raise ValueError('Ticker is required')

        if isinstance(ticker, str):
            ticker = [ticker]

        ticker = [x.upper() for x in ticker]

        values = self._return_ticker_id(ticker)

        return_value = dict()

        for key, value in values.items():

            api = ROOT_URL + \
                api_dict['ticker_contact_api']['api'] + '/' + str(value)
            method = api_dict['ticker_contact_api']['method']

            return_value[key] = self.call_nepse_function(
                url=api, method=method)

        if len(ticker) == 1:
            return return_value[ticker[0]]

        return return_value

    def get_live_indices(self, indices_id: int = 58) -> list:
        """
            Retrive the live indices data of provided indices if market is close then retrives the last trading date's index

            Note: Refer to following id while using this function you can only pass following values

            Banking SubIndex -> 51
            Hotels And Tourism Index -> 52
            Others Index -> 53
            HydroPower Index -> 54
            Development Bank Index -> 55
            Manufacturing And Processing -> 56
            Sensitive Index -> 57
            NEPSE Index -> 58
            Non Life Insurance -> 59
            Finance Index -> 60
            Trading Index -> 61
            Float Index -> 62
            Sensitive Float Index -> 63
            Microfinance Index -> 64
            Life Insurance -> 65
            Mutual Fund -> 66
            Investment Index -> 67

            Args:
                indices_id (int, default-> 58)

            Returns:
                list : containg time and index inside list

            Raise: 
                ValueError: If proivded indices is not valid
        """

        if indices_id < 51 or indices_id > 67:
            raise ValueError(f"'{indices_id}' is not valid indices ID.")

        api = ROOT_URL + \
            api_dict['indices_live_api']['api'] + "/" + str(indices_id)
        method = api_dict['indices_live_api']['method']

        return self.call_nepse_function(url=api, method=method, which_payload='sector-live')

    # incomplete pyload not working
    # testing requrired

    def get_live_stock(self):
        if not (self.is_market_open()):
            raise ValueError('Market is closed')

        api = ROOT_URL + api_dict['stock_live_api']['api']
        method = api_dict['stock_live_api']['method']

        return self.call_nepse_function(url=api, method=method, which_payload='stock-live')
