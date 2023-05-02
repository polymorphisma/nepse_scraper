import requests
from datetime import datetime, date
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import time
from wasmtime import Store,Module,Instance
import json
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.append(ROOT_DIR)

import paths
from apis import api_dict

ROOT_URL = 'https://www.nepalstock.com.np'
SLEEP_TIME = 3000 # -> wait time for every failed request(in milisecond)


class TokenParser():
    def __init__(self):
        self.store = Store()
        module = Module.from_file(self.store.engine, paths.wasm_file)
        instance = Instance(self.store,module,[])

        self.cdx = instance.exports(self.store)["cdx"]
        self.rdx = instance.exports(self.store)["rdx"]
        self.bdx = instance.exports(self.store)["bdx"]
        self.ndx = instance.exports(self.store)["ndx"]
        self.mdx = instance.exports(self.store)["mdx"]
        

    def parse_token_response(self, token_response):
        n = self.cdx(self.store,token_response['salt1'], token_response['salt2'], token_response['salt3'], token_response['salt4'], token_response['salt5'])
        l = self.rdx(self.store,token_response['salt1'], token_response['salt2'], token_response['salt4'], token_response['salt3'], token_response['salt5'])
        o = self.bdx(self.store,token_response['salt1'], token_response['salt2'], token_response['salt4'], token_response['salt3'], token_response['salt5'])
        p = self.ndx(self.store,token_response['salt1'], token_response['salt2'], token_response['salt4'], token_response['salt3'], token_response['salt5'])
        q = self.mdx(self.store,token_response['salt1'], token_response['salt2'], token_response['salt4'], token_response['salt3'], token_response['salt5'])
        
        i = self.cdx(self.store,token_response['salt2'], token_response['salt1'], token_response['salt3'], token_response['salt5'], token_response['salt4'])
        r = self.rdx(self.store,token_response['salt2'], token_response['salt1'], token_response['salt3'], token_response['salt4'], token_response['salt5'])
        s = self.bdx(self.store,token_response['salt2'], token_response['salt1'], token_response['salt4'], token_response['salt3'], token_response['salt5'])
        t = self.ndx(self.store,token_response['salt2'], token_response['salt1'], token_response['salt4'], token_response['salt3'], token_response['salt5'])
        u = self.mdx(self.store,token_response['salt2'], token_response['salt1'], token_response['salt4'], token_response['salt3'], token_response['salt5'])

        access_token  = token_response['accessToken']
        refresh_token = token_response['refreshToken']
        
        parsed_access_token = access_token[0:n] + access_token[n+1:l] + access_token[l+1:o] + access_token[o+1:p] + access_token[p+1:q] + access_token[q+1:]
        parsed_refresh_token = refresh_token[0:i] + refresh_token[i+1:r] + refresh_token[r+1:s] + refresh_token[s+1:t] + refresh_token[t+1:u] + refresh_token[u+1:]
        
        return (parsed_access_token, parsed_refresh_token)

class PayloadParser():
    def __init__(self):
        self.dummyData = [147, 117, 239, 143, 157, 312, 161, 612, 512, 804, 411, 527, 170, 511, 421, 667, 764, 621, 301, 106, 133, 793, 411, 511, 312, 423, 344, 346, 653, 758, 342, 222, 236, 811, 711, 611, 122, 447, 128, 199, 183, 135, 489, 703, 800, 745, 152, 863, 134, 211, 142, 564, 375, 793, 212, 153, 138, 153, 648, 611, 151, 649, 318, 143, 117, 756, 119, 141, 717, 113, 112, 146, 162, 660, 693, 261, 362, 354, 251, 641, 157, 178, 631, 192, 734, 445, 192, 883, 187, 122, 591, 731, 852, 384, 565, 596, 451, 772, 624, 691]
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
        headers = {'Authorization': f'Salter {access_token_value[0]}', **self.headers}
        
        response = requests.request(self.method, self.url, headers=headers, data=self.payload, verify=False)
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

        payload_id = payload_id + access_token_value[1].get(f"salt{index_value+1}") *  today - access_token_value[1].get(f"salt{index_value}")

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
        self.token_parser= TokenParser()

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

    def request_api(self, url, access_token, method='GET', which_payload = None, querystring = None, payload=None):
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
        headers = {'Authorization': f'Salter {access_token[0]}', **self.headers}

        if payload == None:
            payload = {'id': self.parser_obj.return_payload(access_token, which=which_payload)}


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
            response.raise_for_status()  # Raise an exception if the response status code is not successful
            return response
        
        except requests.exceptions.RequestException as err:
            print(f"Error sending request: {err}")
            return None
        

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

        token_response = requests.request(self.token_method, self.token_url, headers=header, verify=False).json()
        for salt_index in range(1, 6):
            token_response[f'salt{salt_index}'] = int(token_response[f'salt{salt_index}'])
     
        return [self.token_parser.parse_token_response(token_response)[0], token_response]
    
    def return_data(self, url, access_token, method='GET', which_payload=None,  querystring = None, payload=None):
        return self.request_api(method=method, url = url, access_token = access_token, which_payload=which_payload, querystring=querystring, payload=payload)

from retrying import retry
import csv

