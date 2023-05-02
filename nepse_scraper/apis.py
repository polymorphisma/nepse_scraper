api_dict = {
    "authenticate_api": {"api":"https://www.nepalstock.com.np/api/authenticate/prove", "method":"GET"},
    "today_price_api": {"api":"https://www.nepalstock.com.np/api/nots/nepse-data/today-price", "method":"POST"},
    "marketopen_api":{"api":"https://www.nepalstock.com.np/api/nots/nepse-data/market-open", "method":"GET"},
    "refer_api":{"api":"https://www.nepalstock.com.np", "method":"GET"},
    "head_indices_api":{"api":"https://www.nepalstock.com/api/nots/index/history/", "method":"GET"}, # -> should add index ID like https://www.nepalstock.com/api/nots/index/history/51
    "sectorwise_summary_api": {"api":"https://www.nepalstock.com.np/api/nots/sectorwise", "method":"GET"},
    "market_summary_api": {"api":"https://www.nepalstock.com.np/api/nots/market-summary-history", "method":"GET"},
}