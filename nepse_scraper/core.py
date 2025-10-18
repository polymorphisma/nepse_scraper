# nepse_scraper/core.py
import logging
import warnings
from typing import Any, Dict, Optional

import requests
import certifi
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib3.exceptions import InsecureRequestWarning

from .auth import PayloadParser, TokenParser
from .endpoints import api_dict
from .exceptions import SSLCertVerificationError, NepseScraperException

logger = logging.getLogger(__name__)
ROOT_URL = 'https://www.nepalstock.com'


class NepseAPISession:
    def __init__(self, verify_ssl: bool = True):
        self._token_parser = TokenParser()
        self._payload_parser = PayloadParser()
        self.access_token: Optional[str] = None
        self.token_details: Optional[Dict[str, Any]] = None
        
        self._market_open_id: Optional[int] = None
        
        self.session = requests.Session()
        
        if verify_ssl:
            self.session.verify = certifi.where()
        else:
            self.session.verify = False
            warnings.warn(
                "SSL certificate verification has been disabled. This is not recommended and may be insecure.",
                InsecureRequestWarning
            )

        retry_strategy = Retry(
            total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive', 'Referer': f'{ROOT_URL}/',
        })
        logger.debug("NepseAPISession initialized.")

    def _get_access_token(self) -> None:
        if self.access_token: return
        logger.info("No active token found. Fetching new access token from NEPSE.")
        auth_endpoint = api_dict['authenticate_api']
        url = ROOT_URL + auth_endpoint['api']
        try:
            response = self.session.request(auth_endpoint['method'], url)
            response.raise_for_status()
            token_response = response.json()
            for i in range(1, 6): token_response[f'salt{i}'] = int(token_response[f'salt{i}'])
            self.access_token, _ = self._token_parser.parse_token_response(token_response)
            self.token_details = token_response
            logger.info("Successfully authenticated and stored new token.")
        except requests.exceptions.SSLError as e:
            logger.error(f"SSL Certificate Verification failed: {e}", exc_info=True)
            # Returing custom exception for ssl verification.
            raise SSLCertVerificationError(
                "SSL certificate verification failed. This is likely due to the NEPSE server's "
                "incomplete certificate chain or a network proxy. "
                "Try initializing the client with: NepseScraper(verify_ssl=False)"
            ) from e
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to authenticate with NEPSE API: {e}", exc_info=True)
            raise e

    def _fetch_market_open_id(self) -> int:
        if self._market_open_id is not None:
            logger.debug(f"Using cached market_open_id: {self._market_open_id}")
            return self._market_open_id

        self._get_access_token() # We need to be authenticated to call this.
        logger.debug("Fetching market open ID for payload calculation.")
        endpoint = api_dict['marketopen_api']
        url = ROOT_URL + endpoint['api']
        headers = {'Authorization': f'Salter {self.access_token}'}
        
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            market_data = response.json()
            self._market_open_id = market_data["id"]
            return self._market_open_id
        except (requests.exceptions.RequestException, KeyError) as e:
            logger.error(f"Failed to fetch or parse market open ID: {e}", exc_info=True)
            raise IOError("Could not retrieve the necessary payload ID from NEPSE.") from e


    def _get_payload_id(self, which_payload: str) -> int:
        self._get_access_token()
        given_id = self._fetch_market_open_id()
        
        return self._payload_parser.calculate_payload_id(
            given_id=given_id,
            token_details=self.token_details,
            which=which_payload
        )

    def get(self, path: str, params: Optional[Dict] = None) -> requests.Response:
        self._get_access_token()
        url = ROOT_URL + path
        headers = {'Authorization': f'Salter {self.access_token}'}
        logger.debug(f"Making GET request to: {url} with params: {params}")
        resp = self.session.get(url, params=params, headers=headers)
        resp.raise_for_status()
        return resp

    def post(self, path: str, payload: Optional[Dict] = None, params: Optional[Dict] = None, which_payload: Optional[str] = None) -> requests.Response:
        self._get_access_token()
        url = ROOT_URL + path
        headers = {'Authorization': f'Salter {self.access_token}'}
        
        if payload is None:
            final_payload = {'id': self._get_payload_id(which_payload=which_payload)}
        else:
            final_payload = payload

        logger.debug(f"Making POST request to: {url} with payload: {final_payload} and params: {params}")
        resp = self.session.post(url, json=final_payload, params=params, headers=headers)
        resp.raise_for_status()
        return resp