class Request_module:
    def __init__(self) -> None:
        self.nepse_obj = Nepse()
        self.desired_status = 200

    @retry(wait_fixed = SLEEP_TIME)
    def call_nepse_function(self, url, method,  querystring=None, payload=None):
        try:
            access_token = self.nepse_obj.get_valid_token()
            response = self.nepse_obj.return_data(url, access_token=access_token, method=method, querystring=querystring, payload=payload)

            if response.status_code != self.desired_status:
                raise ValueError('Unexpected status code: {}'.format(response.status_code))
            
            return response.json()
        
        except Exception as exp:
            print(exp)
            raise ValueError('Unexpected Error: {}'.format(exp))
        
    def is_trading_day(self):
        """
        Check if today is a trading day on the Nepal Stock Exchange (NEPSE).
        
        Returns:
            True if today is a trading day, False otherwise.
        """
        api = ROOT_URL + api_dict['marketopen_api']['api']
        method = api_dict['marketopen_api']['method']

        response = self.call_nepse_function(url=api, method=method)

        date_ = response['asOf'].split('T')[0]

        if date_ != str(date.today()):
            return False
        
        return True

    def get_today_price(self, date_= None) -> json:
        api = ROOT_URL + api_dict['today_price_api']['api']
        method = api_dict['today_price_api']['method']

        querystring = {"page":"0","size":"500","businessDate":date_}

        return self.call_nepse_function(url=api, method=method, querystring=querystring)
    
    def get_head_indices(self) -> dict:
        api = ROOT_URL + api_dict['head_indices_api']['api']
        method = api_dict['head_indices_api']['method']

        querystring = {"page":"0","size":"500"}

        dicts = {}

        with open(paths.headindices_path, 'r') as rf:
            csv_reader = csv.reader(rf)

            # skip the header row
            next(csv_reader)
            for row_values in csv_reader:
                index_name = row_values[0]
                print(index_name)
                dicts[index_name] = self.call_nepse_function(url=api + index_name, method=method, querystring=querystring)

        return dicts
    
    def get_sectorwise_summary(self, date_=None):
        api = ROOT_URL + api_dict['sectorwise_summary_api']['api']
        method = api_dict['sectorwise_summary_api']['method']

        querystring = {"page":"0","size":"500","businessDate":date_}


        return self.call_nepse_function(url=api, method=method, querystring=querystring)

    def get_market_summary(self, date_ = None):
        api = ROOT_URL + api_dict['market_summary_history_api']['api']
        method = api_dict['market_summary_history_api']['method']

        querystring = {"page":"0","size":"500","businessDate":date_}


        return self.call_nepse_function(url=api, method=method, querystring=querystring)
    
    def get_news(self):
        api = ROOT_URL + api_dict['disclosure']['api']
        method = api_dict['disclosure']['method']

        return self.call_nepse_function(url=api, method=method)
    
    def get_top_gainer(self):
        api = ROOT_URL + api_dict['top_gainer']['api']
        method = api_dict['top_gainer']['method']


        return self.call_nepse_function(url=api, method=method)
    
    def get_top_loser(self):
        api = ROOT_URL + api_dict['top_loser']['api']
        method = api_dict['top_loser']['method']

        return self.call_nepse_function(url=api, method=method)
    
    def get_top_turnover(self):
        api = ROOT_URL + api_dict['top_turnover']['api']
        method = api_dict['top_turnover']['method']


        return self.call_nepse_function(url=api, method=method)

    def get_top_trade(self):
        api = ROOT_URL + api_dict['top_trade']['api']
        method = api_dict['top_trade']['method']

        return self.call_nepse_function(url=api, method=method)

    def get_top_transaction(self):
        api = ROOT_URL + api_dict['top_transaction']['api']
        method = api_dict['top_transaction']['method']

        return self.call_nepse_function(url=api, method=method)
    
    def get_today_market_summary(self):
        api = ROOT_URL + api_dict['market_summary_api']['api']
        method = api_dict['market_summary_api']['method']

        return self.call_nepse_function(url=api, method=method)

    def get_security_detail(self):
        api = ROOT_URL + api_dict['security_api']['api']
        method = api_dict['security_api']['method']

        return self.call_nepse_function(url=api, method=method)
    
    def get_marketcap(self):
        api = ROOT_URL + api_dict['marketcap_api']['api']
        method = api_dict['marketcap_api']['method']

        return self.call_nepse_function(url=api, method=method)
    

    def get_trading_average(self, date_=None, n_days=120):
        api = ROOT_URL + api_dict['trading_average_api']['api']
        method = api_dict['trading_average_api']['method']

        querystring = {"page":"0","size":"500","businessDate":date_,"nDays":n_days}

        return self.call_nepse_function(url=api, method=method, querystring=querystring)
    
    def get_broker(self, member_name= "", contact_person="", contact_number = "", member_code="", province_id = 0, district_id = 0, municipality_id = 0):

        api = ROOT_URL + api_dict['broker_api']['api']
        method = api_dict['broker_api']['method']
        querystring = {"page":"0","size":"500"}


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
        api = ROOT_URL + api_dict['sector_api']['api']
        method = api_dict['sector_api']['method']
        querystring = {"page":"0","size":"500"}

        return self.call_nepse_function(url=api, method=method, querystring=querystring)
    
