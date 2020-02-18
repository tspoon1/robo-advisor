# app/robo_advisor.py
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


print("REQUESTING SOME DATA FROM THE INTERNET...")

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS")
symbol = "TSLA"

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"
print("URL:", request_url)

response = requests.get(request_url)
print(type(response))
#print(dir(response))
print(response.status_code)
#print(response.text)
print(type(response.text))

parsed_response = json.loads(response.text)
print(type(parsed_response)) #> list

print(parsed_response)

# for any_prod in parsed_response:
#     print(any_prod["id"], any_prod["name"])
# first_prod = parsed_response[0]

# print(first_prod["name"])


print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")