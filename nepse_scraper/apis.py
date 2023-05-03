api_dict = {
    "authenticate_api": {"api":"/api/authenticate/prove", "method":"GET"},
    "today_price_api": {"api":"/api/nots/nepse-data/today-price", "method":"POST"},
    "marketopen_api":{"api":"/api/nots/nepse-data/market-open", "method":"GET"},
    "refer_api":{"api":"", "method":"GET"},
    "head_indices_api":{"api":"/api/nots/index/history", "method":"GET"}, # -> should add index ID like https://www.nepalstock.com/api/nots/index/history/51
    "sectorwise_summary_api": {"api":"/api/nots/sectorwise", "method":"GET"},
    "market_summary_history_api": {"api":"/api/nots/market-summary-history", "method":"GET"},
    "disclosure":{"api":"/api/nots/news/companies/disclosure", "method":"GET"},
    "top_gainer":{"api":"/api/nots/top-ten/top-gainer", "method":"GET"},
    "top_loser":{"api":"/api/nots/top-ten/top-loser", "method":"GET"},
    "top_turnover":{"api":"/api/nots/top-ten/turnover", "method":"GET"},
    "top_trade":{"api":"/api/nots/top-ten/trade", "method":"GET"},
    "top_transaction":{"api":"/api/nots/top-ten/transaction", "method":"GET"},
    "market_summary_api":{"api":"/api/nots/market-summary", "method":"GET"},
    "security_api":{"api":"/api/nots/company/list","method":"GET"},
    "marketcap_api":{"api":"/api/nots/nepse-data/marcapbydate","method":"GET"},
    "trading_average_api":{"api":"/api/nots/nepse-data/trading-average","method":"GET"},
    "broker_api":{"api":"/api/nots/member","method":"POST"},
    "sector_api":{"api":"/api/nots/sector", "method":"GET"},
    "sector_index_api":{"api":"/api/nots/index", "method":"GET"},
}