from nepse_scraper import Request_module

# create object from Request_module class
request_obj = Request_module()

# getting today's price from nepse
today_price = request_obj.get_today_price()
print(today_price)

