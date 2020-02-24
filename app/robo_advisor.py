#app/robo_advisor.py

import json
import csv
import os
from datetime import datetime

import requests

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

low_prices = []

for i in dates:
    low_prices.append(parsed_response["Time Series (Daily)"][f"{str(i)}"]["3. low"])

recent_low = min(low_prices)



######################################################
#     WRITING TO CSV
######################################################

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=["city", "name"])
    writer.writeheader() # uses fieldnames set above
    writer.writerow({"city": "New York", "name": "Yankees"})
    writer.writerow({"city": "New York", "name": "Mets"})
    writer.writerow({"city": "Boston", "name": "Red Sox"})
    writer.writerow({"city": "New Haven", "name": "Ravens"})


##########################
#   Begin Output         #
##########################

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA")
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
print(f"WRITING DATA TO {csv_file_path}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")