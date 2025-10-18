# nepse_scraper/auth.py

import json
import logging ## LOGGING: Import the logging module
from datetime import datetime
from wasmtime import Store, Module, Instance
from importlib.resources import files
from typing import Any, Callable, Dict, List, Tuple

## LOGGING: Get a logger specific to this module
logger = logging.getLogger(__name__)

WASM_FILE = files('nepse_scraper').joinpath('nepse.wasm')


class TokenParser:
    def __init__(self) -> None:
        self.store: Store = Store()
        module: Module = Module.from_file(self.store.engine, WASM_FILE)
        instance: Instance = Instance(self.store, module, [])

        self.cdx: Callable[..., int] = instance.exports(self.store)["cdx"]
        self.rdx: Callable[..., int] = instance.exports(self.store)["rdx"]
        self.bdx: Callable[..., int] = instance.exports(self.store)["bdx"]
        self.ndx: Callable[..., int] = instance.exports(self.store)["ndx"]
        self.mdx: Callable[..., int] = instance.exports(self.store)["mdx"]
        logger.debug("TokenParser initialized with WASM module.") ## LOGGING

    def parse_token_response(self, token_response: Dict[str, Any]) -> Tuple[str, str]:
        logger.debug("Starting token response parsing.") ## LOGGING
        n: int = self.cdx(self.store, token_response['salt1'], token_response['salt2'],
                          token_response['salt3'], token_response['salt4'], token_response['salt5'])
        l: int = self.rdx(self.store, token_response['salt1'], token_response['salt2'],
                          token_response['salt4'], token_response['salt3'], token_response['salt5'])
        o: int = self.bdx(self.store, token_response['salt1'], token_response['salt2'],
                          token_response['salt4'], token_response['salt3'], token_response['salt5'])
        p: int = self.ndx(self.store, token_response['salt1'], token_response['salt2'],
                          token_response['salt4'], token_response['salt3'], token_response['salt5'])
        q: int = self.mdx(self.store, token_response['salt1'], token_response['salt2'],
                          token_response['salt4'], token_response['salt3'], token_response['salt5'])
        i: int = self.cdx(self.store, token_response['salt2'], token_response['salt1'],
                          token_response['salt3'], token_response['salt5'], token_response['salt4'])
        r: int = self.rdx(self.store, token_response['salt2'], token_response['salt1'],
                          token_response['salt3'], token_response['salt4'], token_response['salt5'])
        s: int = self.bdx(self.store, token_response['salt2'], token_response['salt1'],
                          token_response['salt4'], token_response['salt3'], token_response['salt5'])
        t: int = self.ndx(self.store, token_response['salt2'], token_response['salt1'],
                          token_response['salt4'], token_response['salt3'], token_response['salt5'])
        u: int = self.mdx(self.store, token_response['salt2'], token_response['salt1'],
                          token_response['salt4'], token_response['salt3'], token_response['salt5'])

        access_token: str = token_response['accessToken']
        refresh_token: str = token_response['refreshToken']

        parsed_access_token: str = (
            access_token[0:n] + access_token[n+1:l] + access_token[l+1:o] +
            access_token[o+1:p] + access_token[p+1:q] + access_token[q+1:]
        )
        parsed_refresh_token: str = (
            refresh_token[0:i] + refresh_token[i+1:r] + refresh_token[r+1:s] +
            refresh_token[s+1:t] + refresh_token[t+1:u] + refresh_token[u+1:]
        )
        logger.debug("Successfully parsed access and refresh tokens.") ## LOGGING

        return (parsed_access_token, parsed_refresh_token)


class PayloadParser:
    def __init__(self) -> None:
        ## REFACTOR: Removed all network-related attributes (url, method, headers).
        # This class should only perform calculations.
        self.dummyData: List[int] = [
            147, 117, 239, 143, 157, 312, 161, 612, 512, 804, 411, 527, 170, 511, 421, 667, 764, 621,
            301, 106, 133, 793, 411, 511, 312, 423, 344, 346, 653, 758, 342, 222, 236, 811, 711, 611,
            122, 447, 128, 199, 183, 135, 489, 703, 800, 745, 152, 863, 134, 211, 142, 564, 375, 793,
            212, 153, 138, 153, 648, 611, 151, 649, 318, 143, 117, 756, 119, 141, 717, 113, 112, 146,
            162, 660, 693, 261, 362, 354, 251, 641, 157, 178, 631, 192, 734, 445, 192, 883, 187, 122,
            591, 731, 852, 384, 565, 596, 451, 772, 624, 691
        ]
        logger.debug("PayloadParser initialized.") ## LOGGING

    ## REFACTOR: The method no longer makes a network call.
    # It now requires the `given_id` from the market-open endpoint to be passed in.
    def calculate_payload_id(
        self,
        given_id: int,
        token_details: Dict[str, Any],
        which: str
    ) -> int:
        today: int = datetime.now().day
        payload_id: int = self.dummyData[given_id] + given_id + 2 * today
        
        logger.debug(f"Initial payload calculation: id={payload_id} from given_id={given_id}, today={today}") ## LOGGING

        if which == 'stock-live':
            return payload_id

        if which == 'sector-live':
            index_value: int = 3 if payload_id % 10 < 5 else 1
        else:
            index_value = 1 if payload_id % 10 < 5 else 3

        payload_id = (
            payload_id
            + token_details.get(f"salt{index_value+1}", 0) * today
            - token_details.get(f"salt{index_value}", 0)
        )
        logger.debug(f"Final calculated payload_id: {payload_id} for type='{which}'") ## LOGGING

        return payload_id