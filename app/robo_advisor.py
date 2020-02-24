#app/robo_advisor.py

import requests
import json
from datetime import datetime

#adapted from prof-rossetti (intended for groceries exercise)
def to_usd(my_price):
    return f"${my_price:,.2f}"

symbol = "MSFT"
API_KEY = "AT4O43WGEJDDMJQI"
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"

response = requests.get(request_url)


parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys())

latest_day = dates[0]

###########################
#   Getting latest close  #
###########################

latest_close = parsed_response["Time Series (Daily)"][f"{latest_day}"]["4. close"]



###########################
#    Getting recent high  #
###########################

high_prices = []

for i in dates:
    high_prices.append(parsed_response["Time Series (Daily)"][f"{str(i)}"]["2. high"])

recent_high = max(high_prices)


###########################
#    Getting recent low  #
###########################

recent_low = parsed_response["Time Series (Daily)"][f"{last_refreshed}"]["3. low"]


print(datetime.today())



print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")